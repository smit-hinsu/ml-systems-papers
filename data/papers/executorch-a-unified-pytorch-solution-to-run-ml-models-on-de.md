---
slug: executorch-a-unified-pytorch-solution-to-run-ml-models-on-de
title: "ExecuTorch - A Unified PyTorch Solution to Run ML Models On-Device"
authors:
- Mergen Nachin
- Digant Desai
- Stephen Jia
- Chen Lai
- Mengwei Liu
- Jacob Szwejbka
- Raziel Alvarez
- RJ Ascani
- Dave Bort
- Manuel Candales
- Andrew Caples
- Yanan Cao
- Zhengxu Chen
- Soumith Chintala
- Gregory Comer
- Tanvir Islam
- Songhao Jia
- Tarun Karuturi
- Jack Khuu
- Abhinay Kukkadapu
- Tugsbayasgalan Manlaibaatar
- Andrew Or
- Kimish Patel
- Siddartha Pothapragada
- Lucy Qiu
- Supriya Rao
- Orion Reblitz-Richardson
- Max Ren
- Scott Roy
- Anthony Shoumikhin
- Scott Wolchok
- Guang Yang
- Angela Yi
- Martin Yuan
- Hansong Zhang
- Jack Zhang
- Jerry Zhang
- Shunting Zhang
- Cagatay Bilgin
organizations:
- Meta
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3768
openreview_url: https://openreview.net/forum?id=jmE5nwC9kb
arxiv_url: 'https://arxiv.org/abs/2605.08195'
presentation_type: oral
official_category: ''
award: ''
status: draft
reading_status: want-to-read
research_or_industry: industry
indexed_by: smithinsu
indexed_date: '2026-05-24'
citations: null
citations_updated: ''
code_url: ''
project_url: ''
slides_url: ''
domain:
- llm-serving
hardware:
- Microcontrollers
- Mobile SoCs
- Wearables
models_evaluated:
- LLMs
- VLMs
agentic_models: []
topics:
- quantization
principles:
- fuse
- tier
observations:
  fuse: "Sub-graph delegation keeps tensors in accelerator-native formats, avoiding costly CPU-GPU copies for each heterogeneous SoC component in the serving pipeline."
  tier: "Static memory planning for microcontroller targets eliminates dynamic allocations and maximizes SRAM reuse across operators at inference time."
problem: "Edge ML deployment is fragmented across hardware, requiring model conversion outside PyTorch and blocking rapid iteration from research to production."
key_results: "ExecuTorch ships LLMs on Meta AI wearables and smartphones, scaling from <1MB microcontrollers to multi-accelerator SoCs with PyTorch-native semantics."
---

## Key Contributions

- **ExecuTorch framework**: A unified PyTorch-native deployment pipeline for edge AI that preserves PyTorch semantics while enabling pluggable execution backends for diverse accelerators (NPUs, DSPs, GPUs).
- **Heterogeneous backend delegation**: Sub-graph delegation allows portions of a model to be lowered to device-specific backends (e.g., Core ML, QNN, XNNPACK) while the rest runs portably.
- **Quantization and memory optimization**: Built-in quantization API and static memory planning for embedded targets where dynamic allocation is infeasible.

## Trade-offs

- The PyTorch-native approach requires ahead-of-time export (torch.export), which has limitations with dynamic control flow compared to eager mode.
- Pluggable backend delegation adds integration complexity; each new hardware target requires a backend delegate implementation.

## Nuances

- ExecuTorch is production-deployed at Meta for wearables and smartphones, making it an industry system paper rather than a research-only proposal.
- The framework intentionally bridges research-to-production validation by enabling deployment behavior testing within PyTorch.
