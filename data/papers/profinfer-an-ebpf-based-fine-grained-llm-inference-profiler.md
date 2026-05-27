---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
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
  of LLM inference with MoE routing and offloading patterns on llama.cpp
models_evaluated: []
observations: {}
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=tYHWS7YPof
organizations:
- Huawei
- Technical University of Munich
presentation_type: oral
principles: []
problem: Edge LLM inference engines have no operator-level profiling; developers cannot
  identify memory-bound vs. compute-bound bottlenecks without source modifications.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3740_fDdgYfm.pdf
slug: profinfer-an-ebpf-based-fine-grained-llm-inference-profiler
status: draft
title: 'ProfInfer: An eBPF-based Fine-Grained LLM Inference Profiler'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3740
---

## Background

eBPF lets you attach lightweight tracing programs to kernel and userspace events without recompiling the target process. Edge LLM inference engines like llama.cpp run on devices with no GPU vendor profiling tools, and behaviors like MoE routing (dynamically selecting expert layers) and CPU offloading (moving KV pages to RAM under pressure) are invisible to coarse-grained timers. Without operator-level visibility, developers can't distinguish compute-bound from memory-bandwidth-bound slowdowns.

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