---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Paul Janson
- Benjamin Thérien
- Quentin Anthony
- Xiaolong Huang
- Abhinav Moudgil
- Eugene Belilovsky
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/Belilovsky-Lab/pylo
domain:
- llm-training
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: CUDA-accelerated VeLO/fc_lopt throughput on ViT-B/16 increases from 49.73/39.36
  to 191.18/205.59 samples/sec; ~4x speedup over naive implementations.
models_evaluated: []
observations:
  balance: Combining learned optimizers with LR schedules and weight decay substantially
    improves convergence; prior JAX-based tools lacked this integration capability.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=M9V1n4KxSd
organizations:
- Concordia University
presentation_type: oral
principles:
- balance
problem: State-of-the-art learned optimizers like VeLO are JAX-only and lack PyTorch
  interfaces, excluding ~70% of the ML community from using them at scale.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3824_HZUGKXd.pdf
slug: pylo-towards-accessible-learned-optimizers-in-pytorch
status: draft
title: 'Pylo: Towards Accessible Learned Optimizers in PyTorch'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3824
---

## Background

Learned optimizers are neural networks meta-trained to replace fixed update rules like Adam: they take gradients in and emit weight updates. The flagship, VeLO, was meta-trained for 4,000 TPU-months entirely in JAX. No PyTorch library exposed these as drop-in `torch.optim.Optimizer` replacements at competitive throughput.

## Key Contributions

- **PyLO library**: PyTorch-based package exposing learned optimizers (fc_lopt, VeLO) via the standard `torch.optim.Optimizer` interface, making them drop-in replacements for Adam without requiring JAX
- **CUDA-accelerated optimizer kernels**: custom CUDA implementations of fc_lopt and VeLO achieve ~4× throughput on ViT-B/16 (batch size 32) vs. naive Python implementations (39.36/49.73 → 205.59/191.18 samples/sec)
- **LR schedule and weight decay integration**: demonstrates learned optimizers benefit substantially from combining with standard optimization tools, a capability missing from prior JAX-based implementations
- Open-source at https://github.com/Belilovsky-Lab/pylo; targets large-scale pre-training tasks beyond the limited-scale academic tasks of prior learned optimizer work

## Trade-offs

- VeLO was meta-trained for 4000 TPU-months on a fixed distribution; its generalization to novel architectures outside the meta-training distribution is not guaranteed.
- Throughput benchmarks are measured on ViT-B/16; LLM decoder pre-training workloads may exhibit different bottlenecks.

## Nuances

- The ~70% PyTorch usage statistic is approximate; it motivates the accessibility argument but does not directly measure learned optimizer adoption rates.
- The improvement from combining LR schedules with learned optimizers is established empirically; the theoretical interaction between learned optimizer dynamics and external schedule signals is not fully characterized.