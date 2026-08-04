---
agentic_models: []
arxiv_date: 2026-03
arxiv_url: https://arxiv.org/abs/2603.24916
authors:
- Yassien Shaalan
award: ''
citations: 0
citations_updated: '2026-07-31'
code_url: ''
domain:
- edge-inference
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 6.31× smaller flash footprint (~225 kB vs. ~1.4 MB) while retaining ≥95%
  of large-model macro-F1 on three ECG benchmarks; 96.2% accuracy on Speech Commands
models_evaluated: []
observations: {}
official_category: ''
openreview_url: https://openreview.net/forum?id=NrDa5Fu10D
optimization_type: []
organizations:
- Independent Researcher
presentation_type: oral
principles: []
problem: Pointwise convolution mixers dominate flash/SRAM on microcontrollers even
  after INT8 quantization, blocking deployment of competitive CNNs in TinyML settings.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3818_UaGcJ0C.pdf
slug: once-for-all-channel-mixers-hypertinypw-generative-compressi
status: draft
title: 'Once-for-All Channel Mixers (HyperTinyPW): Generative Compression for TinyML'
topics:
- quantization
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3818
---

## Background

TinyML runs neural nets on microcontrollers with kilobytes of flash and SRAM. Pointwise (1×1) convolutions dominate flash footprint in lightweight CNNs like MobileNet: every layer stores its own weight matrix, and even INT8 models overrun MCU budgets. Pruning and quantization shrink each matrix but still keep one per layer.

## Key Contributions

- **HyperTinyPW**: compression-as-generation approach that replaces stored pointwise (PW) convolution weights with a shared micro-MLP that synthesizes PW kernels once at load time from tiny per-layer codes, then caches them for standard INT8 inference
- **Cross-layer latent basis sharing**: a single generator shared across layers removes inter-layer weight redundancy; only PW1 layers are kept in INT8 for morphology stability while all other PW layers are generated on demand
- **TinyML-faithful accounting**: introduces packed-byte accounting that covers generator, heads/factorization, codes, kept PW1, and backbone weights, enabling fair comparison against prior compression methods
- Achieves 6.31× flash reduction at ~225 kB vs. ~1.4 MB CNN baseline while retaining ≥95% macro-F1 on Apnea-ECG, PTB-XL, MIT-BIH; 96.2% accuracy on Speech Commands

## Trade-offs

- One-time synthesis cost at load time adds deployment latency; for applications with very fast cold-start requirements the synthesis overhead may be unacceptable.
- The shared generator must be kept in flash; if the generator itself is large relative to the per-layer code savings, the compression ratio degrades for models with few layers or few PW channels.

## Nuances

- The ≥95% macro-F1 retention threshold is validated on ECG and keyword spotting tasks; transfer to other embedded sensing modalities (e.g., vibration, IMU) is asserted but not evaluated.
- Bootstrap confidence intervals and validation-tuned thresholds are used to make comparisons rigorous, but the single-author study lacks external reproducibility verification at this stage.
