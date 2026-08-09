---
agentic_models: []
arxiv_url: ''
authors:
- Ignacio Cano
- Yu Wang
- Mike Burrows
- Ziqiang Feng
- Matheus Camargo
- Chao Wang
- David Liu
- Tengyu Sun
- Alexander Wertheim
- Arissa Wongpanich
- Christof Angermueller
- Hyojun Kim
- Wenqi Cao
- Aleksey Orekhov
- Amit Sabne
- Emma Sevastian
- Mehrdad Khani
- Karthik Murthy
- Berkin Ilbeyi
- Subhankar Shah
- Ryan Lefever
- Arjun Khare
- Ankit Sinha
- Peter Ma
- Matt Bierbaum
- Jeremiah Wilke
- Emily Donahue
- Sami Abu-El-Haija
- Nikhil Sarda
- Vineetha Govindaraj
- Shobha Vasudevan
- Kirill Gugaev
- Idan Nachman
- Jie Sun
- Jose Baiocchi Paredes
- Samrat Ghosh
- Domagoj Babic
- Zongwei Zhou
- Naveen Kumar
- Phitchaya Phothilimthana
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- ml-compilers
- llm-training
hardware:
- Google TPU (fleet)
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: CATWILD covers a large fraction of Google's TPU training fleet; specific
  chip-savings % not disclosed, but 5+ years in production at datacenter scale.
models_evaluated: []
observations:
  search-ai: XLA compilation quality is directly measurable via execution
    time on real hardware, making automated search tractable where human experts cannot
    cover the combinatorial tiling/fusion/layout space.
  cache: Fleet jobs re-run the same handful of model architectures for months, so
    most tuning searches would pay again for a configuration another job already
    found.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=hB3nov3gIP
organizations:
- Google
presentation_type: oral
principles:
- search-ai
- cache
problem: XLA heuristics leave performance on the table; manually tuning tiling, fusion,
  and layout for diverse TPU workloads is infeasible at fleet scale.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: ''
slug: catwild-compiler-autotuning-for-tpu-workloads-in-the-wild
status: draft
title: 'CATWILD: Compiler Autotuning for TPU Workloads in the Wild'
topics:
- autotuning
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3774
---

## Key Contributions

- **CATWILD system**: First ML compiler autotuning system deployed at datacenter scale, automatically searching over XLA compiler parameters (tiling factors, fusion strategies, memory layout) for diverse TPU training workloads without requiring human expert intervention.
- **Fleet-scale tuning pipeline**: Orchestrates measurement jobs across Google's TPU fleet to evaluate candidate configurations, building a growing corpus of tuned configurations that cover a large fraction of production training jobs.
- **Workload-aware configuration reuse**: Identifies structurally equivalent or similar computation graphs to reuse previously tuned configurations, amortizing search cost across jobs sharing the same model architecture.
- Five years of production operational experience documented, including lessons on handling workload diversity, TPU generation changes, and configuration staleness.

## Trade-offs

- Autotuning requires executing candidate configurations on real hardware, incurring non-trivial tuning overhead before a job begins benefiting; short-lived jobs may not amortize the search cost.
- Configuration quality is bounded by the search budget; jobs with unusual computation patterns outside the tuned distribution may see smaller gains.

## Nuances

- Specific chip-savings percentages are not disclosed in the paper, making it hard to independently assess magnitude versus the XLA graph-level autotuner baseline (which achieved 10–20% speedup in earlier Google work).
- The system covers training workloads; inference-time compilation (where latency sensitivity is higher and job durations are shorter) is not characterized.
- Configuration staleness as models evolve between training runs requires periodic re-tuning; the triggering policy and its overhead are part of the operational complexity not fully described in the abstract.