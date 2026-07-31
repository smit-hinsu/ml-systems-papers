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
domain:
- fleet-efficiency
- observability
hardware:
- TPU
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: MPG decomposes fleet waste into scheduling, runtime, and program layers;
  comm-compute overlap achieves 1.38× throughput at 72% FLOPS on 1024 TPUs.
models_evaluated: []
observations:
  balance: Scheduling goodput (>95% in Google's fleet) proves work allocation
    is balanced; unequal utilization at the program and runtime layers — not job scheduling
    — is where compute actually goes to waste.
  pipeline: Comm-compute overlap in production 500B-param training
    reached 72% FLOPS utilization on 1024 TPUs, a 1.38× improvement, validating that
    this technique is the highest-leverage program goodput lever
official_category: Research Papers
optimization_type: []
openreview_url: https://openreview.net/forum?id=y31QSL9yMG
organizations:
- Google
presentation_type: oral
principles:
- balance
- pipeline
problem: MFU cannot separate whether TPU fleet inefficiency comes from scheduling,
  runtime failures, or program inefficiency, making optimization non-actionable.
project_url: ''
reading_status: read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3734_ahO01yG.pdf
slug: ml-fleet-tpu-goodput
status: under-review
title: 'Machine Learning Fleet Efficiency: Improving TPU Systems at Scale with ML
  Productivity Goodput'
topics:
- communication-overlap
- pipeline-parallelism
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3734
---

## Key Contributions

- **ML Productivity Goodput (MPG) metric**: decomposes overall fleet efficiency into three multiplicative components — Scheduling Goodput (resource availability), Runtime Goodput (forward progress vs. failures/overhead), and Program Goodput (actual vs. roofline compute utilization)
- **Production fleet analysis**: applied MPG to Google's TPU fleet across thousands of accelerators; scheduling goodput already exceeds 95%, making runtime and program goodput the actionable levers
- **Communication-compute overlap deployment**: validated that overlapping collectives with compute achieves 1.38× throughput improvement and 72% FLOPS utilization on 1024 TPUs training a 500B-parameter language model
- **Compiler optimization accounting**: framework for attributing MPG changes to XLA algebraic simplifications across the top 150 fleet workloads, enabling cost-benefit analysis of compiler passes

## Findings

- Scheduling goodput in Google's TPU fleet exceeds 95%, meaning resource availability is near-optimal and not the limiting factor; runtime and program efficiency are the actionable levers.
- Runtime goodput losses — job crashes, checkpoint/restart overhead, and stall recovery — account for more fleet waste than scheduling or hardware utilization gaps combined.
- Serving workloads show consistently lower runtime goodput than training workloads; the gap is observed fleet-wide but its specific failure modes are not fully characterized.
- Comm-compute overlap for a 500B-parameter model on 1024 TPUs achieves 72% FLOPS utilization, a 1.38× throughput improvement — the largest single program goodput gain measured in the fleet study.
- XLA algebraic simplifications across the top 150 fleet workloads produce measurable program goodput improvements that the MPG framework can attribute per compiler pass, enabling cost-benefit analysis of optimization decisions.

## Trade-offs

- MPG requires access to job traces, hardware telemetry, and compiler profiles simultaneously; this data infrastructure exists at Google but is not available in most other organizations
- Program Goodput uses a roofline model as the ideal baseline, which may be overly optimistic for irregular workloads (sparse models, variable sequence lengths) where the roofline is not achievable

## Nuances

- Scheduling goodput being >95% optimal means further fleet wins must come from runtime or program efficiency, but these require changing framework internals or model architecture — much harder than scheduling tweaks
- Runtime goodput for serving workloads is consistently lower than training workloads in the fleet; the paper does not fully explain this gap, suggesting uncharacterized failure modes specific to inference
- The MPG framework is described at a level that would be difficult to reproduce outside Google; the metric definition is principled but the paper does not release the measurement tooling