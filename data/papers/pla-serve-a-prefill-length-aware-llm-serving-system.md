---
agentic_models: []
arxiv_url: https://arxiv.org/abs/2601.11589
authors:
- Jianshu She
- Zonghang Li
- HONGCHAO DU
- Shangyu Wu
- Wenhao Zheng
- Eric Xing
- Zhengzhong Liu
- Huaxiu Yao
- Chun Jason Xue
- Qirong Ho
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware:
- NVIDIA H200
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: 30%+ TTFT reduction vs. SGLang under PD disaggregation; 35% throughput
  gain and 28% fewer SLO violations on Qwen2.5-32B on H200.
models_evaluated:
- Qwen2.5-7B
- Qwen2.5-14B
- Qwen2.5-32B
observations:
  cache: CUDA Graph plans for power-of-two length-bucket short prefills
    reuse compiled graphs across requests, eliminating kernel launch overhead and
    JIT compilation per request.
  balance: Mixing compute-bound long and memory-bound short prefills in
    one batch leaves GPU idle after short requests finish; dedicated queues keep each
    batch's computation homogeneous.
official_category: ''
openreview_url: https://openreview.net/forum?id=dzjCkSEDyG
organizations:
- Carnegie Mellon University
- University of Illinois Urbana-Champaign
presentation_type: oral
principles:
- balance
- cache
problem: Batching short and long prompts together causes long requests to delay short
  ones, inflating TTFT for the majority of real-world workloads.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3787_G7LPmPu.pdf
slug: pla-serve-a-prefill-length-aware-llm-serving-system
status: draft
title: 'PLA-Serve: A Prefill-Length-Aware LLM Serving System'
topics:
- continuous-batching
- kv-cache
- prefix-caching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3787
---

## Key Contributions

- **Dual-queue length disaggregation**: Separate request queues for long-prefill (compute-bound) and short-prefill (memory-bound) requests with either temporal disaggregation (alternating on a single prefill instance) or spatial disaggregation (dedicated instances per length class), eliminating contention between the two bottleneck types.
- **Adaptive Wait-Depth (AWD) scheduler**: Dynamically adjusts batch waiting windows and target batch depths based on observed fill time and actual batch sizes, balancing per-request TTFT against throughput without requiring manual SLO threshold configuration.
- **CUDA Graph-based clustering for short prefills**: Pre-captures fixed execution graphs keyed by power-of-two prompt-length × batch-size buckets, reducing kernel launch overhead and enabling 7.3–8.3% time savings on short-prefill distillation workloads by reusing compiled graphs.
- **Instance-pressure controller**: Lightweight feedback controller that dynamically shifts workload type across multi-GPU instances based on real-time per-instance queue pressure, enabling 28% SLO violation reduction in multi-instance deployments versus standard load balancing.

## Trade-offs

- CUDA Graph initialization adds 8–12 seconds of startup overhead per graph and 228–277 MB of GPU memory per model; only amortized if the same length-bucket combination recurs frequently.
- CUDA Graph reuse is limited to short-prefill requests; long-prefill requests remain dynamically dispatched, so mixed long/short traffic reduces graph reuse frequency.
- Spatial disaggregation (dedicated prefill instances per length class) increases GPU pool fragmentation; low-traffic length classes strand capacity.

## Nuances

- Evaluations use Qwen2.5 models (7B–32B) on H200; the benefit of length disaggregation depends on the prompt-length distribution of the target workload — workloads with unimodal length distributions gain less than those with bimodal long/short separation.
- The dual-queue boundary between "long" and "short" is a threshold that must be calibrated per model and serving configuration; a suboptimal split reduces gains without clear failure indication.
- Multi-turn conversation workloads accumulate context over turns, shifting requests from short to long class during a session; the system's handling of dynamic length class transitions is not fully characterized.