import shutil
import tempfile
import unittest
from pathlib import Path

import torch

from Scripts.TransformerBlock import SharedMultiHeadAttention
from Scripts.pyAI import GPT, _encode_qa_record, _encode_prompt


class StubTokenizer:
    def bos_id(self):
        return 2

    def eos_id(self):
        return 3

    def pad_id(self):
        return 0

    def unk_id(self):
        return 1

    def encode(self, text, out_type=int):
        return [ord(character) % 20 + 4 for character in text]


class ModelPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary_directory.name)
        tokenizer_source = Path(__file__).parents[1] / "Models" / "tokenizer.model"
        shutil.copy2(tokenizer_source, self.directory / "tokenizer.model")
        self.corpus_path = self.directory / "corpus.txt"
        self.corpus_path.write_text(
            "Q: question alpha R: response alpha\n"
            "Q: question beta R: response beta\n"
            "Q: question gamma R: response gamma\n"
            "Q: question delta R: response delta\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temporary_directory.cleanup()

    def make_model(self, corpus_path=None):
        model = GPT(str(self.directory), torch.device("cpu"))
        model.load_corpus(str(corpus_path or self.corpus_path))
        return model

    def test_reloading_corpus_does_not_reinitialize_weights(self):
        model = self.make_model()
        with torch.no_grad():
            model.token_embedding.weight.fill_(0.125)
        weights = model.token_embedding.weight.detach().clone()

        model.load_corpus(str(self.corpus_path))

        self.assertTrue(torch.equal(model.token_embedding.weight, weights))
        self.assertIs(model.output_head.weight, model.token_embedding.weight)

    def test_eval_changes_module_mode(self):
        model = GPT(str(self.directory), torch.device("cpu"))
        model.eval()

        self.assertFalse(model.training)
        self.assertFalse(model.dropout.training)
        self.assertTrue(all(not block.training for block in model.blocks))

    def test_training_and_chat_share_the_exact_prompt_prefix(self):
        tokenizer = StubTokenizer()
        prompt = _encode_prompt(tokenizer, "Bonjour")
        encoded, answer_start = _encode_qa_record(tokenizer, "Bonjour", "Salut")

        self.assertEqual(encoded[:answer_start], prompt)
        self.assertEqual(encoded[-1], tokenizer.eos_id())

    def test_response_loss_masks_prompt_and_padded_targets(self):
        model = self.make_model()
        record = model.sequences[0]
        record_question = "question alpha"
        prompt = _encode_prompt(model.tokenizer, record_question)
        encoded, answer_start = _encode_qa_record(
            model.tokenizer, record_question, "response alpha"
        )
        self.assertEqual(record.tolist(), encoded)

        first_answer_target = answer_start - 1
        self.assertTrue(
            torch.all(model.response_target_ids[0, :first_answer_target] == -100)
        )
        self.assertEqual(
            model.response_target_ids[0, first_answer_target].item(),
            record[answer_start].item(),
        )
        actual_length = model.sequence_lengths[0].item()
        self.assertTrue(torch.all(model.response_target_ids[0, actual_length:] == -100))
        self.assertEqual(prompt, encoded[:answer_start])

    def test_fit_can_disable_prompt_loss_when_model_default_enables_it(self):
        model = self.make_model()
        model.loaded_model = "response-loss-override"
        model.loss_on_prompt = True
        seen_targets = []
        original_forward = model.forward

        def capture_targets(indices, targets=None):
            if targets is not None:
                seen_targets.append(targets.detach().clone())
            return original_forward(indices, targets)

        model.forward = capture_targets
        model.fit(
            convergence_threshold=1e-8,
            eval_interval=1,
            patience=5,
            batch_size=1,
            max_steps=1,
            eval_iterations=1,
            loss_on_prompt=False,
        )

        self.assertTrue(any(torch.any(targets == -100) for targets in seen_targets))

    def test_attention_is_causal_and_prefix_is_visible_to_every_position(self):
        attention = SharedMultiHeadAttention(
            4, 8, 2, dropout_rate=0.0, memory_size=1, num_reflection_tokens=1
        ).eval()
        values = torch.randn(1, 4, 4)
        changed_future = values.clone()
        changed_future[:, 3] += 100
        baseline = attention(values)
        changed = attention(changed_future)
        torch.testing.assert_close(baseline[:, :3], changed[:, :3])

        with torch.no_grad():
            attention.shared_proj.weight.zero_()
            attention.projection.weight.copy_(torch.eye(4))
            attention.projection.bias.zero_()
            attention.prefix_k.zero_()
            attention.prefix_v.fill_(1)
        outputs = attention(torch.zeros(1, 4, 4))
        self.assertTrue(torch.all(outputs > 0))

    def test_fit_saves_and_restores_the_best_checkpoint(self):
        model = self.make_model()
        model.loaded_model = "best-test"

        model.fit(
            convergence_threshold=1e-8,
            eval_interval=1,
            patience=5,
            batch_size=1,
            max_steps=2,
            eval_iterations=1,
        )

        checkpoint = torch.load(
            self.directory / "best-test.pth",
            map_location="cpu",
            weights_only=True,
        )
        for name, value in model.state_dict().items():
            torch.testing.assert_close(value.cpu(), checkpoint[name])


if __name__ == "__main__":
    unittest.main()
