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
hardware:
- TPU
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: ML Productivity Goodput (MPG) decomposes fleet efficiency into scheduling,
  runtime, and program components; identifies actionable optimization opportunities
  in Google's production TPU fleet
models_evaluated: []
principles:
- straggler-bubbles
official_category: Research Papers
openreview_url: https://openreview.net/forum?id=y31QSL9yMG
organizations:
- Google
presentation_type: oral
problem: Measuring and improving ML fleet efficiency across a large heterogeneous
  TPU cluster lacks a principled unified metric.
project_url: ''
status: draft
reading_status: read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3734_ahO01yG.pdf
slug: ml-fleet-tpu-goodput
title: 'Machine Learning Fleet Efficiency: Improving TPU Systems at Scale with ML
  Productivity Goodput'
topics: []
venue_url: https://mlsys.org/virtual/2026/oral/3734
---

## Summary

This paper addresses a surprisingly difficult problem: how do you measure whether a fleet of thousands of TPUs is being used well? Existing metrics like MFU (Model FLOP Utilization) capture hardware efficiency but miss higher-level inefficiencies. The authors introduce **ML Productivity Goodput (MPG)**, a new metric that hierarchically decomposes fleet efficiency into three components:

1. **Scheduling goodput**: Are jobs running on available hardware promptly?
2. **Runtime goodput**: When running, is the job making forward progress (vs. crashing, restarting)?
3. **Program goodput**: Is the running program efficiently using the hardware (MFU-style)?

This decomposition makes it actionable — each component points to a different team and fix. Applied to Google's production TPU fleet, MPG identified concrete opportunities: scheduling improvements, framework modernization, and compiler optimizations.

## Key Contributions

- ML Productivity Goodput (MPG) metric with a three-level decomposition
- Production-scale analysis of Google's TPU fleet using MPG
- Identification of which efficiency gaps are largest and most fixable

## Method

MPG is defined recursively: overall goodput = scheduling × runtime × program goodput. Data is collected from production job traces, hardware telemetry, and compiler profiles. The paper validates that improvements in each component measurably increase MPG.

## Limitations

- Metric design reflects Google's specific infrastructure; generalizability to other cluster configs is unclear
- Some components of MPG require internal telemetry that may not be available outside Google

## Personal Notes

<!-- Add your own observations, questions, and connections to other work here -->