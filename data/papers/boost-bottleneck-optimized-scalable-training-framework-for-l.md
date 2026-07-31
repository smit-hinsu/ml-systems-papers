---
agentic_models: []
arxiv_url: https://arxiv.org/abs/2512.12131
authors:
- Zhengyang Wang
- Ziyue Liu
- Ruijie Zhang
- Avinash Maurya
- Bogdan Nicolae
- Paul Hovland
- Franck Cappello
- Zheng Zhang
award: ''
citations: 3
citations_updated: '2026-07-31'
code_url: ''
domain:
- llm-training
hardware:
- GPU
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: BOOST achieves 1.46-1.91x speedup over full-rank baselines and 1.87-2.27x
  over naive 3D-parallel low-rank training on GPU clusters.
models_evaluated:
- Low-rank bottleneck LLMs
observations:
  balance: Online-RMSNorm and linear layer grouping keep GPU utilization high by eliminating
    idle bubbles introduced by bottleneck architecture's uneven operator sizes.
  fuse: Bottleneck-aware tensor parallelism splits low-rank factors across devices
    to avoid the excessive cross-device communication of naively applied 3D parallelism.
official_category: ''
openreview_url: https://openreview.net/forum?id=JhN5hldx4V
optimization_type: []
organizations:
- UC Santa Barbara
- Argonne National Laboratory
presentation_type: oral
principles:
- fuse
- balance
problem: Low-rank bottleneck architectures scale poorly under standard 3D tensor parallelism,
  causing excessive communication overhead and low GPU utilization.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3830.pdf
slug: boost-bottleneck-optimized-scalable-training-framework-for-l
status: draft
title: 'BOOST: BOttleneck-Optimized Scalable Training Framework for Low-Rank Large
  Language Models'
topics:
- tensor-parallelism
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3830
---

## Key Contributions

- **Bottleneck-aware Tensor Parallelism**: A novel parallelism strategy tailored to low-rank bottleneck architectures that reduces cross-device communication by exploiting the factored structure.
- **Online-RMSNorm and linear layer grouping**: Kernel-level optimizations that fuse operations and eliminate idle compute caused by uneven operator sizes in bottleneck layers.
- **Low-rank activation checkpointing**: Reduces memory footprint by checkpointing only the compact low-rank activations rather than full-rank intermediates.

## Trade-offs

- BOOST is specialized for low-rank bottleneck architectures; it does not generalize to standard full-rank transformers without architectural modification.
- The bottleneck architecture itself may reduce model expressiveness depending on rank choice.

## Nuances

- The 1.46-1.91x speedup is measured end-to-end over full-rank baselines, not just the communication-reduced portion.
- The comparison to naive 3D parallelism (1.87-2.27x) is the more practically relevant number for researchers already using low-rank architectures.
