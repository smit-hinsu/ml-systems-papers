---
agentic_models: []
arxiv_date: 2026-01
arxiv_url: https://arxiv.org/abs/2601.05296
authors:
- Jiyuan Zhang
- Yining Liu
- Siqi Yan
- Lisen Deng
- Jennifer Cao
- Shuqi Yang
- Bi Xue
- Min Ni
- Shen Li
award: ''
citations: 0
citations_updated: '2026-05-24'
code_url: ''
date: '2026-05-21'
domain:
- recs-models
- llm-training
hardware:
- H100
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Up to 6.2× speedup and 4× activation memory reduction vs. MegaBlocks
  baseline on H100; SwiGLU MoE gets 2×–6.2× speedup, SiLU gets 1.4×–3.7×
models_evaluated: []
observations:
  avoid-redundant-work: Activation checkpointing recomputes SiLU during the backward
    pass instead of storing intermediates, trading cheap recomputation for large HBM
    savings without changing training semantics
  exploit-memory-hierarchy: SwiGLU fusion combines dual first-layer projections and
    activation epilogue into a single kernel, eliminating intermediate global memory
    writes and keeping activations in registers/shared memory
  reduce-data-movement: Conventional MoE routing materializes ~94GB permutation buffers
    in HBM; four compact index structures replace these with index-only tensors, eliminating
    most permutation traffic.
official_category: Research Papers
openreview_url: https://openreview.net/forum?id=L8qKfWWkry
organizations:
- Meta
presentation_type: oral
principles:
- reduce-data-movement
- exploit-memory-hierarchy
- avoid-redundant-work
problem: MoE training stores all expert weights and routing buffers in HBM even though
  only top-k experts fire per token, creating a memory wall that limits batch size.
project_url: ''
reading_status: read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3826_TlhaaTE.pdf
slug: moeblaze
status: draft
title: 'MoEBlaze: Breaking the Memory Wall for Efficient MoE Training on Modern GPUs'
topics:
- moe
- kernel-fusion
- cpu-offload
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3826
---

## Key Contributions

- **Four compact token dispatch index structures**: expert_token_indices, expert_token_offsets, token_expert_indices, and token_index_map replace conventional large materialized routing buffers, eliminating ~94GB of intermediate tensor allocations during expert dispatch
- **SwiGLU fused kernel**: combines both first-layer projections and the activation epilogue into a single CUDA kernel, removing intermediate HBM writes for the dominant operation in SwiGLU-based MoE experts
- **On-the-fly gathering**: expert GEMM accesses original unpermuted activations directly via index lists rather than requiring an explicit token permutation pass, removing a full HBM round-trip
- **SiLU activation checkpointing**: recomputes cheap SiLU activations during the backward pass rather than storing them, yielding up to 3.6× activation memory savings for SiLU-based MoE
- System evaluated on seven representative MoE configurations spanning dimensions 512–2048, 4–16 experts, top-k 1–4, achieving 6.2× peak speedup over MegaBlocks on H100

## Trade-offs

- Activation checkpointing increases backward-pass compute; benefit is largest when memory is the bottleneck, but recomputation cost becomes visible at high batch sizes where HBM is not saturated
- On-the-fly gathering trades spatial locality for memory savings; token accesses are non-sequential and may cause cache pressure on hardware with limited L2/SRAM

## Nuances

- Experiments measure a single MoE layer, not end-to-end training throughput; pipeline and communication overheads in multi-node training are not characterized
- The paper originates from Meta's Thinking Machines Lab but does not explicitly state production deployment; the "over 4× speedup, over 50% memory savings" claim in the abstract combines best-case numbers from different configurations
- Results are specific to recommendation-model MoE topology (many small experts, moderate sequence lengths); LLM-scale MoE with fewer, larger experts may exhibit different bottlenecks