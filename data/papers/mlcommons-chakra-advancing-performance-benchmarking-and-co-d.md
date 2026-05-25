---
agentic_models: []
arxiv_url: https://arxiv.org/abs/2305.14516
authors: []
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/mlcommons/chakra
domain:
- observability
- fleet-efficiency
hardware:
- NVIDIA H100
- NVIDIA H200
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Chakra ET adopted across 3+ MLCommons simulators and multiple hardware
  vendors; enables workload replay and co-design without proprietary production traces.
models_evaluated:
- Mixtral-8x22B
- Mixtral-8x7B
observations:
  ai-solves-verifiable: Chakra ETs are deterministic replay-capable traces; this makes
    distributed ML simulation tractable for automated hardware co-design without real
    cluster access.
  avoid-redundant-work: A captured Chakra ET replays across simulated hardware configurations
    without re-running the original training job, amortizing measurement cost across
    the design space.
official_category: ''
openreview_url: https://openreview.net/forum?id=s2WcSv2Hzt
organizations:
- Meta
- NVIDIA
- AMD
- Google
- Georgia Tech
- MLCommons
presentation_type: oral
principles:
- ai-solves-verifiable
- avoid-redundant-work
problem: Without a portable workload format, ML co-design requires specialized hardware
  unavailable to most; optimizations can't be evaluated offline or shared.
project_url: ''
reading_status: want-to-read
research_or_industry: mixed
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3742_UFSQJ36.pdf
slug: mlcommons-chakra-advancing-performance-benchmarking-and-co-d
status: draft
title: 'MLCommons Chakra: Advancing Performance Benchmarking and Co-design using Standardized
  Execution Traces'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3742
---

## Key Contributions

- **Chakra Execution Traces (ET) format**: open, graph-based representation of distributed ML workloads capturing operator execution order, communication dependencies, tensor shapes, and timing metadata — portable across frameworks and hardware platforms and usable for both replay and simulation
- **Trace collection tooling**: instrumentation for JAX, PyTorch, and other frameworks to capture Chakra ETs from production training and inference runs with low overhead; enables workload archival for future hardware co-design studies
- **Cross-platform simulation integration**: adapters connecting Chakra ETs to ML simulators (e.g., ASTRA-sim, Proteus) so new hardware topologies and communication schedules can be evaluated against recorded production workloads without requiring access to original hardware
- Ecosystem adoption: Chakra ET format used across MLCommons benchmarks and by multiple hardware vendors for pre-silicon performance modeling and memory system co-design

## Trade-offs

- Chakra ETs capture execution structure but not dynamic data values; simulation accuracy depends on whether the workload is compute-bound or data-sensitive — variable-length workloads or dynamic control flow may diverge between real execution and replay
- The format is richer than ONNX graphs but requires Chakra-specific tooling to produce and consume; adoption outside the MLCommons ecosystem requires investment in adapters

## Nuances

- The paper does not report concrete performance numbers comparing Chakra-enabled co-design decisions to production outcomes; value is demonstrated through ecosystem adoption rather than direct speedup claims
- Chakra ET fidelity depends on complete instrumentation of all ops; missing operators (e.g., custom CUDA kernels outside standard frameworks) produce incomplete traces that break simulation
- Authors are not listed in the available abstract — this is a community paper with contributions from multiple organizations; specific design decisions may reflect committee consensus rather than a single coherent architecture