---
agentic_models: []
arxiv_date: 2025-02
arxiv_url: https://arxiv.org/abs/2502.06982
authors:
- Arissa Wongpanich
- Tayo Oguntebi
- Jose Baiocchi Paredes
- Yu Wang
- Phitchaya Phothilimthana
- Ritwika Mitra
- Zongwei Zhou
- Naveen Kumar
- Vijay Janapa Reddi
award: ''
citations: 8
citations_updated: '2026-05-24'
code_url: ''
date: '2026-05-21'
domain:
- fleet-efficiency
- observability
hardware:
- TPU
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: MPG metric decomposes fleet waste into scheduling (>95% optimal), runtime,
  and program components; comm-compute overlap yields 1.38× throughput and 72% FLOPS
  on 1024 TPUs for 500B-param model
models_evaluated: []
observations:
  balance-utilization: MPG reveals that runtime goodput gaps (crashes, restarts, checkpointing
    overhead) rather than scheduling or hardware utilization are the dominant efficiency
    bottleneck in Google's production TPU fleet
  overlap-independent-work: Comm-compute overlap in production 500B-param training
    reached 72% FLOPS utilization on 1024 TPUs, a 1.38× improvement, validating that
    this technique is the highest-leverage program goodput lever
official_category: Research Papers
openreview_url: https://openreview.net/forum?id=y31QSL9yMG
organizations:
- Google
presentation_type: oral
principles:
- balance-utilization
- overlap-independent-work
problem: Traditional hardware utilization metrics like MFU cannot identify whether
  TPU fleet inefficiency comes from scheduling, runtime failures, or program inefficiency,
  making improvements non-actionable.
project_url: ''
reading_status: read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3734_ahO01yG.pdf
slug: ml-fleet-tpu-goodput
status: draft
title: 'Machine Learning Fleet Efficiency: Improving TPU Systems at Scale with ML
  Productivity Goodput'
topics:
- communication-overlap
- pipeline-parallelism
venue_url: https://mlsys.org/virtual/2026/oral/3734
---


## Key Contributions

- **ML Productivity Goodput (MPG) metric**: decomposes overall fleet efficiency into three multiplicative components — Scheduling Goodput (resource availability), Runtime Goodput (forward progress vs. failures/overhead), and Program Goodput (actual vs. roofline compute utilization)
- **Production fleet analysis**: applied MPG to Google's TPU fleet across thousands of accelerators; scheduling goodput already exceeds 95%, making runtime and program goodput the actionable levers
- **Communication-compute overlap deployment**: validated that overlapping collectives with compute achieves 1.38× throughput improvement and 72% FLOPS utilization on 1024 TPUs training a 500B-parameter language model
- **Compiler optimization accounting**: framework for attributing MPG changes to XLA algebraic simplifications across the top 150 fleet workloads, enabling cost-benefit analysis of compiler passes

## Trade-offs

- MPG requires access to job traces, hardware telemetry, and compiler profiles simultaneously; this data infrastructure exists at Google but is not available in most other organizations
- Program Goodput uses a roofline model as the ideal baseline, which may be overly optimistic for irregular workloads (sparse models, variable sequence lengths) where the roofline is not achievable

## Nuances

- Scheduling goodput being >95% optimal means further fleet wins must come from runtime or program efficiency, but these require changing framework internals or model architecture — much harder than scheduling tweaks
- Runtime goodput for serving workloads is consistently lower than training workloads in the fleet; the paper does not fully explain this gap, suggesting uncharacterized failure modes specific to inference
- The MPG framework is described at a level that would be difficult to reproduce outside Google; the metric definition is principled but the paper does not release the measurement tooling