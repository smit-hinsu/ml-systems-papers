---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Justin Bauer
- Thomas Walshe
- Derek Pham
- Harit Vishwakarma
- Armin Parchami
- Frederic Sala
- Paroma Varma
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- rl-training
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Mixed-complexity RLVR datasets yield 5× sample efficiency vs. easy-only
  training for SLMs on counting, graph, and spatial reasoning in low-data regimes
models_evaluated:
- Small Language Models (SLMs)
observations:
  balance: Training on mixed-complexity tasks prevents trivial (easy-only) and intractable
    (hard-only) examples from dominating the curriculum, keeping learning signal dense
    throughout low-data training.
  search-ai: Procedurally generated datasets with controllable complexity and verifiable
    answers let RLVR train on objectively checkable problems, enabling scaling law
    studies without human annotation.
official_category: ''
openreview_url: https://openreview.net/forum?id=fV4t4kYvgi
organizations:
- Snorkel AI
- University of Wisconsin-Madison
presentation_type: oral
principles:
- search-ai
- balance
problem: RLVR post-training requires large annotated datasets with ground-truth answers;
  applying it effectively in low-data, low-compute regimes is unsolved.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3783.pdf
slug: learning-from-less-measuring-the-effectiveness-of-rlvr-in-lo
status: draft
title: 'Learning from Less: Measuring the Effectiveness of RLVR in Low Data and Compute
  Regimes'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3783
---

## Background

RLVR fine-tunes LLMs on problems with objectively checkable answers (math, code, puzzles), using pass/fail as the reward signal. It has shown strong results at frontier scale, but those runs assume large annotated datasets and thousands of GPU-days. For sub-7B models with single-GPU budgets, whether RLVR produces real capability gains — and which dataset properties matter — was an open empirical question.

## Key Contributions

- **Procedural dataset framework**: Three novel procedurally generated datasets (number counting, graph reasoning, spatial reasoning) with controllable size, diversity, and complexity provide fine-grained benchmarks for RLVR data scaling studies.
- **Low-complexity-to-high generalization**: Models trained on simpler RLVR tasks consistently generalize to harder tasks of the same type, enabling cheap-to-generate easy examples as a lever for harder-task performance.
- **Mixed-complexity sample efficiency**: Training on datasets mixing easy, medium, and hard examples delivers up to 5× sample efficiency over easy-only training in low-data regimes, identifying curriculum design as a key data efficiency lever.

## Trade-offs

- Results are limited to procedurally generated tasks (counting, graph, spatial); generalization of the findings to open-ended reasoning tasks with natural language ground truth is unclear.
- The 5× sample efficiency advantage applies specifically to low-data regimes; at large data scales the benefit over easy-only training may diminish.

## Nuances

- The study focuses on small language models, not frontier LLMs; the discovered data scaling laws may not hold at larger parameter counts where capacity becomes less of a constraint.
- Procedural data generators provide controlled properties but may not capture the distribution of real-world RLVR fine-tuning tasks practitioners care about.