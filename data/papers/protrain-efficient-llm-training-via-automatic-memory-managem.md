---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Hanmei Yang
- Jin Zhou
- Yao Fu
- Xiaoqun Wang
- Ramine Roane
- Hui Guan
- Tongping Liu
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-training
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 1.43x–2.71x training throughput improvement over manual-tuned training
  systems via automated memory management without accuracy loss.
models_evaluated: []
observations:
  balance: ProTrain's cost models estimate latency, memory, and I/O bandwidth precisely
    to find configurations that avoid memory pressure while keeping GPU utilization
    high, eliminating manual misconfiguration.
  recompute: ProTrain auto-selects activation checkpoint granularity using cost models
    that weigh memory savings against recomputation overhead; the planner finds the
    optimal schedule without manual search.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=XDkOn0iTiH
organizations:
- University of Massachusetts Amherst
presentation_type: oral
principles:
- balance
- recompute
problem: LLM training memory-saving techniques expose low-level knobs requiring manual
  tuning; misconfiguration causes suboptimal hardware utilization or OOM failures.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3800_lv912MR.pdf
slug: protrain-efficient-llm-training-via-automatic-memory-managem
status: draft
title: 'ProTrain: Efficient LLM Training via Automatic Memory Management'
topics:
- cpu-offload
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3800
---

## Background

LLM training requires fitting activations, gradients, optimizer states, and weights simultaneously in GPU memory. Techniques like activation checkpointing (recompute instead of store), CPU offloading, and gradient accumulation each reduce memory pressure but add compute or I/O overhead. Choosing the right combination and granularity depends on model, batch size, and hardware — and is currently configured by hand, with expert engineers still routinely misconfiguring it.

## Key Contributions

- **Automated memory management abstraction**: collapses complex memory management strategies (activation checkpointing, offloading, recomputation) into a small set of tunable configuration parameters, removing the need for expert-level manual tuning
- **High-fidelity cost models**: runtime profiler provides precise estimates of latency, memory usage, and I/O bandwidth to build cost models that guide configuration search without exhaustive empirical trial
- **Configuration search**: uses cost models to find optimal parameter settings for a given model architecture and hardware; does not alter training algorithm so convergence is unaffected
- Achieves 1.43×–2.71× throughput improvement over state-of-the-art training systems across evaluated LLM workloads

## Trade-offs

- Cost model accuracy depends on hardware characterization; new GPU architectures or interconnects require re-profiling to maintain search quality.
- The abstraction layer covers a finite set of strategies; novel memory-saving techniques introduced after the system is built require extending the parameter space.

## Nuances

- Throughput improvement range (1.43×–2.71×) spans different model/hardware configurations; specific workloads and the number of GPU configurations evaluated are not detailed in the abstract.
- The system targets resource-constrained environments; at full-scale clusters with ample memory, the benefits may be smaller.