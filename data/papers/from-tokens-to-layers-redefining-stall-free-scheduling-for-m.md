---
agentic_models: []
arxiv_url: https://arxiv.org/abs/2510.08055
authors:
- Gunjun Lee
- Jiwon Kim
- Jaiyoung Park
- Younjoo Lee
- Jung Ho Ahn
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware:
- NVIDIA H100
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Up to 70% TTFT reduction and 41% end-to-end latency improvement on Qwen3-30B-A3B
  and GPT-OSS-20B MoE models on H100; 22% per-token energy reduction.
models_evaluated:
- Qwen3-30B-A3B
- GPT-OSS-20B
observations:
  overlap-independent-work: Layered prefill assigns one layer group per iteration
    for both decode and prefill, interleaving across model depth rather than serializing;
    prefill latency hides behind decode.
  reduce-data-movement: Token-level chunked prefill forces expert weight reloads per
    chunk, inflating MoE off-chip traffic by up to 39%; layer-group scheduling loads
    each weight exactly once per request.
  exploit-memory-hierarchy: Layer-group scheduling keeps each expert's weights resident
    for the full layer group, loading each weight exactly once per request vs. once
    per chunk with token-level scheduling (39% more traffic).
official_category: ''
openreview_url: https://openreview.net/forum?id=yyDbI3HXco
organizations: []
presentation_type: oral
principles:
- reduce-data-movement
- overlap-independent-work
- exploit-memory-hierarchy
problem: Chunked prefill in MoE serving forces redundant expert weight reloads per
  chunk, inflating memory traffic by up to 39% and increasing TTFT.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3732_cXYJO0z.pdf
slug: from-tokens-to-layers-redefining-stall-free-scheduling-for-m
status: draft
title: 'From Tokens to Layers: Redefining Stall-Free Scheduling for MoE Serving with
  Layered Prefill'
topics:
- moe
- continuous-batching
- kernel-fusion
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3732
---

## Key Contributions

- **Layered prefill scheduling**: Partitions the transformer into G = max(1, ⌈L/512⌉) contiguous layer groups (where L is input length); per iteration, exactly one designated group processes both decode and new prefill work while all others run decode-only, ensuring each token traverses every expert weight exactly once.
- **Elimination of redundant MoE weight loads**: Because each request processes all tokens in a layer group together before moving to the next, expert weights are loaded once per layer group per request — removing the per-chunk reload overhead that chunked prefill incurs on MoE models, reducing memory traffic by 39% on long-context (arXiv) and 12% on shorter-context (ShareGPT) workloads.
- **Maintained stall-free decode**: The one-group-per-iteration interleaving rule guarantees prefill completes in exactly G iterations without preempting in-progress decode; TBT compliance is preserved at the same level as chunked prefill while TTFT is dramatically reduced.
- Evaluated on two H100 GPUs with Qwen3-30B-A3B (128 experts, top-8) and GPT-OSS-20B (32 experts, top-4), achieving a 14–45% increase in SLO-attained request rate.

## Trade-offs

- Layered prefill's benefit scales with prompt length and MoE expert count; on shorter-context workloads like ShareGPT, memory traffic reduction drops to 12%, limiting TTFT and latency gains.
- Layer-group formation requires knowing the input length upfront to compute G; dynamically arriving requests with varying lengths may make group boundaries suboptimal across a mixed batch.

## Nuances

- Evaluation is on a 2-GPU setup; behavior at larger tensor-parallelism degrees (8+ GPUs per node) where all-to-all communication dominates over memory bandwidth may shift the bottleneck and reduce layered prefill's advantage.
- The per-token energy reduction (up to 22%) is measured on the evaluated models; models with denser MoE routing (higher top-k) or larger expert sizes would see proportionally different savings.
- The approach is specific to MoE models; for dense transformer models without expert routing, layered prefill provides no benefit over standard chunked prefill.