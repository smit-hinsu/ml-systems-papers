---
agentic_models: []
arxiv_date: 2025-12
arxiv_url: https://arxiv.org/abs/2512.10977
authors:
- Alec Hammond
- Aram Markosyan
- Aman Dontula
- Simon Mahns
- Zacharias Fisches
- Dmitrii Pedchenko
- Keyur Muzumdar
- Natacha Supper
- Site Cao
- Haishan Zhu
- Mark Saroufim
- Joe Isaacson
- Laura Wang
- Warren Hunt
- Kaustubh Gondkar
- Roman Levenstein
- Gabriel Synnaeve
- Richard Li
- Jacob Kahn
- Ajit Mathews
award: ''
citations: 4
citations_updated: '2026-07-31'
code_url: ''
domain:
- ml-kernels
- hardware
hardware:
- MTIA
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Generated 481 unique ATen operator kernels passing all PyTorch OpInfo
  tests (20,000+ tests) for MTIA silicon and simulation environments
models_evaluated: []
observations:
  cache: Shared JIT compilation cache and linter catch trivial errors before expensive
    hardware simulation, reducing the cost of the LLM generation-test loop across
    481 operators.
  search-ai: LLMs generate ATen kernels via JIT compilation and OpInfo test harness;
    passing 20,000+ correctness tests provides the verifiable signal guiding generation
    and enabling overnight backend creation.
official_category: ''
openreview_url: https://openreview.net/forum?id=O3Bx0nNGnW
optimization_type: []
organizations:
- Meta
presentation_type: oral
principles:
- search-ai
- cache
problem: New AI accelerator platforms (e.g., MTIA) lack PyTorch ATen backends; expert
  kernel authors cannot cover the full operator set needed for standard ML workloads.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3817.pdf
slug: agentic-operator-generation-for-ml-asics
status: draft
title: Agentic Operator Generation for ML ASICs
topics:
- llm-code-generation
- autotuning
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3817
---

## Key Contributions

- **TritorX system**: agentic pipeline integrating LLMs with a custom linter, JIT compilation, and PyTorch OpInfo-based test harness to generate functionally correct Triton ATen kernels at scale for new accelerator targets
- **Coverage-first philosophy**: unlike prior kernel-generation work that optimizes performance on a small set of high-usage kernels, TritorX targets correctness across the full ATen operator set including diverse data types, shapes, and argument patterns
- **481 operator kernels generated**: successfully generated kernels and wrappers for 481 unique ATen operators that pass all corresponding PyTorch OpInfo tests (20,000+ tests in total) for Meta's MTIA hardware
- **Hardware-simulation compatibility**: pipeline runs on both real MTIA silicon and hardware simulation environments for next-generation devices, enabling pre-silicon backend development

## Trade-offs

- Coverage-first design means generated kernels are not performance-optimized; achieving high throughput on critical operators requires a separate optimization pass after correctness is established.
- The approach is limited to operators expressible in Triton; operators requiring architecture-specific assembly intrinsics or memory access patterns outside Triton's abstraction need manual implementation.

## Nuances

- "Overnight generation" of a complete backend refers to correctness of functional tests, not production-readiness; performance tuning and edge-case hardening are separate steps.
- The evaluation covers 481 operators but the total ATen operator set is larger; coverage of less-common operators with unusual data type combinations is not fully characterized.
