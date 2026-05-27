---
agentic_models: []
arxiv_url: ''
authors:
- Fengjuan Wang
- Zhiyi Su
- Xingzhu Hu
- Cheng Wang
- Mou Sun
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/021ai/FP8-FLOW-MOE-AE
domain:
- llm-training
hardware:
- GPU
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: FP8-Flow-MoE achieves 21% higher throughput and 16.5 GB less GPU memory
  vs BF16/naive-FP8 on a 671B MoE model with stable convergence.
models_evaluated:
- MoE LLM (671B parameters)
observations:
  cache: Scaling-aware transpose and fused FP8 operators eliminate explicit cast operations,
    reducing Q/DQ conversions from 12 to 2 in the MoE training dataflow.
  fuse: FP8-centric dataflow keeps tensors in FP8 format throughout, eliminating BF16
    materializaion steps that waste memory bandwidth.
  quantize: Casting-free FP8 stores and computes in the same format, eliminating double-quantization
    error from the FP8-store→BF16-compute round-trip; single-format FP8 paths reduce
    noise across MoE.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=wyH60Su6G7
organizations:
- Zhejiang Lab
presentation_type: oral
principles:
- cache
- fuse
- quantize
problem: FP8 MoE training still relies on BF16-dominated dataflows with frequent quantize-dequantize
  casts, eroding most of FP8's theoretical efficiency gains.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3737.pdf
slug: fp8-flow-moe-a-casting-free-fp8-recipe-without-double-quanti
status: draft
title: 'FP8-Flow-MoE: A Casting-Free FP8 Recipe without Double Quantization Error'
topics:
- quantization
- moe
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3737
---

## Background

FP8 on H100/H200 roughly doubles matmul throughput and halves memory bandwidth vs. BF16, but most frameworks keep primary compute in BF16 and cast to FP8 only for matmul. In MoE models with many expert layers, tensors are quantized and dequantized at every boundary, erasing most of the theoretical speedup. When a tensor is quantized along different dimensions for storage vs. compute, two rounding steps accumulate — "double quantization error."

## Key Contributions

- **Quantization-consistent FP8-centric dataflow**: Maintains tensors in FP8 format throughout the MoE forward and backward pass, eliminating 10 of 12 explicit cast operations via a scaling-aware transpose.
- **Fused FP8 operators**: Custom fused kernels for MoE routing + expert computation in FP8, preventing intermediate BF16 materialization at operator boundaries.
- **Plug-and-play recipe**: Compatible with TransformerEngine and Megatron-LM, enabling drop-in adoption for existing large-scale MoE training pipelines.

## Trade-offs

- Removing BF16 intermediate tensors reduces numerical precision checkpoints for debugging; diagnosing numerical instability is harder in a fully FP8 pipeline.
- The scaling-aware transpose adds bookkeeping complexity for per-tensor scaling factors across operator boundaries.

## Nuances

- The double quantization error problem is specific to cases where tensors are quantized along different dimensions — the paper's fix requires consistent dimension-aware scaling throughout the dataflow.
- Results on a 671B MoE model; behavior on smaller MoE models may differ due to different compute-to-communication ratios.