import os
import tempfile
import time
from contextlib import nullcontext

import sentencepiece as spm
import torch
import torch.nn as nn
import torch.nn.functional as F

if __package__:
    from .TransformerBlock import OptimizedTransformerBlock
    from .config import GENERATION_PARAMS, MODEL_PARAMS, TRAINING_PARAMS
    from .corpus import load_qa_records, question_group_key, split_indices_by_group
else:
    from TransformerBlock import OptimizedTransformerBlock
    from config import GENERATION_PARAMS, MODEL_PARAMS, TRAINING_PARAMS
    from corpus import load_qa_records, question_group_key, split_indices_by_group


def _build_warmup_cosine_scheduler(
    optimizer: torch.optim.Optimizer,
    max_steps: int,
) -> tuple[torch.optim.lr_scheduler.LRScheduler, int]:
    """Builds a 5% linear warm-up followed by cosine decay to 10% of the base LR."""
    warmup_steps = (
        min(max(1, max_steps // 20), 500, max_steps - 1)
        if max_steps > 1
        else 0
    )
    base_lr = optimizer.param_groups[0]["lr"]

    if warmup_steps == 0:
        return (
            torch.optim.lr_scheduler.CosineAnnealingLR(
                optimizer, T_max=max_steps, eta_min=base_lr * 0.1
            ),
            warmup_steps,
        )

    warmup = torch.optim.lr_scheduler.LinearLR(
        optimizer,
        start_factor=0.1,
        end_factor=1.0,
        total_iters=warmup_steps,
    )
    cosine = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer,
        T_max=max_steps - warmup_steps,
        eta_min=base_lr * 0.1,
    )
    return (
        torch.optim.lr_scheduler.SequentialLR(
            optimizer, schedulers=[warmup, cosine], milestones=[warmup_steps]
        ),
        warmup_steps,
    )


def _encode_with_special_tokens(
    tokenizer: spm.SentencePieceProcessor,
    text: str,
    add_eos: bool,
) -> list[int]:
    token_ids = [tokenizer.bos_id(), *tokenizer.encode(text, out_type=int)]
    if add_eos:
        token_ids.append(tokenizer.eos_id())
    return token_ids


def _encode_prompt(tokenizer: spm.SentencePieceProcessor, question: str) -> list[int]:
    """Encode the exact question prefix shared by training and chat."""
    return [
        tokenizer.bos_id(),
        *tokenizer.encode(f"Q: {question} R:", out_type=int),
    ]


def _encode_qa_record(
    tokenizer: spm.SentencePieceProcessor,
    question: str,
    answer: str,
    max_sequence_length: int | None = None,
) -> tuple[list[int], int]:
    """Encode prompt and response separately to preserve their token boundary."""
    prompt_ids = _encode_prompt(tokenizer, question)
    answer_ids = tokenizer.encode(f" {answer}", out_type=int)
    if max_sequence_length is not None:
        if max_sequence_length < 3:
            raise ValueError("max_sequence_length must be at least 3.")
        answer_ids = answer_ids[: max_sequence_length - 2]
        prefix_limit = max_sequence_length - len(answer_ids) - 1
        if len(prompt_ids) > prefix_limit:
            if prefix_limit == 1:
                prompt_ids = prompt_ids[:1]
            else:
                prompt_ids = [
                    prompt_ids[0],
                    *prompt_ids[-(prefix_limit - 1):],
                ]
    return [*prompt_ids, *answer_ids, tokenizer.eos_id()], len(prompt_ids)


def open_file(
    filepath: str,
    mode: str,
    new_text: str = None,
    encoding: str = "utf-8",
) -> str | None:
    """Open a file for reading or append text."""
    if mode == "r":
        with open(filepath, mode, encoding=encoding) as file:
            return file.read()
    if mode == "a":
        with open(filepath, mode, encoding=encoding) as file:
            if new_text is not None:
                file.write(new_text)
        return None
    raise ValueError(f"Unsupported mode: {mode}")


class GPT(nn.Module):
    """Decoder-only Transformer with a grouped Q/R training pipeline."""

    def __init__(self, source_dir: str, device: torch.device):
        super().__init__()
        self.source_dir = source_dir
        self.token_ids = None
        self.tokenizer = None
        self.device = torch.device(device)
        self.data = None
        self.sequences = None
        self.sequence_groups = []
        self.sequence_lengths = None
        self.input_ids = None
        self.target_ids = None
        self.response_target_ids = None
        self.vocab_size = None
        self.block_size = MODEL_PARAMS["block_size"]
        self.embedding_dim = MODEL_PARAMS["embedding_dim"]
        self.num_heads = MODEL_PARAMS["num_heads"]
        self.num_layers = MODEL_PARAMS["num_layers"]
        self.learning_rate = MODEL_PARAMS["learning_rate"]
        self.dropout_rate = MODEL_PARAMS["dropout"]
        self.batch_size = TRAINING_PARAMS["batch_size"]
        self.loss_on_prompt = MODEL_PARAMS["loss_on_prompt"]
        self.dropout = nn.Dropout(self.dropout_rate)
        self.position_embedding = nn.Embedding(self.block_size, self.embedding_dim)
        self.blocks = nn.Sequential(
            *[
                OptimizedTransformerBlock(
                    self.embedding_dim,
                    self.block_size,
                    self.num_heads,
                    self.dropout_rate,
                    memory_size=MODEL_PARAMS["memory_size"],
                    num_reflection_tokens=MODEL_PARAMS["num_reflection_tokens"],
                )
                for _ in range(self.num_layers)
            ]
        )
        self.final_norm = nn.LayerNorm(self.embedding_dim)
        self.token_embedding = None
        self.output_head = None
        self.loaded_model = None
        self.last_training_metrics = None
        self.to(self.device)
        self._initialize_weights()

    def _initialize_weights(self) -> None:
        """Apply GPT-2-style initialization, scaling residual projections."""
        for module_name, module in self.named_modules():
            if isinstance(module, nn.Linear):
                nn.init.normal_(module.weight, mean=0.0, std=0.02)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
                if module_name.endswith(
                    ("attention.projection", "reseau_ffwd.reseau.3")
                ):
                    module.weight.data.mul_(1 / (2 * self.num_layers) ** 0.5)
            elif isinstance(module, nn.Embedding):
                nn.init.normal_(module.weight, mean=0.0, std=0.02)
            elif isinstance(module, nn.LayerNorm):
                nn.init.ones_(module.weight)
                nn.init.zeros_(module.bias)
        for module in self.modules():
            if isinstance(module, OptimizedTransformerBlock):
                nn.init.normal_(module.attention.prefix_k, mean=0.0, std=0.02)
                nn.init.normal_(module.attention.prefix_v, mean=0.0, std=0.02)

    def _ensure_vocabulary_layers(self, vocab_size: int) -> None:
        if self.token_embedding is not None:
            if self.token_embedding.num_embeddings != vocab_size:
                raise RuntimeError(
                    "Tokenizer vocabulary changed after model initialization. "
                    "Use a fresh model and checkpoint when retraining the tokenizer."
                )
            return
        self.token_embedding = nn.Embedding(vocab_size, self.embedding_dim)
        self.output_head = nn.Linear(self.embedding_dim, vocab_size, bias=False)
        self.output_head.weight = self.token_embedding.weight
        self.to(self.device)
        self._initialize_weights()

    def _load_tokenizer(self, retrain_tokenizer: bool = False) -> None:
        os.makedirs(self.source_dir, exist_ok=True)
        tokenizer_path = os.path.join(self.source_dir, "tokenizer.model")
        if retrain_tokenizer:
            if self.data is not None or self.loaded_model is not None:
                raise RuntimeError(
                    "Tokenizer retraining requires a fresh GPT instance so existing "
                    "weights cannot become misaligned with token IDs."
                )
            if self.token_embedding is not None:
                raise RuntimeError(
                    "Tokenizer retraining requires a fresh GPT instance."
                )
            with tempfile.TemporaryDirectory(
                prefix=".tokenizer-", dir=self.source_dir
            ) as temporary_directory:
                model_prefix = os.path.join(temporary_directory, "tokenizer")
                spm.SentencePieceTrainer.Train(
                    input=self._corpus_path,
                    model_prefix=model_prefix,
                    vocab_size=MODEL_PARAMS["vocab_size"],
                    model_type="bpe",
                    character_coverage=1.0,
                    hard_vocab_limit=False,
                    pad_id=0,
                    unk_id=1,
                    bos_id=2,
                    eos_id=3,
                )
                os.replace(f"{model_prefix}.model", tokenizer_path)
                os.replace(
                    f"{model_prefix}.vocab",
                    os.path.join(self.source_dir, "tokenizer.vocab"),
                )
        elif not os.path.isfile(tokenizer_path):
            raise FileNotFoundError(
                f"Tokenizer not found at {tokenizer_path}; retrain it explicitly "
                "with load_corpus(..., retrain_tokenizer=True)."
            )

        self.tokenizer = spm.SentencePieceProcessor()
        if not self.tokenizer.load(tokenizer_path):
            raise RuntimeError(f"Unable to load SentencePiece tokenizer: {tokenizer_path}")
        special_token_ids = (
            self.tokenizer.pad_id(),
            self.tokenizer.unk_id(),
            self.tokenizer.bos_id(),
            self.tokenizer.eos_id(),
        )
        if special_token_ids != (0, 1, 2, 3):
            raise RuntimeError(
                "Tokenizer special token IDs must be PAD=0, UNK=1, BOS=2, EOS=3; "
                f"got {special_token_ids}."
            )
        self.vocab_size = self.tokenizer.get_piece_size()
        self._ensure_vocabulary_layers(self.vocab_size)

    def load_corpus(self, corpus_name: str, retrain_tokenizer: bool = False) -> None:
        """Load the tokenizer and prepare padded Q/R tensors; retraining is opt-in."""
        has_drive = bool(os.path.splitdrive(corpus_name)[0])
        is_windows_rooted_path = (
            os.name == "nt" and os.path.isabs(corpus_name) and not has_drive
        )
        corpus_path = (
            os.path.join(self.source_dir, corpus_name.lstrip("/\\"))
            if is_windows_rooted_path or not os.path.isabs(corpus_name)
            else corpus_name
        )
        if not os.path.isfile(corpus_path):
            raise FileNotFoundError(f"Corpus '{corpus_path}' not found.")

        try:
            self._corpus_path = corpus_path
            self._load_tokenizer(retrain_tokenizer=retrain_tokenizer)
            records = load_qa_records(
                corpus_path,
                deduplicate=True,
                skip_invalid=True,
                filter_noise=True,
            )
            self.sequences = []
            self.sequence_groups = []
            prompt_lengths = []
            for record in records:
                encoded, answer_start = _encode_qa_record(
                    self.tokenizer,
                    record.question,
                    record.answer,
                    max_sequence_length=self.block_size + 1,
                )
                self.sequences.append(torch.tensor(encoded, dtype=torch.long))
                self.sequence_groups.append(question_group_key(record.question))
                prompt_lengths.append(answer_start)
            if not self.sequences:
                raise ValueError("The corpus contains no non-empty training sequences.")

            self.sequence_boundaries = [0]
            for sequence in self.sequences:
                self.sequence_boundaries.append(
                    self.sequence_boundaries[-1] + len(sequence)
                )
            input_rows = [sequence[:-1] for sequence in self.sequences]
            target_rows = [sequence[1:] for sequence in self.sequences]
            response_rows = []
            for targets, answer_start in zip(target_rows, prompt_lengths):
                response_targets = targets.clone()
                response_targets[: max(answer_start - 1, 0)] = -100
                response_rows.append(response_targets)

            pad_id = self.tokenizer.pad_id()
            self.input_ids = nn.utils.rnn.pad_sequence(
                input_rows, batch_first=True, padding_value=pad_id
            ).to(self.device)
            self.target_ids = nn.utils.rnn.pad_sequence(
                target_rows, batch_first=True, padding_value=pad_id
            ).to(self.device)
            self.response_target_ids = nn.utils.rnn.pad_sequence(
                response_rows, batch_first=True, padding_value=-100
            ).to(self.device)
            self.sequence_lengths = torch.tensor(
                [len(row) for row in input_rows],
                dtype=torch.long,
                device=self.device,
            )
            self.data = torch.cat(self.sequences).to(self.device)
            print(
                f"Corpus: {len(records)} enregistrements, "
                f"longueur maximale {self.input_ids.size(1)} tokens "
                f"(contexte: {self.block_size}, vocabulaire: {self.vocab_size})"
            )
        except Exception as error:
            raise RuntimeError(f"Failed to load corpus '{corpus_name}': {error}") from error

    def _get_sequence_boundaries(self) -> list[int]:
        """Return the start indices of each encoded Q/R sequence."""
        return self.sequence_boundaries

    def forward(
        self,
        indices: torch.Tensor,
        targets: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor | None]:
        if self.token_embedding is None or self.output_head is None:
            raise RuntimeError("No tokenizer vocabulary loaded. Call load_corpus() first.")
        _, seq_length = indices.shape
        if seq_length > self.block_size:
            raise ValueError(
                f"Input length {seq_length} exceeds block_size {self.block_size}."
            )
        positions = torch.arange(seq_length, device=indices.device)
        x = self.token_embedding(indices) + self.position_embedding(positions)
        x = self.dropout(x)
        x = self.final_norm(self.blocks(x))
        logits = self.output_head(x)
        loss = None
        if targets is not None:
            loss = F.cross_entropy(
                logits.reshape(-1, logits.size(-1)),
                targets.reshape(-1),
                ignore_index=-100,
            )
        return logits, loss

    def _atomic_save_state_dict(self, state_dict: dict, checkpoint_path: str) -> None:
        checkpoint_directory = os.path.dirname(checkpoint_path)
        os.makedirs(checkpoint_directory, exist_ok=True)
        descriptor, temporary_path = tempfile.mkstemp(
            prefix=f".{os.path.basename(checkpoint_path)}.",
            suffix=".tmp",
            dir=checkpoint_directory,
        )
        os.close(descriptor)
        try:
            torch.save(state_dict, temporary_path)
            os.replace(temporary_path, checkpoint_path)
        finally:
            if os.path.exists(temporary_path):
                os.remove(temporary_path)

    def create_model(self, model_name: str) -> None:
        """Create a checkpoint from the current initialized model."""
        if self.token_embedding is None:
            raise RuntimeError("Load a corpus and tokenizer before creating a model.")
        self.loaded_model = model_name
        self.save_model()

    def reset_parameters(self) -> None:
        """Reinitialize model weights without changing the tokenizer or architecture."""
        self._initialize_weights()

    def load_model(self, model_name: str) -> None:
        """Load a compatible weights-only checkpoint on the configured device."""
        checkpoint_path = os.path.join(self.source_dir, model_name + ".pth")
        if self.tokenizer is None:
            self._load_tokenizer()
        if not os.path.isfile(checkpoint_path):
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")
        self._ensure_vocabulary_layers(self.vocab_size)
        try:
            state_dict = torch.load(
                checkpoint_path,
                map_location=self.device,
                weights_only=True,
            )
            self.load_state_dict(state_dict)
        except (RuntimeError, ValueError, TypeError) as error:
            raise RuntimeError(
                f"Checkpoint '{checkpoint_path}' is incompatible with the current "
                "model/tokenizer. Preserve it as a legacy checkpoint and train a "
                "new model from scratch."
            ) from error
        self.loaded_model = model_name
        print(f"Model {model_name} loaded successfully.")

    def save_model(self) -> str:
        """Atomically save the current state to the active model checkpoint."""
        if self.loaded_model is None:
            raise ValueError("No active checkpoint name. Set loaded_model before saving.")
        checkpoint_path = os.path.join(self.source_dir, self.loaded_model + ".pth")
        self._atomic_save_state_dict(self.state_dict(), checkpoint_path)
        return "saved"

    def change_learning_rate(self, lr: float) -> None:
        self.learning_rate = lr

    def _autocast(self):
        if self.device.type == "cuda" and torch.cuda.is_bf16_supported():
            return torch.autocast(device_type="cuda", dtype=torch.bfloat16)
        return nullcontext()

    def fit(
        self,
        convergence_threshold: float,
        eval_interval: int = 100,
        patience: int = 10,
        batch_size: int | None = None,
        max_steps: int = 10_000,
        eval_iterations: int = 50,
        on_progress=None,
        stop_event=None,
        loss_on_prompt: bool | None = None,
    ) -> bool:
        """Train with a grouped split, response-only loss, and best-checkpoint restore."""
        if self.data is None:
            raise RuntimeError("No corpus loaded. Call load_corpus() before fit().")
        if convergence_threshold <= 0:
            raise ValueError("Convergence threshold must be > 0.")
        if eval_interval <= 0 or patience <= 0 or max_steps <= 0 or eval_iterations <= 0:
            raise ValueError(
                "eval_interval, patience, max_steps and eval_iterations must be > 0."
            )
        batch_size = self.batch_size if batch_size is None else batch_size
        if batch_size <= 0:
            raise ValueError("batch_size must be > 0.")
        if self.loaded_model is None:
            raise ValueError(
                "Set an active checkpoint name before fitting so the best model can be saved."
            )

        train_indices, val_indices = split_indices_by_group(self.sequence_groups)
        include_prompt_loss = (
            self.loss_on_prompt if loss_on_prompt is None else loss_on_prompt
        )
        train_target_ids = (
            self.target_ids if include_prompt_loss else self.response_target_ids
        )
        bucket_size = max(batch_size * 20, batch_size)

        def make_buckets(indices):
            ordered = sorted(indices, key=lambda index: int(self.sequence_lengths[index]))
            return [
                torch.tensor(ordered[start:start + bucket_size], device=self.device)
                for start in range(0, len(ordered), bucket_size)
            ]

        split_buckets = {
            "train": make_buckets(train_indices),
            "val": make_buckets(val_indices),
        }

        def get_batch(split: str):
            buckets = split_buckets[split]
            bucket_sizes = torch.tensor([len(bucket) for bucket in buckets], dtype=torch.float)
            bucket_index = torch.multinomial(bucket_sizes, 1).item()
            bucket = buckets[bucket_index]
            positions = torch.randint(len(bucket), (batch_size,), device=self.device)
            sampled_indices = bucket[positions]
            sequence_length = int(self.sequence_lengths[sampled_indices].max().item())
            actual_tokens = int(self.sequence_lengths[sampled_indices].sum().item())
            return (
                self.input_ids[sampled_indices, :sequence_length],
                train_target_ids[sampled_indices, :sequence_length],
                actual_tokens,
            )

        @torch.no_grad()
        def estimate_loss() -> dict[str, float]:
            was_training = self.training
            self.eval()
            results = {}
            try:
                for split in ("train", "val"):
                    losses = []
                    for _ in range(eval_iterations):
                        inputs, targets, _ = get_batch(split)
                        with self._autocast():
                            _, loss = self(inputs, targets)
                        if loss is None or not torch.isfinite(loss):
                            raise FloatingPointError(
                                f"Non-finite {split} loss during evaluation."
                            )
                        losses.append(loss.item())
                    results[split] = sum(losses) / len(losses)
            finally:
                self.train(was_training)
            return results

        decay_parameters = []
        no_decay_parameters = []
        seen_parameters = set()
        for name, parameter in self.named_parameters():
            if not parameter.requires_grad or id(parameter) in seen_parameters:
                continue
            seen_parameters.add(id(parameter))
            if parameter.ndim == 2 and "prefix_" not in name:
                decay_parameters.append(parameter)
            else:
                no_decay_parameters.append(parameter)

        optimizer_options = {"lr": self.learning_rate, "betas": (0.9, 0.95)}
        if self.device.type == "cuda":
            optimizer_options["fused"] = True
        optimizer = torch.optim.AdamW(
            [
                {"params": decay_parameters, "weight_decay": 0.05},
                {"params": no_decay_parameters, "weight_decay": 0.0},
            ],
            **optimizer_options,
        )
        scheduler, warmup_steps = _build_warmup_cosine_scheduler(optimizer, max_steps)
        print(
            f"Split: {len(train_indices)} séquences train, {len(val_indices)} validation "
            f"({len(set(self.sequence_groups))} groupes de questions)"
        )
        print(
            f"Config: block_size={self.block_size}, embedding_dim={self.embedding_dim}, "
            f"layers={self.num_layers}, heads={self.num_heads}, "
            f"batch_size={batch_size}, lr={self.learning_rate}, "
            f"warmup_steps={warmup_steps}, bf16={self.device.type == 'cuda' and torch.cuda.is_bf16_supported()}"
        )

        step = 0
        best_val_loss = float("inf")
        best_state = None
        patience_counter = 0
        stopped = False
        progress_interval = min(10, eval_interval)
        tokens_since_eval = 0
        total_tokens_seen = 0
        evaluation_started = time.perf_counter()
        self.train()

        try:
            while step < max_steps:
                if stop_event is not None and stop_event.is_set():
                    stopped = True
                    print("Arrêt demandé; le meilleur checkpoint est conservé.")
                    break

                inputs, targets, actual_tokens = get_batch("train")
                optimizer.zero_grad(set_to_none=True)
                with self._autocast():
                    _, loss = self(inputs, targets)
                if loss is None or not torch.isfinite(loss):
                    raise FloatingPointError(
                        f"Non-finite training loss at optimizer step {step + 1}."
                    )
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.parameters(), max_norm=1.0)
                optimizer.step()
                scheduler.step()
                step += 1
                tokens_since_eval += actual_tokens
                total_tokens_seen += actual_tokens

                if step == 1 or step % progress_interval == 0:
                    if on_progress:
                        on_progress(
                            f"Entraînement — étape {step}/{max_steps}, "
                            f"perte: {loss.item():.4f}"
                        )

                if step % eval_interval == 0 or step == max_steps:
                    losses = estimate_loss()
                    elapsed = max(time.perf_counter() - evaluation_started, 1e-9)
                    tokens_per_second = tokens_since_eval / elapsed
                    current_lr = scheduler.get_last_lr()[0]
                    improved = losses["val"] < best_val_loss
                    if improved:
                        best_val_loss = losses["val"]
                        patience_counter = 0
                        best_state = {
                            name: tensor.detach().cpu().clone()
                            for name, tensor in self.state_dict().items()
                        }
                        self.save_model()
                        status = "meilleur checkpoint sauvegardé"
                    else:
                        patience_counter += 1
                        status = f"patience {patience_counter}/{patience}"
                    print(
                        f"Step {step:>6} | train loss: {losses['train']:.4f} | "
                        f"val loss (réponse): {losses['val']:.4f} | "
                        f"lr: {current_lr:.2e} | tokens/s: {tokens_per_second:.1f} | "
                        f"{status}"
                    )
                    self.last_training_metrics = {
                        "step": step,
                        "tokens_seen": total_tokens_seen,
                        "train_loss": losses["train"],
                        "val_loss": losses["val"],
                        "tokens_per_second": tokens_per_second,
                    }
                    tokens_since_eval = 0
                    evaluation_started = time.perf_counter()
                    if patience_counter >= patience:
                        print(f"Early stopping à l'étape {step}.")
                        break
                    if losses["val"] < convergence_threshold:
                        print(
                            f"Convergence atteinte: val_loss={losses['val']:.4f} "
                            f"< {convergence_threshold}."
                        )
                        break
        except KeyboardInterrupt:
            stopped = True
            print("\nEntraînement interrompu; le meilleur checkpoint est conservé.")
        finally:
            if best_state is not None:
                self.load_state_dict(best_state)
            self.eval()
        return stopped

    def generate(
        self,
        indices: torch.Tensor,
        num_new_tokens: int,
        temperature: float = GENERATION_PARAMS["temperature"],
        top_k: int | None = GENERATION_PARAMS["top_k"],
    ) -> torch.Tensor:
        """Generate tokens with sampling controls and stop each row at EOS."""
        if num_new_tokens < 0:
            raise ValueError("num_new_tokens must be >= 0.")
        if temperature <= 0:
            raise ValueError("temperature must be > 0.")
        if top_k is not None and top_k <= 0:
            raise ValueError("top_k must be > 0 or None.")

        eos_id = self.tokenizer.eos_id() if self.tokenizer is not None else None
        blocked_ids = []
        for method_name in ("pad_id", "unk_id", "bos_id"):
            method = getattr(self.tokenizer, method_name, None)
            if callable(method):
                token_id = method()
                if token_id >= 0:
                    blocked_ids.append(token_id)

        was_training = self.training
        self.eval()
        finished = torch.zeros(indices.shape[0], dtype=torch.bool, device=indices.device)
        try:
            with torch.no_grad():
                for _ in range(num_new_tokens):
                    truncated_indices = indices[:, -self.block_size:]
                    logits, _ = self(truncated_indices)
                    next_logits = logits[:, -1, :] / temperature
                    for token_id in blocked_ids:
                        if token_id < next_logits.size(-1):
                            next_logits[:, token_id] = float("-inf")
                    if top_k is not None:
                        k = min(top_k, next_logits.size(-1))
                        threshold = torch.topk(next_logits, k).values[:, -1, None]
                        next_logits = next_logits.masked_fill(
                            next_logits < threshold, float("-inf")
                        )
                    next_token = torch.multinomial(F.softmax(next_logits, dim=-1), 1)
                    if eos_id is not None:
                        next_token = torch.where(
                            finished.unsqueeze(1),
                            torch.full_like(next_token, eos_id),
                            next_token,
                        )
                        finished |= next_token.squeeze(1).eq(eos_id)
                    indices = torch.cat((indices, next_token), dim=1)
                    if eos_id is not None and finished.all().item():
                        break
        finally:
            self.train(was_training)
        return indices

    def chat(
        self,
        text: str = "",
        num_new_tokens: int | None = None,
        temperature: float | None = None,
        top_k: int | None = None,
    ) -> str:
        """Accept a raw question and return the generated response only."""
        if self.tokenizer is None:
            raise RuntimeError("No tokenizer loaded. Call load_corpus() first.")
        if not text.strip():
            raise ValueError("Question must not be empty.")
        prompt = _encode_prompt(self.tokenizer, text.strip())
        user_input = torch.tensor([prompt], dtype=torch.long, device=self.device)
        output = self.generate(
            user_input,
            GENERATION_PARAMS["max_new_tokens"] if num_new_tokens is None else num_new_tokens,
            GENERATION_PARAMS["temperature"] if temperature is None else temperature,
            GENERATION_PARAMS["top_k"] if top_k is None else top_k,
        )
        generated_ids = output[0, len(prompt):].tolist()
        if self.tokenizer.eos_id() in generated_ids:
            generated_ids = generated_ids[:generated_ids.index(self.tokenizer.eos_id())]
        return self.tokenizer.decode(generated_ids).strip()

    def get_info(self) -> tuple[str, ...]:
        if self.data is None or self.vocab_size is None:
            raise RuntimeError("Cannot display model info before loading a corpus.")
        return (
            "--------- Model Information ---------\n",
            f"tensor: {self.data}\n",
            f"vocab size: {self.vocab_size}\n",
            f"total parameters: {sum(p.numel() for p in self.parameters()):,}",
        )
