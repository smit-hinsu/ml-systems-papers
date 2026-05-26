---
title: 'FLoRIST: Singular Value Thresholding for Efficient and Accurate Federated Fine-Tuning of Large Language Models'
slug: florist-singular-value-thresholding-for-efficient-and-accura
authors:
- Hariharan Ramesh
- Jyotikrishna Dass
organizations:
- University of Arizona
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3840
openreview_url: https://openreview.net/forum?id=GTZRs756YJ
arxiv_url: https://arxiv.org/abs/2506.09199
slides_url: ''
code_url: ''
project_url: ''
official_category: ''
presentation_type: oral
award: ''
arxiv_date: '2025-06'
domain:
- llm-training
topics:
- fsdp-zero
- quantization
principles:
- cache
- fuse
observations:
  cache: SVD is performed on the compact stacked-adapter space rather than constructing the full weight-update matrix, avoiding O(d²) computation and memory that scales with model width.
  fuse: Clients transmit only low-rank adapter pairs (r × d) rather than full weight-update matrices; FLoRIST-E achieves 3× lower communication than FFA-LoRA and 39× lower than FLoRA.
hardware:
- A100
models_evaluated:
- LLaMA-3.2-1B
- TinyLLaMA
- LLaMA-7B
agentic_models: []
citations: null
citations_updated: ''
research_or_industry: research
problem: Federated LoRA aggregation either introduces noise via simple averaging, requires large stacked adapter uploads, or demands expensive full weight-matrix decomposition at the server.
key_results: 3× lower communication vs. FFA-LoRA and 39× vs. FLoRA; 227× vs. full fine-tuning with 8 clients; competitive accuracy on MMLU with A100 MIG slices.
status: draft
reading_status: want-to-read
indexed_by: smithinsu
indexed_date: '2026-05-25'
---

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
