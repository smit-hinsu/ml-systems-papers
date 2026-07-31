---
agentic_models: []
arxiv_date: ''
arxiv_url: 'https://arxiv.org/abs/2305.14135'
authors:
- Tianhong Li
- Vibhaalakshmi Sivaraman
- Pantea Karimi
- Lijie Fan
- Mohammad Alizadeh
- Dina Katabi
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- edge-inference
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Outperforms FEC on 3 quality metrics (PSNR, SSIM, LPIPS) with fewer video
  freezes on public video conferencing datasets
models_evaluated: []
observations:
  approximate: Lost video frames are replaced by generative outputs conditioned on
    surrounding frames; approximate reconstruction avoids retransmission round-trips
    at the cost of occasional visual artifacts.
  skip: Generation is conditioned on what was actually received; the model focuses
    compute on the missing regions rather than reprocessing the entire frame.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=GaBGzA7fpe
organizations:
- MIT
presentation_type: oral
principles:
- skip
- approximate
problem: Packet loss in video conferencing causes video freezes; FEC is impractical
  due to bursty Internet losses requiring unpredictable and wasteful redundancy.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: reparo-loss-resilient-generative-codec-for-video-conferencin
status: draft
title: 'REPARO: LOSS-RESILIENT GENERATIVE CODEC FOR VIDEO CONFERENCING'
topics:
- streaming
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3839
---

## Background

Video conferencing uses UDP — no retransmission, so packet loss causes freezes. Forward Error Correction (FEC) adds sender-side redundancy to recover losses, but real Internet loss is bursty and unpredictable: under-provisioned FEC causes freezes, over-provisioned FEC wastes bandwidth. Deep generative models offer an alternative: reconstruct missing frames at the receiver from surrounding context rather than adding redundancy at the sender.

## Key Contributions

- **Reparo generative codec**: uses deep generative models conditioned on received data to reconstruct lost frames or frame regions at the receiver; eliminates dependence on FEC redundancy for packet recovery
- **Conditional generation**: generation is conditioned on all data received so far, incorporating the model's understanding of how people and objects appear and interact visually; produces semantically coherent reconstructions
- **Loss-resilient video conferencing framework**: handles both full-frame loss and partial-frame (block) loss; evaluated on publicly available video conferencing datasets against state-of-the-art FEC baselines
- Outperforms FEC-based methods on PSNR, SSIM, and LPIPS quality metrics and reduces video freeze frequency

## Trade-offs

- Generative reconstruction is computationally more expensive than FEC decoding; requires sufficient receiver-side compute (GPU) for real-time inference.
- Generated frames may hallucinate visual details (e.g., facial expressions, text) that differ from the original, even if perceptually plausible.

## Nuances

- Quality metrics (PSNR, SSIM, LPIPS) measure perceptual similarity; for video conferencing applications, subjective quality and lip-sync accuracy may be more critical measures.
- End-to-end latency of the generative pipeline at inference time is not quantified in the abstract; real-time constraints (sub-100ms) are stringent for video conferencing.
- The generative model requires training on video conferencing data; domain shift to novel environments or unseen speakers may degrade reconstruction quality.