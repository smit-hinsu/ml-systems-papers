---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Fumikazu KONISHI
- Yuuki Tsubouchi
- Hirofumi Tsuruta
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- fleet-efficiency
- observability
hardware:
- H100
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 33.95 PFLOP/s HPL on 100×H100 nodes; top-49 ISC 2025 via open 800 GbE
  SONiC; workload shifts from large-scale to mid-scale jobs as project matures.
models_evaluated: []
observations:
  balance: Single-tenant cluster shows use shifting from large to mid-scale jobs as
    the project matures; few large jobs account for most GPU time while small jobs
    dominate count — classic HPC pattern.
  measure: Published GPU cluster traces come from multi-tenant clouds where many teams'
    jobs mix; how one LLM project's demand shifts over its lifetime had never been
    watched in isolation.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=n7o6C3p3wk
organizations:
- SAKURA Internet Research Center
presentation_type: oral
principles:
- balance
- measure
problem: Characterizing real-world GPU cluster utilization under a single unified
  LLM development project to understand workload dynamics at scale.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3758_d2pso2Y.pdf
slug: sakuraone-an-open-ethernetbased-ai-hpc-system-and-its-observ
status: draft
title: 'SAKURAONE: An Open Ethernet–Based AI HPC System and Its Observed Workload
  Dynamics in a Single-Tenant LLM Development Environment'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3758
---

## Key Contributions

- **SAKURAONE system design**: 100-node HPC cluster with 8 NVIDIA H100 GPUs per node, 2 PB all-flash Lustre storage, interconnected via rail-optimized 800 GbE leaf-spine fabric with RoCEv2 — the only top-100 ISC 2025 system using a fully open networking stack (SONiC)
- **Open networking validation**: achieves 33.95 PFLOP/s HPL Rmax, 339.86 PFLOP/s HPL-MxP (FP8), and 396.295 TFLOP/s HPCG on vendor-neutral 800 GbE, demonstrating Ethernet scalability for AI HPC
- **Single-tenant workload characterization**: exclusive use by a single LLM research project enables clean observation of utilization dynamics; confirms that small jobs dominate count while few large jobs consume most GPU time
- **Project lifecycle observation**: resource use transitions from large-scale training to mid-scale iterative refinement jobs as the project progresses, providing empirical data on LLM development patterns

## Findings

- Small-scale jobs dominated job count; a few large-scale jobs accounted for most GPU resource time — consistent with prior HPC studies.
- As the single-tenant project progressed from initial large-scale training to iterative refinement, average job size shifted from large to mid-scale.
- Open networking (800 GbE SONiC) achieves competitive HPC benchmarks without proprietary interconnect, suggesting it as a viable alternative to InfiniBand for AI workloads.

## Nuances

- Observations are from a single project over a limited time window; generalizing workload dynamics to multi-tenant environments or different project types requires caution.
- Performance figures (HPL, HPCG) reflect system hardware capabilities; real-world LLM training throughput depends on model and parallelism strategy.