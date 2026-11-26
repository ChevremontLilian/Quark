"""Validation and deterministic cleanup for the French question/answer corpus."""

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import os
from pathlib import Path
import random
import re
import tempfile
import unicodedata
import warnings

if __package__:
    from .config import CORPUS_MAIN
else:
    from config import CORPUS_MAIN


_RECORD_PATTERN = re.compile(r"^Q:\s*(.*?)\s+R:\s*(.*)$")
_KNOWN_NOISE_PATTERNS = (
    re.compile(r"\bmentirondelic\b", re.IGNORECASE),
    re.compile(r"l['’]X est résultat de l['’]action de Y ou qualité de Y", re.IGNORECASE),
    re.compile(r"\bJe vais X cette tâche\b", re.IGNORECASE),
)


@dataclass(frozen=True)
class QARecord:
    question: str
    answer: str
    line_number: int

    @property
    def text(self):
        return f"Q: {self.question} R: {self.answer}"


def normalize_text(text):
    return " ".join(unicodedata.normalize("NFC", text).split())


def format_qa_record(question, answer):
    question = normalize_text(question)
    answer = normalize_text(answer)
    if not question or not answer:
        raise ValueError("question and answer must not be empty")
    return f"Q: {question} R: {answer}"


def append_qa_record(path, question, answer):
    path = Path(path)
    record = format_qa_record(question, answer)
    if path.exists() and path.stat().st_size:
        load_qa_records(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("ab+") as corpus_file:
        corpus_file.seek(0, os.SEEK_END)
        if corpus_file.tell():
            corpus_file.seek(-1, os.SEEK_END)
            if corpus_file.read(1) != b"\n":
                corpus_file.write(b"\n")
        corpus_file.write(f"{record}\n".encode("utf-8"))
    return record


def question_group_key(question):
    return normalize_text(question).casefold()


def load_qa_records(path, deduplicate=False, skip_invalid=False, filter_noise=False):
    """Parse Q/R lines, optionally skipping malformed rows and known noise."""
    records = []
    seen_pairs = set()
    invalid_lines = []
    noisy_lines = []
    path = Path(path)

    with path.open("r", encoding="utf-8-sig") as corpus_file:
        for line_number, raw_line in enumerate(corpus_file, start=1):
            if not raw_line.strip():
                continue

            match = _RECORD_PATTERN.fullmatch(raw_line.strip())
            if match is None:
                message = f"{path}:{line_number}: expected one 'Q: ... R: ...' record"
                if not skip_invalid:
                    raise ValueError(message)
                invalid_lines.append(message)
                continue

            question = normalize_text(match.group(1))
            answer = normalize_text(match.group(2))
            if not question or not answer:
                message = f"{path}:{line_number}: question and answer must not be empty"
                if not skip_invalid:
                    raise ValueError(message)
                invalid_lines.append(message)
                continue

            if filter_noise and any(
                pattern.search(f"{question} {answer}")
                for pattern in _KNOWN_NOISE_PATTERNS
            ):
                noisy_lines.append(line_number)
                continue

            pair = (question, answer)
            if deduplicate and pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            records.append(QARecord(question, answer, line_number))

    if invalid_lines:
        warnings.warn(
            f"Skipped {len(invalid_lines)} invalid corpus line(s); "
            f"first: {invalid_lines[0]}",
            RuntimeWarning,
            stacklevel=2,
        )
    if noisy_lines:
        warnings.warn(
            f"Filtered {len(noisy_lines)} known noisy corpus record(s); "
            f"line(s): {', '.join(map(str, noisy_lines[:10]))}",
            RuntimeWarning,
            stacklevel=2,
        )
    if not records:
        raise ValueError(f"{path}: corpus contains no question/answer records")
    return records


def split_indices_by_group(groups, validation_fraction=0.1, seed=42):
    """Split record indices deterministically without separating repeated prompts."""
    if not 0 < validation_fraction < 1:
        raise ValueError("validation_fraction must be between 0 and 1")

    indices_by_group = defaultdict(list)
    for index, group in enumerate(groups):
        indices_by_group[group].append(index)

    group_names = list(indices_by_group)
    if len(group_names) < 2:
        raise ValueError("At least two distinct question groups are required")

    random.Random(seed).shuffle(group_names)
    validation_group_count = min(
        max(int(len(group_names) * validation_fraction), 1),
        len(group_names) - 1,
    )
    validation_groups = set(group_names[:validation_group_count])
    train_indices = []
    validation_indices = []

    for group, indices in indices_by_group.items():
        target = validation_indices if group in validation_groups else train_indices
        target.extend(indices)

    return train_indices, validation_indices


def clean_corpus(path):
    """Normalize whitespace and remove strict Q/R duplicates, preserving alternatives."""
    path = Path(path)
    records = load_qa_records(path, deduplicate=True)
    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as corpus_file:
            temporary_path = Path(corpus_file.name)
            for record in records:
                corpus_file.write(f"{record.text}\n")
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()

    return len(records)


def _report(path):
    records = load_qa_records(path)
    pairs = Counter((record.question, record.answer) for record in records)
    question_counts = Counter(
        question_group_key(record.question) for record in records
    )
    grouped_answers = defaultdict(set)
    for record in records:
        grouped_answers[question_group_key(record.question)].add(record.answer)

    repeated_questions = sum(count > 1 for count in question_counts.values())
    conflicting_questions = sum(
        len(answers) > 1 for answers in grouped_answers.values()
    )
    print(f"Exemples valides : {len(records)}")
    print(f"Doublons stricts : {sum(count - 1 for count in pairs.values())}")
    print(f"Questions répétées : {repeated_questions}")
    print(f"Questions avec réponses distinctes : {conflicting_questions}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", default=CORPUS_MAIN, help="Fichier Q/R à vérifier")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Normalise le fichier et supprime uniquement les doublons stricts",
    )
    arguments = parser.parse_args(argv)

    _report(arguments.corpus)
    if arguments.clean:
        count = clean_corpus(arguments.corpus)
        print(f"Corpus normalisé : {count} exemples conservés dans {arguments.corpus}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
