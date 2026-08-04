---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Lingjun Gao
- Zhican Wang
- Zhiwen Mo
- Hongxiang Fan
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- ml-kernels
hardware:
- NVIDIA GPU
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 1.41× speedup over gsplat baseline with negligible rendering quality
  drop, via joint algorithm and system co-optimization.
models_evaluated: []
observations:
  skip: Adaptive early sorting skips Gaussian primitives that contribute
    negligible opacity to the current view, reducing sort and rasterize work proportionally
    to scene sparsity.
  fuse: GPU-efficient axis-shared rasterization shares axis-aligned
    tile data across adjacent rasterization threads, cutting redundant memory loads
    per tile.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=i05mMLR9BX
organizations:
- Imperial College London
presentation_type: oral
principles:
- skip
- fuse
problem: 3D Gaussian Splatting requires rendering millions of Gaussians in parallel,
  imposing memory and compute demands that limit deployment on constrained GPUs.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: swiftgs-algorithm-and-system-co-optimization-for-fast-3d-gau
status: draft
title: 'SwiftGS: Algorithm and System Co-Optimization for Fast 3D Gaussian Splatting
  on GPUs'
topics:
- kernel-fusion
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3773
---

## Background

3D Gaussian Splatting represents a scene as millions of semi-transparent ellipsoidal Gaussians, rendered by depth-sorting and alpha-compositing them tile by tile — higher quality than NeRF at lower cost. Every frame sorts and rasterizes all primitives regardless of contribution. Two costs dominate: the O(N log N) depth sort over all Gaussians, and per-tile rasterization that reloads the same data per thread.

## Key Contributions

- **Flash3DGS co-optimization framework**: joint algorithm and system approach combining three complementary optimizations — adaptive early sorting, GPU-efficient axis-shared rasterization, and dynamic thresholding — that together achieve up to 1.41× speedup over the gsplat baseline with negligible image quality loss.
- **Adaptive early sorting**: terminates the Gaussian depth sort early when remaining primitives fall below a dynamic visibility threshold, reducing O(N log N) sort cost proportional to scene sparsity.
- **GPU-efficient axis-shared rasterization**: restructures the rasterization kernel to share tile-axis data across threads within a warp, reducing redundant global memory accesses and improving occupancy.
- **Dynamic thresholding**: prunes low-opacity or distant Gaussians per frame at runtime without architectural changes or retraining, adapting pruning aggressiveness to scene content.
- Optimizations are orthogonal to existing 3DGS acceleration methods, enabling additive speedup when combined.

## Trade-offs

- Adaptive early sorting and dynamic thresholding trade off rendering completeness for speed; aggressive thresholds can cause visible quality degradation in high-density or complex scenes.
- The co-optimization is evaluated on specific GPU architectures; portable performance across older or mobile GPUs with different memory hierarchies is not characterized.

## Nuances

- The 1.41× speedup is measured versus gsplat; gains versus hardware-specific TensorRT-optimized baselines would likely be lower.
- Results target offline rendering quality benchmarks; real-time applications with strict per-frame deadlines may require different threshold calibration.
