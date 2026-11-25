import tempfile
import unittest
from pathlib import Path

from Scripts.corpus import (
    append_qa_record,
    clean_corpus,
    format_qa_record,
    load_qa_records,
    question_group_key,
    split_indices_by_group,
)


class CorpusTests(unittest.TestCase):
    def test_format_and_append_normalize_multiline_input(self):
        self.assertEqual(
            format_qa_record("  Bonjour\nà tous ", " Salut\t! "),
            "Q: Bonjour à tous R: Salut !",
        )
        with tempfile.TemporaryDirectory() as directory:
            corpus_path = Path(directory) / "corpus.txt"
            corpus_path.write_text("Q: Déjà R: présent.", encoding="utf-8")

            append_qa_record(corpus_path, "Nouvelle\nquestion", "Nouvelle réponse")

            self.assertEqual(
                corpus_path.read_text(encoding="utf-8"),
                "Q: Déjà R: présent.\nQ: Nouvelle question R: Nouvelle réponse\n",
            )

    def test_loader_normalizes_and_removes_only_strict_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            corpus_path = Path(directory) / "corpus.txt"
            corpus_path.write_text(
                "Q:  Bonjour   ? R: Salut.\n"
                "Q: Bonjour ?   R: Salut.\n"
                "Q: Bonjour ? R: Bonjour.\n",
                encoding="utf-8",
            )

            records = load_qa_records(corpus_path, deduplicate=True)

        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].text, "Q: Bonjour ? R: Salut.")
        self.assertEqual(records[1].answer, "Bonjour.")

    def test_loader_rejects_malformed_records(self):
        with tempfile.TemporaryDirectory() as directory:
            corpus_path = Path(directory) / "corpus.txt"
            corpus_path.write_text("not a Q/R record\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, r"corpus\.txt:1"):
                load_qa_records(corpus_path)

    def test_cleaner_preserves_alternative_answers_and_removes_blank_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            corpus_path = Path(directory) / "corpus.txt"
            corpus_path.write_text(
                "Q: salut R: Bonjour.\n\n"
                "Q: salut R: Salut !\n"
                "Q: salut R: Bonjour.\n",
                encoding="utf-8",
            )

            count = clean_corpus(corpus_path)

            self.assertEqual(count, 2)
            self.assertEqual(
                corpus_path.read_text(encoding="utf-8").splitlines(),
                ["Q: salut R: Bonjour.", "Q: salut R: Salut !"],
            )

    def test_split_keeps_repeated_questions_in_one_partition(self):
        groups = [
            question_group_key("Bonjour"),
            question_group_key("bonjour "),
            question_group_key("Quelle heure ?"),
            question_group_key("Combien font 2+2 ?"),
            question_group_key("Définis un mot"),
            question_group_key("Une question distincte"),
        ]

        train_indices, validation_indices = split_indices_by_group(groups)

        self.assertTrue(set(train_indices).isdisjoint(validation_indices))
        self.assertEqual(set(train_indices) | set(validation_indices), set(range(6)))
        self.assertEqual(0 in train_indices, 1 in train_indices)
        self.assertEqual(
            split_indices_by_group(groups),
            (train_indices, validation_indices),
        )


if __name__ == "__main__":
    unittest.main()
