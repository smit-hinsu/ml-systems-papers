---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Kasper Overgaard Mortensen
- Ama Bembua Bainson
- Mathias Ravn Tversted
- "Kristoffer Strube Græm"
- Renata Borovica-Gajic
- Andrea Paudice
- Davide Mottin
- Panagiotis Karras
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- fleet-efficiency
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: QBL achieves O(m log k) per-iteration complexity and consistently outperforms
  existing methods in both time and solution quality on state-of-the-art benchmarks
models_evaluated: []
observations:
  balance: QBL's priority queue limits update operations to the top-m
    arms at each step, keeping per-iteration work O(m log k) instead of O(k) and
    preventing the compute from scaling linearly with the arm count.
  cache: Constant sampling overhead and limited update operations
    via a priority queue avoid re-evaluating all arms each iteration; only the arms
    needed for the next decision are touched.
official_category: ''
openreview_url: https://openreview.net/forum?id=lfHvcstuo2
organizations:
- Aarhus University
- University of Southern Denmark
- University of Melbourne
presentation_type: oral
principles:
- balance
- cache
problem: Adversarial multi-armed bandit algorithms with many arms have O(k) per-iteration
  cost, making them impractical for large-arm-count settings like database physical
  design tuning.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: practical-adversarial-multi-armed-bandits-with-sublinear-run
status: draft
title: Practical Adversarial Multi-Armed Bandits with Sublinear Runtime
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3762
---

## Key Contributions

- **Queuing Behind the Leader (QBL)**: adversarial multi-armed bandit algorithm achieving O(m log k) per-iteration complexity using a priority queue to limit update scope to the m selected arms per step, avoiding full O(k) arm re-evaluation
- **Constant sampling overhead**: exploration strategy maintains a fixed overhead per step regardless of arm count, enabling practical deployment at arm counts where prior methods become computationally intractable
- **Balanced exploration**: combines limited updates with a principled exploration mechanism that maintains regret guarantees in nonstationary adversarial environments where the optimal arm changes over time
- Consistently outperforms existing methods in both wall-clock time and solution quality on state-of-the-art benchmarks; applied to physical design tuning in database systems

## Trade-offs

- The O(m log k) bound assumes the priority queue is maintained incrementally; initial construction of the queue requires O(k) time, so the benefit is amortized over many iterations.
- Regret guarantees may differ from full O(k) algorithms in adversarial settings with very high arm churn; the exploration-exploitation balance is calibrated for the database tuning application.
