---
agentic_models: []
arxiv_url: ''
authors:
- Zezhou Wang
- Youjie Li
- Zhiqi Lin
- Jiacheng Yang
- Cong Xie
- Guanyu Feng
- Zheng Zhong
- Ziyue Huang
- Hongyu Zhu
- Zhi Zhang
- Yanghua Peng
- Xin Liu
award: ''
citations: 0
citations_updated: '2026-05-24'
code_url: ''
date: '2026-05-21'
domain:
- llm-training
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
observations: []
key_results: Flexible FSDP with block-wise quantization support; significant memory
  efficiency and performance improvements at scale
mlsys_official_category: Research Papers
mlsys_url: https://mlsys.org/virtual/2026/oral/3860
models_evaluated: []
openreview_url: https://openreview.net/forum?id=3Lj8R0F48P
organizations:
- ByteDance
presentation_type: oral
problem: Existing FSDP (ZeRO) implementations lack flexibility for advanced training
  techniques like block-wise quantization and composable parallelism strategies.
project_url: ''
reading_status: read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3860.pdf
slug: vescale-fsdp
topics:
- fsdp-zero
- quantization
- communication-overlap
title: 'veScale-FSDP: Flexible and High-Performance FSDP at Scale'
---

## Summary

FSDP (Fully Sharded Data Parallel), also known as ZeRO (Zero Redundancy Optimizer), is the dominant approach for memory-efficient large model training: optimizer states, gradients, and parameters are sharded across GPUs, reducing per-GPU memory by a factor of the world size. However, existing FSDP implementations (PyTorch FSDP, DeepSpeed ZeRO) are relatively rigid and don't compose well with advanced techniques.

veScale-FSDP, part of ByteDance's veScale framework, redesigns FSDP to be:

- **Flexible in sharding granularity**: Supports sub-module, block-level, and custom sharding patterns beyond the default flat parameter sharding
- **Composable with quantization**: Integrates block-wise quantization (where weight blocks are quantized at different precisions) directly into the FSDP communication and computation schedule
- **High-performance**: Minimizes overhead from the increased flexibility through careful scheduling

## Key Contributions

- Flexible FSDP design that supports diverse sharding patterns
- Integration with block-wise quantization in the FSDP training loop
- Part of the open-source veScale distributed training framework
- Memory efficiency and performance improvements at scale

## Method

The core change is decoupling parameter sharding from the flat-parameter assumption. veScale-FSDP maintains a sharding metadata graph that describes the desired sharding for each parameter group. The all-gather and reduce-scatter operations are scheduled according to this graph. Block-wise quantization is inserted as a transformation on the parameter shards before communication.

## Results

- Significant performance improvements over standard FSDP at scale
- Memory efficiency gains from block-wise quantization integration
- Demonstrated flexibility for advanced training configurations

## Limitations

- Complexity of sharding metadata graph may increase engineering overhead
- Quantification of "significant" improvements not fully captured in the MLSys page extract — see paper for numbers

## Personal Notes

<!-- Add your own observations, questions, and connections to other work here -->