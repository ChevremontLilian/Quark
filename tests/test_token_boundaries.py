import unittest
from unittest.mock import patch

import torch

from Scripts.pyAI import GPT, _encode_with_special_tokens


class StubTokenizer:
    def bos_id(self):
        return 2

    def eos_id(self):
        return 3

    def encode(self, text: str, out_type: type = int) -> list[int]:
        if text and out_type is int:
            return [10, 11]
        return []


class TokenBoundaryTests(unittest.TestCase):
    def test_training_encodings_start_with_bos_and_end_with_eos(self):
        token_ids = _encode_with_special_tokens(
            StubTokenizer(),
            "Q: Bonjour R: Salut",
            add_eos=True
        )

        self.assertEqual(token_ids, [2, 10, 11, 3])

    def test_prompt_encoding_starts_with_bos_without_eos(self):
        token_ids = _encode_with_special_tokens(
            StubTokenizer(),
            "Bonjour",
            add_eos=False
        )

        self.assertEqual(token_ids, [2, 10, 11])

    def test_generation_stops_after_eos(self):
        model = GPT("", torch.device("cpu"))
        model.tokenizer = StubTokenizer()

        def predict_eos(indices):
            logits = torch.full((indices.shape[0], indices.shape[1], 5), -100.0)
            logits[:, :, 3] = 100.0
            return logits, None

        with patch.object(model, "forward", side_effect=predict_eos):
            output = model.generate(torch.tensor([[2, 10]]), num_new_tokens=10)

        self.assertEqual(output.tolist(), [[2, 10, 3]])


if __name__ == "__main__":
    unittest.main()
