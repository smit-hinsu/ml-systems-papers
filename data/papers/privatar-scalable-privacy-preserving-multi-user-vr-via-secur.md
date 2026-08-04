---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Minchen Yu
- Rui Yang
- Chaobo Jia
- Zhaoyuan Su
- Sheng Yao
- Tingfeng Lan
- Yuchen Yang
- Zirui Wang
- Yue Cheng
- Wei Wang
- Ao Wang
- Ruichuan Chen
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/georgia-tech-synergy-lab/Privatar
domain:
- edge-inference
hardware:
- Meta Quest Pro
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: 2.37× more concurrent users on Meta Quest Pro at 5.7–6.5% higher reconstruction
  loss and ~9% energy overhead vs. local reconstruction baseline
models_evaluated: []
observations: {}
official_category: ''
openreview_url: https://openreview.net/forum?id=WjJfnNhY65
optimization_type: []
organizations:
- The Chinese University of Hong Kong, Shenzhen
- University of Virginia
- Hong Kong University of Science and Technology
- Alibaba Group
- Nokia Bell Labs
presentation_type: oral
principles: []
problem: Multi-user VR avatar reconstruction on headsets limits concurrent users;
  offloading to local untrusted devices risks leaking sensitive facial expression
  data.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3801_3ox1dQR.pdf
slug: privatar-scalable-privacy-preserving-multi-user-vr-via-secur
status: draft
title: 'Privatar: Scalable Privacy-preserving Multi-user VR via Secure Offloading'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3801
---

## Background

VR headsets like Meta Quest Pro reconstruct a neural avatar for each participant in real time, and the on-device GPU saturates with a few concurrent users. Offloading to a nearby edge device would scale capacity but ships raw facial expression data — intimate biometrics — to an untrusted machine. Differential privacy masks individual signals, but worst-case per-frame noise destroys reconstruction fidelity.

## Key Contributions

- **Horizontal Partitioning (HP)**: Decomposes avatar reconstruction in the DCT frequency domain; high-energy (visually significant) components stay on-device while low-energy components are offloaded, empirically limiting information leakage to insensitive frequency bands.
- **Distribution-Aware Minimal Perturbation (DAMP)**: Tracks each user's expression distribution online and applies the minimum noise needed for differential privacy, significantly reducing utility degradation compared to worst-case LDP noise that treats every frame independently.
- **Formal + empirical privacy guarantees**: Privatar provides provable differential privacy guarantees against arbitrary adversaries while remaining robust against empirical expression identification attacks and NN-based attackers.

## Trade-offs

- DAMP requires tracking each user's expression distribution over time; this adds per-user state maintenance overhead and a warm-up period before privacy guarantees reach their stated tightness.
- The 5.7–6.5% reconstruction loss increase is the cost of privacy; applications requiring photorealistic avatar fidelity may find this loss unacceptable compared to on-device reconstruction.

## Nuances

- The 2.37× concurrent user gain is measured on Meta Quest Pro under specific network conditions; gains on other headsets or higher-latency networks may differ significantly.
- Privacy guarantees for DAMP hold under the assumption that user expression distributions are slowly changing and trackable; sudden behavioral shifts may temporarily weaken the privacy bound until distribution tracking re-converges.