---
agentic_models: []
arxiv_url: ''
authors:
- Jianshu She
- Zonghang Li
- HONGCHAO DU
- Shangyu Wu
- Wenhao Zheng
- Eric Xing
- Zhengzhong Liu
- Huaxiu Yao
- Chun Jason Xue
- Qirong Ho
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: PLA-Serve reduces TTFT latency by adaptively disaggregating requests
  by prompt-length group; specific latency numbers require reading the full paper.
models_evaluated: []
observations:
  balance-utilization: Mixing short and long prompts in the same prefill batch creates
    GPU utilization imbalance — short prompts finish early and leave compute idle while
    the batch waits for the longest prompt; disaggregating by length group keeps per-batch
    work homogeneous.
  avoid-redundant-work: Prefix caching is more effective when requests with shared
    prefixes are routed to the same instance; length-aware routing increases the probability
    that matched-length requests share cached prefixes, improving hit rates.
official_category: ''
openreview_url: https://openreview.net/forum?id=dzjCkSEDyG
organizations:
- Carnegie Mellon University
- University of Illinois Urbana-Champaign
presentation_type: oral
principles:
- balance-utilization
- avoid-redundant-work
problem: Unified prefill scheduling in LLM serving ignores prompt-length heterogeneity
  — batching short and long prompts together causes head-of-line blocking and GPU
  underutilization, inflating TTFT for short requests.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3787_G7LPmPu.pdf
slug: pla-serve-a-prefill-length-aware-llm-serving-system
status: draft
title: 'PLA-Serve: A Prefill-Length-Aware LLM Serving System'
topics:
- continuous-batching
- kv-cache
- prefix-caching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3787
---

## Key Contributions

- **Length-Aware Prefill Serving (LAPS)**: classifies incoming requests into prompt-length groups and routes each group to dedicated prefill workers, ensuring that each prefill batch contains requests with similar lengths — eliminating the head-of-line blocking that mixed-length batching causes
- **Adaptive scheduling strategy**: dynamically adjusts length-group boundaries and worker allocation in response to workload shifts, preventing resource starvation when request length distributions change over time
- **Prefix-cache-aware routing**: routes requests to workers that have cached prefixes from the same length group, increasing prefix-cache hit rates by exploiting the correlation between request length and shared system prompt structure

## Trade-offs

- Disaggregating by length group increases the number of distinct prefill worker pools, raising system complexity and potentially stranding capacity in low-traffic length groups
- Length-based routing may conflict with prefix-cache locality: a request could belong to a length group whose worker does not hold the most relevant cached prefix

## Nuances

- Specific latency improvement numbers and hardware configurations are not available from the abstract alone; the effectiveness of length disaggregation depends heavily on the prompt-length distribution of the target workload
- The adaptive boundary adjustment mechanism's overhead and convergence behavior under rapidly shifting workloads are not characterized in the available abstract
- The paper assumes a request router with knowledge of prompt length at admission time; workloads where prompt length is unknown until parsing (e.g., multi-turn conversations with accumulated context) require length estimation
