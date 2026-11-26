"""List suspicious Q/R records and questions with many distinct answers."""

import argparse
from collections import defaultdict
from pathlib import Path

if __package__:
    from .config import CORPUS_MAIN
    from .corpus import (
        _KNOWN_NOISE_PATTERNS,
        _RECORD_PATTERN,
        normalize_text,
        question_group_key,
    )
else:
    from config import CORPUS_MAIN
    from corpus import (
        _KNOWN_NOISE_PATTERNS,
        _RECORD_PATTERN,
        normalize_text,
        question_group_key,
    )


def audit_corpus(path, max_answer_variants=5):
    """Print candidates for manual review without changing the corpus."""
    path = Path(path)
    answers_by_question = defaultdict(set)
    suspicious = []

    with path.open("r", encoding="utf-8-sig") as corpus_file:
        for line_number, raw_line in enumerate(corpus_file, start=1):
            line = raw_line.strip()
            if not line:
                continue
            match = _RECORD_PATTERN.fullmatch(line)
            if match is None:
                suspicious.append((line_number, "format Q/R invalide", line))
                continue

            question = normalize_text(match.group(1))
            answer = normalize_text(match.group(2))
            if not question or not answer:
                suspicious.append((line_number, "question ou réponse vide", line))
                continue
            answers_by_question[question_group_key(question)].add(answer)

            if any(pattern.search(line) for pattern in _KNOWN_NOISE_PATTERNS):
                suspicious.append((line_number, "gabarit/bruit connu", line))
            if "\ufffd" in line or "⁇" in line:
                suspicious.append((line_number, "caractère de remplacement/inconnu", line))
            if answer.endswith(("...", "…")):
                suspicious.append((line_number, "réponse finissant par une ellipse", line))

    print(f"Lignes suspectes : {len(suspicious)}")
    for line_number, reason, line in suspicious:
        print(f"{line_number}: [{reason}] {line}")

    variant_groups = [
        (question, answers)
        for question, answers in answers_by_question.items()
        if len(answers) > max_answer_variants
    ]
    print(
        f"Questions avec plus de {max_answer_variants} réponses distinctes : "
        f"{len(variant_groups)}"
    )
    for question, answers in sorted(variant_groups):
        print(f"{len(answers)} variantes — {question}")
        for answer in sorted(answers):
            print(f"  - {answer}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", default=CORPUS_MAIN, help="Fichier Q/R à auditer")
    parser.add_argument(
        "--max-variants",
        type=int,
        default=5,
        help="Seuil au-delà duquel une question est listée",
    )
    arguments = parser.parse_args(argv)
    if arguments.max_variants < 1:
        parser.error("--max-variants doit être supérieur ou égal à 1")
    audit_corpus(arguments.corpus, arguments.max_variants)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
