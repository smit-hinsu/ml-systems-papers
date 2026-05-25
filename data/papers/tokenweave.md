---
agentic_models: []
arxiv_date: 2025-05
arxiv_url: https://arxiv.org/abs/2505.11329
authors:
- Raja Gond
- Nipun Kwatra
- Ramachandran Ramjee
award: ''
citations: 0
citations_updated: '2026-05-24'
code_url: https://github.com/microsoft/tokenweave
domain:
- llm-serving
hardware:
- H100
- B200
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Up to 1.28× latency and 1.19× throughput on 8×H100/8×B200 DGX for Llama-3.3-70B,
  Qwen2.5-72B, Mixtral-8x22B using only 2–8 SMs via fused AllReduce-RMSNorm kernel
models_evaluated:
- Llama-3.3-70B
- Qwen2.5-72B
- Mixtral-8x22B
observations:
  overlap-independent-work: Wave-aware token splitting partitions batches so communication
    and compute waves align, preventing the wave quantization penalty that defeats
    naive decomposition strategies at small batch sizes
  reduce-data-movement: Performing RMSNorm after ReduceScatter (on 1/N of the tensor)
    rather than after full AllReduce halves HBM reads; combining with Multimem eliminates
    an intermediate HBM write, achieving 1.34×–1.39× single-layer speedup
official_category: Research Papers
openreview_url: https://openreview.net/forum?id=rh2Ylffkq6
organizations:
- Microsoft
presentation_type: oral
principles:
- reduce-data-movement
- overlap-independent-work
problem: In tensor-parallel LLM inference, AllReduce sits on the critical path between
  every transformer layer; existing overlap techniques cause SM contention and fail
  at small batch sizes.
project_url: ''
reading_status: read
research_or_industry: research
slides_url: ''
slug: tokenweave
status: draft
title: 'TokenWeave: Efficient Compute-Communication Overlap for Distributed LLM Inference'
topics:
- tensor-parallelism
- kernel-fusion
- communication-overlap
- all-reduce
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3744
---


## Key Contributions

- **Fused AllReduce-RMSNorm kernel**: performs RMSNorm directly on ReduceScatter partial results before the AllGather completes, using NVSHARP/Multimem PTX instructions on Hopper/Blackwell GPUs — reduces HBM reads from two to one and eliminates an intermediate HBM write
- **Minimal-SM communication**: the fused kernel uses only 2–8 SMs on an 8×H100 system (vs. 16–20+ for prior approaches), freeing the remaining SMs for overlapping compute without resource contention
- **Wave-aware token splitting**: partitions token batches into two sub-batches sized so that the total number of GPU waves does not exceed the single-kernel wave count, preventing the throughput regression that naive decomposition causes at small batch sizes (≥1024 tokens effective)
- Evaluated on Llama-3.3-70B, Qwen2.5-72B, and Mixtral-8x22B on 8×H100 and 8×B200 DGX; TokenWeave occasionally outperforms a hypothetical communication-free model, indicating RMSNorm fusion yields gains beyond communication hiding alone

## Trade-offs

- NVSHARP/Multimem instructions are only available on Hopper (H100) and Blackwell (B200) architectures; the approach does not apply to older GPUs (A100) or non-NVLink topologies (InfiniBand clusters)
- Benefits are largest at decode-phase batch sizes; at very large prefill batches the AllReduce fraction shrinks (Amdahl's law) and gains diminish

## Nuances

- The 1.28× end-to-end latency improvement is measured against an optimized vLLM-Multimem baseline, not vanilla vLLM; the gap vs. unoptimized baselines would be larger but less meaningful
- Wave-aware splitting introduces a batch fragmentation overhead that the paper carefully controls but does not fully characterize for all sequence-length and batch-size combinations
- The approach is not yet enabled by default in vLLM or TensorRT-LLM; production adoption requires framework integration work beyond the kernel implementation