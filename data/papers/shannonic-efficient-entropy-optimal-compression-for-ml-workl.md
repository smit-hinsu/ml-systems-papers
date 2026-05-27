---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Kareem Ibrahim
- Mohammadjavad Maheronnaghsh
- Andreas Moshovos
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
- fleet-efficiency
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 1.3–3.1x faster federated learning over bandwidth-constrained networks;
  29–32% latency reduction in edge-cloud LLM inference; codec state footprint of 530B.
models_evaluated: []
observations:
  fuse: Near-entropy-optimal lossless compression of 8-bit model
    tensors cuts transmitted bytes in federated learning and edge-cloud LLM inference,
    reducing bandwidth-limited latency by 29–32%.
  tier: 530B codec state footprint enables compression/decompression
    to run efficiently on edge devices with limited SRAM, making tensor compression
    practical for bandwidth-constrained edge inference.
official_category: ''
openreview_url: https://openreview.net/forum?id=NhMxI0GbB8
organizations:
- University of Toronto
presentation_type: oral
principles:
- fuse
- tier
problem: Existing lossless tensor compression methods trade off between compression
  ratio, memory footprint, and throughput, making them impractical for ML workloads.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: shannonic-efficient-entropy-optimal-compression-for-ml-workl
status: draft
title: 'Shannonic: Efficient Entropy-Optimal Compression for ML Workloads'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3820
---

## Background

In federated learning and edge-cloud inference, bandwidth between nodes is the bottleneck — lossless compression reduces transmitted bytes without changing model behavior. General-purpose codecs (gzip, zstd) target text and binary data, not 8-bit quantized ML tensor distributions, leaving headroom above the Shannon entropy limit. Prior ANS-based ML tensor codecs either need megabytes of state (won't fit in edge SRAM) or sacrifice throughput to hit high compression ratios.

## Key Contributions

- **Shannonic codec**: lossless ML tensor compression achieving near-entropy-optimal compression with only 530B of codec state and high throughput; encodes each value as a (range index, offset) pair
- **Offline subrange partitioning**: pre-processing step partitions the tensor value space into optimally selected subranges; generates encoding/decoding tables that outperform standard ANS compression
- **Entropy coding with ANS**: uses asymmetric numeral systems to entropy-encode the range index; formally proven and empirically shown to achieve higher compression efficiency than standard ANS
- Achieves coding efficiency within 1% of the Shannon limit for 8-bit quantized models; enables 1.3–3.1× faster federated learning and 29–32% latency reduction in edge-cloud LLM inference

## Trade-offs

- Offline pre-processing step requires building encoding/decoding tables per tensor value distribution; distributions that change significantly (e.g., during training) require re-running the pre-processing step.
- Near-entropy-optimal compression with ANS is computationally more complex than simple run-length encoding; decoder implementation must be efficient enough for edge devices.

## Nuances

- The 1.3–3.1× federated learning speedup range spans different network bandwidth configurations; the exact network conditions (bandwidth, latency) are not specified.
- Evaluation focuses on 8-bit quantized models; compression ratios for floating-point (FP16/BF16) tensors may differ due to different value distributions.
- "Near-entropy-optimal" (within 1% of Shannon limit) is a stronger claim than typical ML compression work; the formal proof is a notable contribution.
