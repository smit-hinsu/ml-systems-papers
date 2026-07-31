---
agentic_models: []
arxiv_date: 2025-10
arxiv_url: https://arxiv.org/abs/2510.27656
authors:
- Nandor Licker
- Kevin Hu
- Vladimir Zaytsev
- Lequn Chen
award: ''
citations: 9
citations_updated: '2026-07-31'
code_url: ''
domain:
- llm-serving
- rl-training
hardware:
- NVIDIA H100
- NVIDIA H200
- NVIDIA ConnectX-7
- AWS EFA
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: 400 Gbps peak on ConnectX-7 and AWS EFA; RL weight updates for trillion-parameter
  models in 1.3 s; MoE decode latency matches DeepEP on ConnectX-7.
models_evaluated: []
observations:
  fuse: Paging writes at 64 KiB granularity achieves 364–396 Gbps; coarser writes
    waste bandwidth on padding while finer granularity increases doorbell overhead.
  pipeline: KvCache transfers for disaggregated inference are issued layer-by-layer
    so RDMA operations are pipelined with computation on the GPU, hiding transfer
    latency behind prefill processing.
official_category: ''
openreview_url: https://openreview.net/forum?id=SjVa05wEiY
optimization_type: []
organizations:
- Perplexity AI
presentation_type: oral
principles:
- pipeline
- fuse
problem: Disaggregated inference, MoE routing, and async RL fine-tuning need flexible
  RDMA point-to-point, but existing libraries are NIC-specific and non-portable.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: ''
slug: fabric-lib-rdma-point-to-point-communication-for-llm-systems
status: draft
title: 'fabric-lib: RDMA Point-to-Point Communication for LLM Systems'
topics:
- moe
- communication-overlap
- kv-cache
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3807
---

## Key Contributions

- **TransferEngine abstraction**: A portable RDMA library exposing a uniform API over NVIDIA ConnectX-7 and AWS EFA, transparently managing multiple NICs per GPU (required on EFA instances with 2–4 × 100 Gbps NICs) without application-level NIC awareness.
- **WriteImm + ImmCounter primitives**: One-sided remote-memory writes with a 32-bit immediate value combined with an order-agnostic completion counter; enables reliable completion notification without requiring ordered message delivery, accommodating the differing guarantees of ConnectX and EFA transports.
- **Three production deployments**: (1) Layer-by-layer KvCache transfer for disaggregated inference with dynamic scaling; (2) pipelined asynchronous RL weight distribution completing trillion-parameter updates in 1.3 seconds; (3) dual-path MoE dispatch/combine routing tokens via RDMA inter-node and NVLink intra-node.
- Achieves 400 Gbps peak on both ConnectX-7 and EFA with 64 KiB paged writes (364–370 Gbps respectively), matching hardware-specific implementations while preserving portability.

## Trade-offs

- Host-proxy path (needed when GPU-initiated RDMA is unavailable, e.g., on AWS) adds ~15 µs latency per EP64 operation compared to the IBGDA GPU-initiated path available on ConnectX-7.
- Prefill throughput lags ConnectX-7-optimized implementations (DeepEP) due to reduced per-rank buffering; the portability abstraction trades some peak performance for hardware-agnosticism.
- All peers must use identical NIC configurations per GPU; heterogeneous clusters mixing NIC types per node are not supported.

## Nuances

- GPU-initiated communication (IBGDA) is not available on AWS cloud instances as of publication; EFA operations go through the host proxy, adding CPU involvement in the critical path for latency-sensitive decode operations.
- The 1.3-second RL update claim is for weight distribution only; the end-to-end training step time including forward/backward passes is not characterized.
- MoE dispatch/combine performance matches DeepEP on ConnectX-7 but the comparison is at equivalent EP size; at higher expert-parallelism degrees the overhead of the abstraction layer may widen.
