import torch
import torch.nn as nn
import torch.nn.functional as F
import sentencepiece as spm
import os

if __package__:
    from .TransformerBlock import OptimizedTransformerBlock
    from .corpus import (
        load_qa_records, question_group_key, split_indices_by_group
    )
else:
    from TransformerBlock import OptimizedTransformerBlock
    from corpus import load_qa_records, question_group_key, split_indices_by_group


def _build_warmup_cosine_scheduler(
    optimizer: torch.optim.Optimizer,
    max_steps: int
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
                optimizer,
                T_max=max_steps,
                eta_min=base_lr * 0.1
            ),
            warmup_steps
        )

    warmup = torch.optim.lr_scheduler.LinearLR(
        optimizer,
        start_factor=0.1,
        end_factor=1.0,
        total_iters=warmup_steps
    )
    cosine = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer,
        T_max=max_steps - warmup_steps,
        eta_min=base_lr * 0.1
    )
    return (
        torch.optim.lr_scheduler.SequentialLR(
            optimizer,
            schedulers=[warmup, cosine],
            milestones=[warmup_steps]
        ),
        warmup_steps
    )


def _encode_with_special_tokens(
    tokenizer: spm.SentencePieceProcessor,
    text: str,
    add_eos: bool
) -> list[int]:
    token_ids = [tokenizer.bos_id(), *tokenizer.encode(text, out_type=int)]
    if add_eos:
        token_ids.append(tokenizer.eos_id())
    return token_ids


def open_file(filepath: str, mode: str, new_text: str = None, encoding: str = "utf-8") -> str | None:
    """
    Opens a file for reading or appending text.

    Args:
        filepath (str): Full path to the file.
        mode (str): 'r' to read content, 'a' to append text.
        new_text (str, optional): Text to append if mode == 'a'.
        encoding (str): File encoding (default "utf-8").

    Returns:
        str | None: File content if mode == 'r', else None.

    Raises:
        ValueError: If the provided mode is neither 'r' nor 'a'.
    """
    if mode == 'r':
        with open(filepath, mode, encoding=encoding) as file:
            return file.read()
    elif mode == 'a':
        with open(filepath, mode, encoding=encoding) as file:
            if new_text is not None:
                file.write(new_text)
    else:
        raise ValueError(f"Unsupported mode: {mode}")

class GPT(nn.Module):
    """
    GPT-style language model (decoder-only transformer).
    Trains its own BPE tokenizer (SentencePiece) on a text corpus,
    then stacks multiple Transformer blocks to predict the next token.
    Provides methods for creating, loading, saving, training, and chatting with the model.
    """

    def __init__(self, source_dir: str, device: torch.device):
        """
        Initializes the tokenizer, loads the corpus, and builds all
        network layers (embeddings, Transformer blocks, output head).

        Args:
            source_dir (str): Directory where tokenizer and checkpoints are saved.
        """
        super().__init__()
        self.source_dir = source_dir
        self.token_ids = None
        self.tokenizer = None
        self.device = device
        self.data = None
        self.sequences = None  # Liste des séquences tokenisées (une par ligne du corpus)
        self.sequence_groups = []
        self.vocab_size = None
        self.block_size = 200
        self.embedding_dim = 128
        self.num_heads = 4
        self.num_layers = 4
        self.learning_rate = 1e-4
        self.dropout_rate = 0.1
        self.batch_size = 8  # Réduit pour plus de stabilité
        self.dropout = nn.Dropout(self.dropout_rate)
        self.position_embedding = nn.Embedding(self.block_size, self.embedding_dim)
        self.blocks = nn.Sequential(
            *[OptimizedTransformerBlock(
                self.embedding_dim,
                self.block_size,
                self.num_heads,
                self.dropout_rate,
                memory_size=64,
                num_reflection_tokens=4,
                rank=16
            ).to(self.device) for _ in range(self.num_layers)]
        )
        self.final_norm = nn.LayerNorm(self.embedding_dim)
        self.loaded_model = None

    def load_corpus(self, corpus_name: str) -> None:
        """
        Trains a SentencePiece tokenizer on the corpus and loads the data.
        Each line of the corpus is treated as a separate sequence.

        Args:
            corpus_name (str): Absolute corpus path or a path relative to source_dir.

        Raises:
            FileNotFoundError: If the corpus file is not found.
            RuntimeError: If an error occurs during loading.
        """
        try:
            has_drive = bool(os.path.splitdrive(corpus_name)[0])
            is_windows_rooted_path = os.name == "nt" and os.path.isabs(corpus_name) and not has_drive
            corpus_path = (
                os.path.join(self.source_dir, corpus_name.lstrip("/\\"))
                if is_windows_rooted_path or not os.path.isabs(corpus_name)
                else corpus_name
            )
            tokenizer_prefix = os.path.join(self.source_dir, "tokenizer")
            tokenizer_path = f"{tokenizer_prefix}.model"
            self.tokenizer = spm.SentencePieceProcessor()
            spm.SentencePieceTrainer.Train(
                input=corpus_path,
                model_prefix=tokenizer_prefix,
                vocab_size=1024,
                model_type="bpe",
                character_coverage=1.0,
                pad_id=0,
                unk_id=1,
                bos_id=2,
                eos_id=3
            )
            self.tokenizer.load(tokenizer_path)
            self.vocab_size = self.tokenizer.get_piece_size()
            special_token_ids = (
                self.tokenizer.pad_id(),
                self.tokenizer.unk_id(),
                self.tokenizer.bos_id(),
                self.tokenizer.eos_id()
            )
            if special_token_ids != (0, 1, 2, 3):
                raise RuntimeError(
                    "Tokenizer special token IDs must be PAD=0, UNK=1, BOS=2, EOS=3; "
                    f"got {special_token_ids}."
                )
            
            records = load_qa_records(corpus_path, deduplicate=True)
            self.sequences = []
            self.sequence_groups = []
            self.sequence_boundaries = [0]
            max_seq_length = 0
            for record in records:
                encoded = _encode_with_special_tokens(
                    self.tokenizer,
                    record.text,
                    add_eos=True
                )
                seq_tensor = torch.tensor(encoded, dtype=torch.long)
                self.sequences.append(seq_tensor)
                self.sequence_groups.append(question_group_key(record.question))
                self.sequence_boundaries.append(
                    self.sequence_boundaries[-1] + len(seq_tensor)
                )
                max_seq_length = max(max_seq_length, len(seq_tensor))
            
            if not self.sequences:
                raise ValueError("The corpus contains no non-empty training sequences.")

            print(
                f"Max sequence length: {max_seq_length} tokens "
                f"(context window: {self.block_size})"
            )
            
            # Concatenéer toutes les séquences avec leurs EOS pour créer self.data
            self.data = torch.cat(self.sequences).to(self.device)
            self.token_embedding = nn.Embedding(self.vocab_size, self.embedding_dim)
            self.output_head = nn.Linear(self.embedding_dim, self.vocab_size)
            self.to(self.device)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Corpus '{corpus_name}' not found.")
        except Exception as e:
            raise RuntimeError(f"Failed to load corpus '{corpus_name}': {e}")
    
    def _get_sequence_boundaries(self) -> list[int]:
        """
        Returns the start indices of each sequence in self.data.
        Used for proper train/val split to avoid sequence leakage.
        """
        if not hasattr(self, 'sequence_boundaries'):
            # Fallback: if sequences were not loaded properly, estimate boundaries
            # by finding EOS tokens (id=3)
            eos_positions = (
                self.data == self.tokenizer.eos_id()
            ).nonzero(as_tuple=True)[0].tolist()
            eos_positions.append(len(self.data))  # Add end
            return [0] + [pos + 1 for pos in eos_positions]
        return self.sequence_boundaries

    def forward(self, indices: torch.Tensor, targets: torch.Tensor = None) -> tuple[torch.Tensor, float | None]:
        """
        Forward pass: transforms token indices into logits for next-token prediction.

        Args:
            indices (torch.Tensor): Token indices, shape (batch, time).
            targets (torch.Tensor, optional): Expected indices to compute loss, shape (batch, time).

        Returns:
            tuple: (logits, loss) where loss is None if targets is None.
        """
        if not hasattr(self, "token_embedding"):
            raise RuntimeError("No corpus loaded. Call load_corpus() before training.")

        batch_size, seq_length = indices.shape
        token_embeddings = self.token_embedding(indices)
        position_embeddings = self.position_embedding(torch.arange(seq_length, device=indices.device))
        x = token_embeddings + position_embeddings
        x = self.dropout(x)  # Dropout après les embeddings
        x = self.blocks(x)
        x = self.final_norm(x)
        logits = self.output_head(x)
        loss = None
        if targets is not None:
            batch_size, seq_length, vocab_size = logits.shape
            loss = F.cross_entropy(
                logits.view(batch_size * seq_length, vocab_size),
                targets.view(batch_size * seq_length),
                ignore_index=self.tokenizer.pad_id()
            )
        return logits, loss

    def create_model(self, model_name: str) -> None:
        """
        Saves the current (often untrained) model state to a new file.

        Args:
            model_name (str): Name of the file to create in self.source_dir.
        """
        try:
            if not hasattr(self, 'token_embedding') or not hasattr(self, 'output_head'):
                raise RuntimeError("Cannot create model without loading corpus first. Call load_corpus() before create_model().")
            torch.save(self.state_dict(), f=os.path.join(self.source_dir, model_name + ".pth"))
            print(f"Model {model_name}.pth created.")
        except FileExistsError:
            print(f"{model_name}.pth already exists.")
        except Exception as e:
            print(f"Error: {e}")

    def load_model(self, model_name: str) -> None:
        """
        Loads model weights from a saved checkpoint.

        Args:
            model_name (str): Name of the checkpoint file to load (without .pth extension).
        """
        try:
            checkpoint_path = os.path.join(self.source_dir, model_name + ".pth")
            state_dict = torch.load(checkpoint_path)
            
            # Check if we need to create token_embedding and output_head
            if not hasattr(self, 'token_embedding') or not hasattr(self, 'output_head'):
                # We need to load the tokenizer to get vocab_size
                if self.tokenizer is None:
                    self.tokenizer = spm.SentencePieceProcessor()
                    try:
                        self.tokenizer.load(os.path.join(self.source_dir, "tokenizer.model"))
                    except Exception as e:
                        raise RuntimeError(f"Tokenizer not found. Please load corpus first or ensure tokenizer.model exists: {e}")
                self.vocab_size = self.tokenizer.get_piece_size()
                self.token_embedding = nn.Embedding(self.vocab_size, self.embedding_dim).to(self.device)
                self.output_head = nn.Linear(self.embedding_dim, self.vocab_size).to(self.device)
            
            self.load_state_dict(state_dict)
            self.loaded_model = model_name
            print("Model loaded successfully.")
        except FileNotFoundError:
            print("No model found. Creating a new one...")
            self.create_model(model_name)
        except RuntimeError as e:
            raise RuntimeError(f"Error loading file:\n{e}")

    def save_model(self) -> str:
        """
        Saves the current model state under the loaded model's name (self.loaded_model).

        Returns:
            str: "saved" on success, "Error" on failure.
        """
        try:
            if self.loaded_model is None:
                raise ValueError("No model loaded. Use load_model() first.")
            torch.save(self.state_dict(), f=os.path.join(self.source_dir, self.loaded_model + ".pth"))
            return "saved"
        except Exception as e:
            print(f"Save error: {e}")
            return "Error"
    def change_learning_rate(self, lr: float):
        """
        <table>
        <tr>
            <td>corpus's size</td>
            <td>model's size </td>
            <td>     LR      </td>
        </tr>
        <tr>
            <td> < 1000 </td>
            <td> small (4-8 layers) </td>
            <td> 1e-4 to 5e-5 </td>
        </tr>
        <tr>
            <td> 1000-10k </td>
            <td> Medium (8-12 layers) </td>
            <td> 3e-5 to 1e-4 </td>
        </tr>
        <tr>
            <td> > 10k      </td>
            <td> big (>12 layers)   </td>
            <td> 1e-4 à 3e-4 </td>
        </tr>
        </table>
        """
        self.learning_rate = lr

    def train(
        self,
        convergence_threshold: float,
        eval_interval: int = 100,
        patience: int = 10,
        batch_size: int = None,
        max_steps: int = 10_000,
        eval_iterations: int = 50,
        on_progress=None,
        stop_event=None
    ) -> bool:
        """
        Full training loop for the model.
        Splits data into train and validation by complete question groups,
        performs forward/backward passes with AdamW and cosine scheduler,
        periodically evaluates validation loss, saves the best model, and stops
        either by early stopping (patience) or when the convergence threshold is reached.

        Can be interrupted with Ctrl+C (KeyboardInterrupt), in which case the model is saved.

        Args:
            convergence_threshold: Target validation loss to reach.
            eval_interval: Number of steps between validation evaluations.
            patience: Number of evaluations without improvement before early stopping.
            batch_size: Batch size for training. If None, uses self.batch_size.
            max_steps: Maximum number of optimizer updates.
            eval_iterations: Number of batches used for each train/validation estimate.
            on_progress: Optional callback receiving periodic step and loss updates.
            stop_event: Optional event used to request a graceful stop between steps.

            WARNING: If convergence_threshold < 0.1, training may never stop.
        """
        if self.data is None:
            raise RuntimeError("No corpus loaded. Call load_corpus() before train().")
        if convergence_threshold <= 0:
            raise ValueError("Convergence threshold must be > 0.")
        if eval_interval <= 0 or patience <= 0 or max_steps <= 0 or eval_iterations <= 0:
            raise ValueError("eval_interval, patience, max_steps and eval_iterations must be > 0.")
        if batch_size is None:
            batch_size = self.batch_size
        if batch_size <= 0:
            raise ValueError("batch_size must be > 0.")

        train_indices, val_indices = split_indices_by_group(self.sequence_groups)
        train_sequences = [self.sequences[index] for index in train_indices]
        val_sequences = [self.sequences[index] for index in val_indices]

        print(
            f"Split: {len(train_sequences)} sequences train, "
            f"{len(val_sequences)} sequences validation "
            f"({len(set(self.sequence_groups))} question groups)"
        )

        def get_batch(split: str, bs: int) -> tuple[torch.Tensor, torch.Tensor]:
            """Samples independent records and masks padding out of the loss."""
            sequences = train_sequences if split == "train" else val_sequences
            sampled_indices = torch.randint(len(sequences), (bs,)).tolist()
            input_rows = []
            target_rows = []
            pad_id = self.tokenizer.pad_id()

            for index in sampled_indices:
                sequence = sequences[index]
                if len(sequence) > self.block_size + 1:
                    start = torch.randint(0, len(sequence) - self.block_size, (1,)).item()
                    sequence = sequence[start:start + self.block_size + 1]

                inputs = sequence[:-1]
                targets = sequence[1:]
                padding = self.block_size - len(inputs)
                input_rows.append(F.pad(inputs, (0, padding), value=pad_id))
                target_rows.append(F.pad(targets, (0, padding), value=pad_id))

            return (
                torch.stack(input_rows).to(self.device),
                torch.stack(target_rows).to(self.device)
            )

        @torch.no_grad()
        def estimate_loss() -> dict[str, float]:
            """Estimates loss on train/val splits."""
            nn.Module.train(self, False)
            results = {}
            try:
                for split in ("train", "val"):
                    losses = torch.zeros(eval_iterations)
                    for i in range(eval_iterations):
                        input_batch, target_batch = get_batch(split, batch_size)
                        _, loss = self(input_batch, target_batch)
                        losses[i] = loss.item()
                    results[split] = losses.mean().item()
            finally:
                nn.Module.train(self, True)
            return results

        decay_parameters = []
        no_decay_parameters = []
        for parameter in self.parameters():
            if not parameter.requires_grad:
                continue
            if parameter.ndim == 1:
                no_decay_parameters.append(parameter)
            else:
                decay_parameters.append(parameter)

        weight_decay = 5e-2
        optimizer = torch.optim.AdamW(
            [
                {"params": decay_parameters, "weight_decay": weight_decay},
                {"params": no_decay_parameters, "weight_decay": 0.0}
            ],
            lr=self.learning_rate,
            betas=(0.9, 0.999)
        )
        scheduler, warmup_steps = _build_warmup_cosine_scheduler(
            optimizer,
            max_steps
        )
        step = 0
        best_val_loss = float("inf")
        patience_counter = 0
        stopped = False
        progress_interval = min(10, eval_interval)
        print(f"Training: target -> loss < {convergence_threshold}")
        print(f"Config: block_size={self.block_size}, embedding_dim={self.embedding_dim}, "
              f"num_layers={self.num_layers}, num_heads={self.num_heads}, dropout={self.dropout_rate}")
        print(
            f"Optimizer: AdamW lr={self.learning_rate}, "
            f"weight_decay={weight_decay} (matrices only; biases/norms=0), "
            f"warmup_steps={warmup_steps}, batch_size={batch_size}, "
            f"max_steps={max_steps}"
        )
        nn.Module.train(self, True)

        try:
            while step < max_steps:
                if stop_event is not None and stop_event.is_set():
                    stopped = True
                    print("Training stop requested; saving the current model weights.")
                    self.save_model()
                    break

                # Forward/backward pass
                input_batch, target_batch = get_batch("train", batch_size)
                _, loss = self(input_batch, target_batch)

                # Optimization
                optimizer.zero_grad(set_to_none=True)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.parameters(), max_norm=1.0)
                optimizer.step()
                scheduler.step()
                step += 1

                if step == 1 or step % progress_interval == 0:
                    loss_value = loss.item()
                    progress = f"Entraînement — étape {step}/{max_steps}, perte: {loss_value:.4f}"
                    #print(f"Step {step:>6}/{max_steps} | train loss: {loss_value:.4f}", flush=True)
                    if on_progress:
                        on_progress(progress)

                # Periodic evaluation
                if step % eval_interval == 0 or step == max_steps:
                    losses = estimate_loss()
                    current_lr = scheduler.get_last_lr()[0]

                    if losses["val"] < best_val_loss:
                        best_val_loss = losses["val"]
                        patience_counter = 0
                        status_msg = f"(best val_loss: {best_val_loss:.4f})"
                        print(
                            f"Step {step:>6} | "
                            f"train loss: {losses['train']:.4f} | "
                            f"val loss: {losses['val']:.4f} | "
                            f"lr: {current_lr:.2e} | "
                            f"status: {self.save_model()} {status_msg}"
                        )
                    else:
                        patience_counter += 1
                        status_msg = f"no improvement (patience: {patience_counter}/{patience})"
                        print(
                            f"Step {step:>6} | "
                            f"train loss: {losses['train']:.4f} | "
                            f"val loss: {losses['val']:.4f} | "
                            f"lr: {current_lr:.2e} | "
                            f"status: {status_msg}"
                        )

                    if patience_counter >= patience:
                        print(f"⏹️  Early stopping: {patience} evaluations sans amélioration. Arrêt à step {step}.")
                        break
                    if losses["val"] < convergence_threshold:
                        print(f"✅ Convergence atteinte: val_loss={losses['val']:.4f} < {convergence_threshold}. Arrêt à step {step}.")
                        break
            else:
                print(f"⏹️  Maximum training steps reached: {max_steps}.")
        except KeyboardInterrupt:
            print("\nTraining interrupted; saving the current model weights.")
            stopped = True
            self.save_model()
        except Exception:
            self.save_model()
            raise
        return stopped
    def generate(self, indices: torch.Tensor, num_new_tokens: int) -> torch.Tensor:
        """
        Generates new tokens autoregressively from a starting sequence.
        Stops each sequence at EOS; finished batch rows are padded with EOS.

        Args:
            indices (torch.Tensor): Starting token sequence, shape (batch, time).
            num_new_tokens (int): Number of tokens to generate.

        Returns:
            torch.Tensor: Original sequence with generated tokens appended.
        """
        eos_id = self.tokenizer.eos_id() if self.tokenizer is not None else None
        finished = torch.zeros(indices.shape[0], dtype=torch.bool, device=indices.device)
        for _ in range(num_new_tokens):
            truncated_indices = indices[:, -self.block_size:]
            logits, _ = self(truncated_indices)
            logits = logits[:, -1, :]
            probabilities = F.softmax(logits, dim=-1)
            next_token = torch.multinomial(probabilities, 1)
            if eos_id is not None:
                next_token = torch.where(
                    finished.unsqueeze(1),
                    torch.full_like(next_token, eos_id),
                    next_token
                )
                finished |= next_token.squeeze(1).eq(eos_id)
            indices = torch.cat((indices, next_token), dim=1)
            if eos_id is not None and finished.all().item():
                break
        return indices

    def chat(self, text: str = "", num_new_tokens: int = 20) -> None:
        """
        Encodes user text, generates a sequence of tokens with the model,
        and prints the decoded output.

        Args:
            text (str): Input message to send to the model.
            num_new_tokens (int): Number of tokens to generate.
        """
        try:
            if self.tokenizer is None:
                raise RuntimeError("No tokenizer loaded. Ensure you have loaded a corpus.")
            if len(text) < 1:
                print("Empty message.")
                return

            self.tokenizer.load(os.path.join(self.source_dir, "tokenizer.model"))
            user_input = torch.tensor(
                [_encode_with_special_tokens(self.tokenizer, text, add_eos=False)],
                dtype=torch.long
            ).to(self.device)
            output = self.generate(user_input, num_new_tokens)
            generated_ids = output[0].tolist()
            return self.tokenizer.decode(generated_ids)
        except Exception as e:
            print(f"Generation error: {e}")

    def get_info(self) -> tuple[str, ...]:
        """
        Returns diagnostic information about the model: data tensor,
        vocabulary size, and total number of parameters.

        Returns:
            tuple[str]: Formatted info lines.

        Raises:
            NameError: If info cannot be retrieved (e.g., no model loaded).
        """
        try:
            return (
                "--------- Model Information ---------\n",
                f"tensor: {self.data}\n",
                f"vocab size: {self.vocab_size}\n",
                f"total parameters: {sum(p.numel() for p in self.parameters()):,}"
            )
        except Exception:
            raise NameError("Cannot display model info. Ensure a model is loaded.")