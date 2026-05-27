---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
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
key_results: Closed-form framework for sparing at Meta 10,000+ GPU LLM clusters; 3
  parameters (block size, spare count, GPU trays) optimized via simulation
models_evaluated: []
observations:
  balance: Sparing configuration (block size, spare count, GPU trays) determines replacement
    speed; under-sparing causes training downtime while over-sparing wastes GPU capacity.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=18jPgte2tM
organizations:
- Meta
presentation_type: oral
principles:
- balance
problem: Selecting optimal sparing (block size, spare count, GPU trays) for LLM training
  clusters is complex and directly impacts fault tolerance and training goodput.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3862_xkbT8SW.pdf
slug: sparing-strategies-to-minimize-reliability-impact-on-large-t
status: draft
title: Sparing Strategies to Minimize Reliability Impact On Large Training Jobs
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3862
---

## Background

At 10,000+ GPU scale, hardware failures are daily events, not exceptions. When a GPU fails mid-run, the training job stalls until hardware is replaced. Sparing pre-provisions spare GPU nodes or trays for hot-swap, but the configuration space — compute block size, spare count, spare tray count — is non-trivial: over-spare and you waste GPUs sitting idle; under-spare and jobs wait hours for replacement hardware.

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