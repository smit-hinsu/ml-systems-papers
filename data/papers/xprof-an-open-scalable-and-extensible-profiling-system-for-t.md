---
agentic_models: []
arxiv_url: ''
authors:
- Robert Hundt
- Naveen Kumar
- Jose Baiocchi Paredes
- Scott Goodson
- Clive Verghese
- Prasanna Rengasamy
- Kelvin Le
- Jiya Zhang
- Charles Alaras
- Yin Zhang
- Kan Cai
- Jiten Thakkar
- Sai Ganesh Bandiatmakuri
- Yogesh SY
- Ani Udipi
- Vikas Agarwal
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/openxla/xprof
date: 2026-05
domain:
- observability
- fleet-efficiency
hardware:
- TPU
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: XProf profiles thousands of chips at <1% overhead with <7µs snapshots;
  adopted by third-party vendors; used in MLPerf-winning Google submissions.
models_evaluated: []
observations:
  ai-solves-verifiable: LLO Bundle Visualization exposes clock-cycle execution times
    per MXU pipeline stage — verifiable ground-truth feedback for compiler optimization
    without manual hardware analysis.
  balance-utilization: Utilization Viewer converts raw MXU bus activity counters into
    compute-bound vs. memory-bound diagnoses (e.g., 7.3% utilization), making load
    imbalance visible without hardware expertise.
official_category: ''
openreview_url: https://openreview.net/forum?id=KqRLAdGK6C
organizations:
- Google
presentation_type: oral
principles:
- balance-utilization
- ai-solves-verifiable
problem: Optimizing ML across thousands of TPUs requires deep hardware expertise;
  profilers surface raw metrics but not actionable full-stack optimization guidance.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3827.pdf
slug: xprof-an-open-scalable-and-extensible-profiling-system-for-t
status: draft
title: 'XProf: An Open, Scalable, and Extensible Profiling System for the Modern ML
  Stack'
topics:
- autotuning
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3827
---

## Key Contributions

- **Continuous Profiling Snapshots**: always-on flight recorder using a 2GB host-side circular buffer retaining ~90 seconds of performance data; captures anomalies programmatically with <7µs per packet overhead, enabling post-hoc analysis of transient failures without manual re-triggering
- **Utilization Viewer**: translates raw hardware performance counters (MXU bus activity, HBM bandwidth, SparseCore utilization) into actionable utilization percentages, automatically classifying models as compute-bound or memory-bound without requiring user hardware expertise
- **LLO Bundle Visualization**: exposes Low-Level Operations bundle data at machine-instruction granularity, providing exact execution times and block utilization metrics per MXU pipeline stage to identify idle cycles in matrix multiplication pipelines
- **Hardware-agnostic PJRT C API extension**: pluggable architecture that has been adopted by third-party accelerator vendors, extending XProf's analysis to non-Google hardware within the OpenXLA ecosystem
- Full-stack host+device visibility across TensorCore, SparseCore, HBM, and MXU; distributed monitoring of thousands of chips with <1% workload overhead; open-sourced at github.com/openxla/xprof

## Nuances

- XProf's optimization suggestions are heuristic and hardware-specific to Google's TPU generations; actionable guidance for GPU workloads or third-party accelerators may be less precise
- The <1% overhead claim applies to the continuous profiling mode; full trace collection (used for detailed analysis) has higher overhead not quantified in the abstract
- "Winning MLPerf submissions" is cited as evidence of impact but the connection between XProf insights and submission improvements is not quantified — it is plausible that other optimizations drove the gains
- The tool is primarily designed for JAX/OpenXLA workloads; PyTorch or TensorFlow users on TPUs would need framework adaptation