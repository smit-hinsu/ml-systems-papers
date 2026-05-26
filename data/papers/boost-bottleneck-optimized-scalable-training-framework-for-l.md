---
slug: boost-bottleneck-optimized-scalable-training-framework-for-l
title: "BOOST: BOttleneck-Optimized Scalable Training Framework for Low-Rank Large Language Models"
authors:
- Zhengyang Wang
- Ziyue Liu
- Ruijie Zhang
- Avinash Maurya
- Bogdan Nicolae
- Paul Hovland
- Franck Cappello
- Zheng Zhang
organizations:
- UC Santa Barbara
- Argonne National Laboratory
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3830
openreview_url: https://openreview.net/forum?id=JhN5hldx4V
arxiv_url: ''
presentation_type: oral
official_category: ''
award: ''
status: draft
reading_status: want-to-read
research_or_industry: research
indexed_by: smithinsu
indexed_date: '2026-05-24'
citations: null
citations_updated: ''
code_url: ''
project_url: ''
slides_url: ''
domain:
- llm-training
hardware:
- GPU
models_evaluated:
- Low-rank bottleneck LLMs
agentic_models: []
topics:
- tensor-parallelism
principles:
- fuse
- balance
observations:
  fuse: "Bottleneck-aware tensor parallelism splits low-rank factors across devices to avoid the excessive cross-device communication of naively applied 3D parallelism."
  balance: "Online-RMSNorm and linear layer grouping keep GPU utilization high by eliminating idle bubbles introduced by bottleneck architecture's uneven operator sizes."
problem: "Low-rank bottleneck architectures scale poorly under standard 3D tensor parallelism, causing excessive communication overhead and low GPU utilization."
key_results: "BOOST achieves 1.46-1.91x speedup over full-rank baselines and 1.87-2.27x over naive 3D-parallel low-rank training on GPU clusters."
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
