---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Jinsol Park
- Corey Nolet
- Edward Raff
- Tim Oates
- Akira Naruse
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- ml-compilers
hardware:
- NVIDIA GPU (multi-GPU node)
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 22.7× speedup on single GPU vs CPU baseline; projected up to 74× speedup
  with multi-GPU for datasets too large for CPU to complete
models_evaluated: []
observations:
  balance: Multi-GPU sharding distributes nearest-neighbor construction and graph
    optimization across devices, eliminating single-GPU memory wall at hundreds-of-GB
    scale.
  tier: Out-of-core strategy partitions the dataset across GPU HBM and host DRAM,
    staging tiles through high-bandwidth GPU memory to avoid CPU bottleneck on large
    embeddings.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=CR35IJQD2J
organizations:
- UMBC
- NVIDIA
presentation_type: oral
principles:
- tier
- balance
problem: UMAP on tens to hundreds of GB of vectors is intractable on CPU (hours to
  days), blocking interactive exploratory workflows at massive scale.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3847.pdf
slug: massive-scale-out-of-core-umap-on-the-gpu
status: draft
title: Massive-Scale Out-Of-Core UMAP on the GPU
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3847
---

## Background

GPU-accelerated UMAP (cuML) runs in minutes for up to ~10M vectors, but industry-scale datasets (hundreds of millions for recommendation systems or genomics) exceed GPU HBM capacity. CPU-based UMAP at that scale takes hours to days, blocking interactive analysis. Out-of-core tiling through GPU memory in stages is the standard technique, but UMAP's k-NN graph construction and optimization steps have complex cross-dataset dependencies that complicate tiling.

## Key Contributions

- **Out-of-core GPU UMAP**: partitions dataset into tiles that exceed single-GPU memory, staging each tile through GPU HBM for accelerated k-NN graph construction and optimization while spilling to host DRAM between tiles
- **Multi-GPU support**: optional data-parallel extension distributes tiles across multiple GPUs on a single node, enabling near-linear scaling at hundred-GB dataset sizes where CPU cannot complete within practical time limits
- Achieves interactive-analysis turnaround times for datasets that previously required hours-to-days of CPU processing

## Findings

- Single-GPU delivers 22.7× speedup over CPU on smaller datasets where the CPU baseline runs to completion.
- At larger scales where CPU cannot complete, multi-GPU throughput extrapolation projects up to 74× effective speedup.
- Out-of-core overhead is modest; the GPU memory hierarchy remains the dominant performance lever even with host-DRAM spilling.

## Trade-offs

- Out-of-core tiling introduces synchronization points between tiles; embedding quality may differ slightly from a fully in-memory run depending on tile boundary handling.
- Projected 74× multi-GPU number is extrapolated from scaling behavior, not measured end-to-end on a single run, since the CPU baseline cannot complete at those scales.