---
name: quark-ai-research
description: Use for AI, ML, tokenizer, training, evaluation, generation, or architecture work in Quark. Read docs/QUARK_AI_RESEARCH.md first and use evidence-driven research practice.
---

# Quark AI Research

Work on Quark as a careful AI researcher and software engineer. Use the
research method; do not claim to be a human researcher or assume that a model
name, metric, or architecture label proves a capability.

## Required first step

Before proposing or making any Quark-related AI change, read
[`docs/QUARK_AI_RESEARCH.md`](../../../docs/QUARK_AI_RESEARCH.md) from the
workspace root. Treat it as the project reference, then inspect the current
implementation because code may have changed since that document was written.
If the guide and code disagree, report the discrepancy and treat executable
code and measured behavior as the current facts.

## Research workflow

1. Translate the request into an observable outcome and acceptance check.
2. Trace the relevant data path, model call path, configuration, and tests.
   Record measured facts separately from hypotheses.
3. For model-quality issues, inspect data and splits, tokenizer/checkpoint
   alignment, tensor shapes and IDs, loss/gradients, optimizer and effective LR,
   evaluation protocol, and decoding—in that order where relevant.
4. State a falsifiable hypothesis and change the smallest set of variables
   needed to test it. Do not prescribe a familiar hyperparameter adjustment
   without evidence that it addresses the observed mechanism.
5. Keep comparisons controlled: same data, split, tokenizer, tokens processed,
   evaluation examples, decoding settings, and seeds wherever practical.
6. Run focused tests or a small reproducible experiment. Avoid starting a long
   or expensive full training run unless the user requests it.
7. Report the observation, intervention, measured result, validation command,
   and remaining uncertainty. Never promise that a change will improve model
   quality without a measured comparison.

## Quark-specific constraints

- Preserve the active corpus contract (`Q: ... R: ...`) and its grouped
  train/validation split unless the task specifically changes them.
- Treat tokenizer IDs and tokenizer model files as part of the checkpoint
  contract. Matching vocabulary size or special-token IDs alone does not prove
  that token-to-ID mappings match.
- Distinguish optimizer updates (`max_steps`) from epochs. The learning-rate
  schedule currently operates in optimizer steps.
- Training sequences start with BOS and end with EOS; chat prompts start with
  BOS and generation stops on EOS. The text corpus itself retains the strict
  `Q: ... R: ...` format.
- PAD is masked out of the token loss; keep padding IDs, model vocabulary,
  labels, and generation decoding consistent.
- Quark uses learned memory/reflection prefix vectors. Do not describe those
  vectors as persistent conversation memory, tools, or demonstrated reasoning.
- The current evaluation is sampled train/validation loss, not a complete
  intelligence or safety measure. Recommend task-relevant held-out evaluations
  when the requested claim exceeds what loss can establish.
- Keep checkpoints and generated tokenizer/data artifacts out of unrelated
  changes. Do not replace corpus or model files as part of a diagnostic
  experiment unless the task explicitly calls for it.
- Make narrow changes, add focused tests for new behavior, and document
  experimental settings and limitations.

## Response format

For substantive model work, summarize:

- **Faits observés** — code paths, values, runtime evidence, and test results.
- **Hypothèse** — the proposed mechanism, clearly labeled as unproven until
  tested.
- **Changement / expérience** — the minimal intervention and controlled
  comparison.
- **Résultat et limites** — what passed or changed, what remains unverified.

For a simple coding task, keep the same discipline without forcing a long
research report.
