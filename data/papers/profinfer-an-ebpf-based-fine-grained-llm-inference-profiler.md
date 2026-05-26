---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Bohua Zou
- Debayan Roy
- Dhimankumar Yogesh Airao
- Weihao Xu
- Binqi Sun
- Yutao Liu
- Haibo Chen
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- observability
hardware:
- Edge devices (llama.cpp)
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Less than 4% runtime overhead while providing operator-level profiling
  of LLM inference including MoE routing and operator offloading patterns on edge
  devices running llama.cpp
models_evaluated: []
observations:
  cache: eBPF dynamic probe attachment avoids modifying or recompiling
    LLM inference engine source code; probes attach to already-running binaries,
    eliminating the need to rebuild instrumented versions for each profiling session.
  balance: ProfInfer's hardware counter trend visualization reveals whether
    a workload is memory-bound or compute-bound per operator, enabling developers to
    direct optimization effort to actual bottlenecks rather than guessing.
official_category: ''
openreview_url: https://openreview.net/forum?id=tYHWS7YPof
organizations:
- Huawei
- Technical University of Munich
presentation_type: oral
principles:
- cache
- balance
problem: LLM inference engines on edge devices offer no operator-level visibility,
  leaving developers unable to identify whether workloads are memory-bound or compute-bound
  without modifying or recompiling the engine.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: ''
slug: profinfer-an-ebpf-based-fine-grained-llm-inference-profiler
status: draft
title: 'ProfInfer: An eBPF-based Fine-Grained LLM Inference Profiler'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3740
---

## Key Contributions

- **Non-intrusive eBPF profiling**: ProfInfer dynamically attaches eBPF probes to runtime functions across multiple inference engine layers without modifying or recompiling source, making it deployable on production llama.cpp instances.
- **Multi-layer trace collection**: Probes span operator execution, graph scheduling, and hardware counter layers, producing rich visualizations of operator timelines, computation graphs, and memory-vs-compute bottleneck trends.
- **MoE and offloading visibility**: Specifically captures MoE routing decisions and operator offloading behavior, two critical but previously opaque patterns in edge LLM inference.

## Trade-offs

- eBPF probes are kernel-mediated and require root or CAP_BPF privileges; deployments on locked-down edge devices may not have the necessary permissions.
- The framework is validated on llama.cpp; applicability to other edge runtimes (e.g., MLC-LLM, ExecuTorch) requires re-implementing probe attachment points for each runtime's internal APIs.

## Nuances

- The <4% overhead claim is for steady-state profiling; initial probe attachment may cause momentary latency spikes that affect the first few inference requests.
- Visualization quality depends on trace density; sparse workloads (few operators) provide less actionable information than dense multi-layer inference pipelines.
