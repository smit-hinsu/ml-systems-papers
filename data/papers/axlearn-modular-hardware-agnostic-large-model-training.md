---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Mark Lee
- Chang Lan
- Tom Gunter
- John Peebles
- Hanzhi Zhou
- Xuan Kelvin Zou
- Sneha Bangalore
- Chung-Cheng Chiu
- Nan Du
- Xianzhi Du
- Philipp Dufter
- Liang He
- Ruixuan Hou
- Haoshuo Huang
- Dongseong Hwang
- Xiang Kong
- Jinhao Lei
- Tao Lei
- Ethan Li
- Li Li
- Jiarui Lu
- Zhiyun Lu
- Yiping Ma
- David Qiu
- Vivek Rathod
- Senyu Tong
- Zhucheng Tu
- Chong Wang
- Jianyu Wang
- Yongqiang Wang
- Zirui Wang
- Floris Weers
- Sam Wiseman
- Guoli Yin
- Bowen Zhang
- Xiyou Zhou
- Danyang Zhuo
- Cheng Leong
- Ruoming Pang
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-training
organizations:
- Apple
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Integrates new features like RoPE across hundreds of modules with 10
  lines of code vs. hundreds required in comparable systems; maintains equivalent
  training performance at scale
models_evaluated: []
observations:
  cache: Strict interface encapsulation between components allows RoPE
    to be added across hundreds of modules with only 10 lines of code; changes propagate
    automatically without per-module manual updates.
  balance: Constant-complexity scaling (vs. linear/quadratic in competing
    systems) means adding parallelism dimensions or new hardware backends does not
    require proportionally more framework integration code.
official_category: ''
openreview_url: https://openreview.net/forum?id=41x11EB3bc
presentation_type: oral
principles:
- cache
- balance
problem: Large-scale training frameworks accumulate quadratic integration complexity
  as hardware backends and model components multiply, making rapid experimentation
  and hardware migration slow and error-prone.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: ''
slug: axlearn-modular-hardware-agnostic-large-model-training
status: draft
title: 'AXLearn: Modular, Hardware-Agnostic Large Model Training'
topics:
- tensor-parallelism
- pipeline-parallelism
- fsdp-zero
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3858
---

## Key Contributions

- **Strict component encapsulation**: each software component in AXLearn exposes a well-defined interface with no cross-layer leakage; this enables composing components across hardware backends without framework-wide refactoring
- **Constant-complexity scaling**: adding new features or parallelism strategies grows integration code at O(1) rather than O(N) or O(N²) as in competing systems; adding RoPE requires 10 lines of code across hundreds of modules vs. hundreds of lines in other frameworks
- **Hardware-agnostic training**: unified abstraction layer supports different hardware backends (GPU, TPU, custom accelerators) without model code changes; enables experimentation across infrastructure
- **Production deployment at Apple**: AXLearn is Apple's internal production training system used to train large-scale deep learning models; the paper documents design principles and operational experience from real workloads

## Trade-offs

- Strict encapsulation imposes interface overhead; components cannot directly access peer internals for performance-critical shortcuts, potentially limiting extreme hand-optimized paths.
- Hardware-agnostic abstraction may miss backend-specific optimizations that require tight coupling to the hardware; performance parity is claimed but may not hold for all workloads.

## Nuances

- The "equivalent performance compared to state-of-the-art training systems" claim is relative to unnamed comparators; the specific benchmarks and hardware configurations used for comparison are not detailed in the abstract.
- AXLearn is not open-sourced at the time of publication; the paper documents architecture rather than providing a deployable artifact.
