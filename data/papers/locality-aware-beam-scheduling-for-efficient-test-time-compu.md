---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Hsing-Ti Wang
- Hung-Tso Shiao
- Chia-Lin Yang
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
- edge-inference
hardware:
- Consumer-grade GPUs
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Over 95% KV cache transfer reduction; 3.39×–9.72× end-to-end speedup
  on OPT-6.7B, 3.60×–8.74× on LLaMA-2-7B, 4.17×–7.99× on Qwen-7B vs. layer-wise
  offloading
models_evaluated:
- OPT-6.7B
- LLaMA-2-7B
- Qwen-7B
observations:
  cache: Inter-beam locality detection identifies beams sharing a common
    prefix and reuses their overlapping KV segments, eliminating redundant KV cache
    transfers for prefix data that would otherwise be re-transferred independently
    for each beam.
  pipeline: Balanced grouping with prefetching overlaps KV cache
    data movement from CPU/host memory with GPU computation, hiding transfer latency
    behind active decode steps during test-time compute.
official_category: ''
openreview_url: https://openreview.net/forum?id=dTo8jAXm9K
organizations:
- National Taiwan University
presentation_type: oral
principles:
- cache
- pipeline
problem: Step-wise beam search for test-time compute on consumer GPUs causes severe
  I/O stalls because the expanding KV cache must be repeatedly transferred between
  CPU and GPU memory.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: locality-aware-beam-scheduling-for-efficient-test-time-compu
status: draft
title: Locality-Aware Beam Scheduling for Efficient Test-Time Compute with a Consumer-grade
  GPU
topics:
- kv-cache
- memory-management
- prefix-caching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3788
---

## Key Contributions

- **Inter-token locality exploitation**: Within each decode step, consecutive tokens in the same beam access nearly identical KV cache data; the scheduler batches these accesses to maximize transfer reuse per I/O operation.
- **Inter-beam locality exploitation**: Beams sharing a common prefix reuse their overlapping KV segments, eliminating redundant transfers for shared prefix data across the beam tree.
- **Balanced grouping with prefetching**: Beams are grouped by KV locality and scheduled with prefetching, overlapping data movement with compute to hide transfer latency during beam search expansion.

## Trade-offs

- The approach targets consumer-grade GPUs with limited VRAM and CPU-GPU bandwidth; on data center GPUs with large HBM capacity, the KV transfer bottleneck is less severe and the benefit diminishes.
- Balanced grouping constrains beam scheduling order, which may affect beam search diversity or require relaxed prefix-sharing assumptions for certain decoding strategies.

## Nuances

- The 95%+ transfer reduction is the peak observed reduction; actual savings depend on the beam width, sequence length, and the degree of prefix sharing among active beams.
- Speedup ranges (e.g., 3.39×–9.72× for OPT-6.7B) reflect variation across beam widths and sequence lengths; the upper end occurs at wide beam configurations where locality is most exploitable.
