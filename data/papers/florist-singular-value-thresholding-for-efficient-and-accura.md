---
agentic_models: []
arxiv_date: 2025-06
arxiv_url: https://arxiv.org/abs/2506.09199
authors:
- Hariharan Ramesh
- Jyotikrishna Dass
award: ''
citations: 3
citations_updated: '2026-07-31'
code_url: ''
domain:
- llm-training
hardware:
- A100
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 3× lower communication vs. FFA-LoRA and 39× vs. FLoRA; 227× vs. full
  fine-tuning with 8 clients; competitive accuracy on MMLU with A100 MIG slices.
models_evaluated:
- LLaMA-3.2-1B
- TinyLLaMA
- LLaMA-7B
observations: {}
official_category: ''
openreview_url: https://openreview.net/forum?id=GTZRs756YJ
optimization_type: []
organizations:
- University of Arizona
presentation_type: oral
principles: []
problem: Federated LoRA aggregation either adds noise from averaging, requires large
  adapter uploads, or demands full weight-matrix decomposition at the server.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3840_BwPF7aI.pdf
slug: florist-singular-value-thresholding-for-efficient-and-accura
status: draft
title: 'FLoRIST: Singular Value Thresholding for Efficient and Accurate Federated
  Fine-Tuning of Large Language Models'
topics:
- fsdp-zero
- quantization
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3840
---

## Background

Federated fine-tuning trains across clients (hospitals, phones, edge devices) that never share raw data. LoRA keeps uploads small — each client sends a low-rank A/B adapter pair — but averaging adapters introduces cross-term noise: (A₁B₁ + A₂B₂)/2 is not the average of the underlying weight updates. Aggregating correctly instead means rebuilding the full O(d²) weight matrix on the server, which costs too much.

## Key Contributions

- **Intermediate-space SVD aggregation**: Stacks local LoRA adapters from all clients and performs SVD within the compact intermediate space (size r×clients) rather than reconstructing the full d×d weight-update matrix, keeping server-side compute tractable
- **Singular value thresholding (SVT)**: Applies an energy-based truncation criterion — retaining the top-p singular components where ∑(top-p)² / ∑(all)² ≥ τ — to automatically determine the global adapter rank, avoiding manual rank selection
- **Noise-free aggregation**: Uses weighted stacking to avoid cross-term noise present in simpler averaging baselines (FedAvg-LoRA), producing mathematically correct aggregation of local adapter information
- **Homogeneous and heterogeneous client support**: The same aggregation pipeline handles clients with different compute budgets and local dataset sizes; evaluated on 4 A100 MIG slices (20GB each) across diverse NLP datasets

## Trade-offs

- Stacking all client adapters at the server still requires O(num_clients × r × d) memory; with many clients or large d, server memory pressure can grow.
- Tuning the SVT threshold τ requires a held-out validation set on the server, which may not be available in all federated settings.

## Nuances

- Experiments use 4 simulated clients on a single machine; true federated deployments with network latency and straggler clients may behave differently.
- Comparison baselines (FFA-LoRA, FLoRA) have different accuracy–efficiency trade-offs; FLoRIST is Pareto-dominant on the communication/accuracy frontier, not universally best on accuracy alone.
