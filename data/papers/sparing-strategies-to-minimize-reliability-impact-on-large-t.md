---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Kevin Quirk
- Matthew Lennie
- Ehsan K. Ardestani
- Satyajeet Singh Ahuja
- Matthew Bergeron
- Andrew Grier
- Zhaodong Wang
- Mustafa Ozdal
- Xu Zhang
- Abhinav Triguna
- Ying Zhang
- Mathew Oldham
- Chunqiang Tang
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- fleet-efficiency
- llm-training
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Analytical closed-form framework optimizes sparing strategy for Meta's
  hyperscale LLM training clusters; simulation validates model and guides production
  sparing decisions.
models_evaluated: []
observations:
  balance: Sparing strategy (block size, spare count, spare GPU trays)
    directly determines how quickly failed components can be replaced, controlling
    the imbalance between active and spare compute; under-sparing causes long downtime
    while over-sparing wastes resources.
  cache: Pre-allocating the right number of spare compute blocks minimizes
    recomputation from checkpoint rollback by reducing mean time-to-recovery for hardware
    failures during LLM training.
official_category: ''
openreview_url: https://openreview.net/forum?id=18jPgte2tM
organizations:
- Meta
presentation_type: oral
principles:
- balance
- cache
problem: Choosing the optimal sparing strategy (block size, spare count, spare GPU
  trays) for LLM training clusters is complex and directly impacts fault tolerance
  and goodput.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: ''
slug: sparing-strategies-to-minimize-reliability-impact-on-large-t
status: draft
title: Sparing Strategies to Minimize Reliability Impact On Large Training Jobs
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3862
---

## Key Contributions

- **Analytical sparing framework**: closed-form expressions to guide sparing strategy decisions including compute block size, number of spare blocks, and spare GPU trays; enables first-order recommendations without exhaustive simulation
- **Simulation validation component**: cross-validates the analytical model against simulated cluster behavior; provides confidence in recommendations for configurations not yet deployed in production
- **Production deployment at Meta**: framework applied to Meta's hyperscale AI training infrastructure; helps engineers optimize fault tolerance, minimize downtime, and maximize goodput during LLM training
- First principled analysis of sparing strategy trade-offs in the context of large-scale LLM training job reliability

## Findings

- Sparing strategy (block size, spare count) is a key lever for controlling training job availability and goodput; over-sparing wastes resources while under-sparing leads to extended downtime.
- Closed-form analytical model provides practical first-order guidance, validated by simulation for production-scale configurations.

## Trade-offs

- Analytical model assumes simplified failure distributions; real hardware exhibits correlated and bursty failures that may deviate from model assumptions.
- Optimal sparing is cluster-topology specific; results for Meta's infrastructure may not directly generalize to different interconnect or hardware architectures.

## Nuances

- The paper provides framework and methodology rather than a universally optimal sparing ratio; practitioners need to parameterize the model with their specific hardware failure rates.
- Spare GPU tray granularity is a practical consideration tied to physical rack and power topology; the framework must account for physical infrastructure constraints.
