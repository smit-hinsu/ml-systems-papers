---
slug: blueprint-bootstrap-and-bridge-a-security-look-at-nvidia-gpu
title: "Blueprint, Bootstrap, and Bridge: A Security Look at NVIDIA GPU Confidential Computing"
authors:
- Zhongshu Gu
- Enriquillo Valdez
- Salman Ahmed
- Julian James Stephen
- Michael Le
- Hani Jamjoom
- Shixuan Zhao
- Zhiqiang Lin
organizations:
- IBM Research
- Ohio State University
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3741
openreview_url: https://openreview.net/forum?id=t9RDCO1aL7
arxiv_url: 'https://arxiv.org/abs/2507.02770'
presentation_type: oral
official_category: ''
award: ''
status: draft
reading_status: want-to-read
research_or_industry: research
indexed_by: smithinsu
indexed_date: '2026-05-24'
citations: null
citations_updated: ''
code_url: ''
project_url: ''
slides_url: ''
domain:
- observability
hardware:
- NVIDIA GPU (Ampere, Hopper)
models_evaluated:
- AI workloads under GPU-CC
agentic_models: []
topics: []
principles:
- cache
observations:
  cache: "Systematic reverse-engineering of GPU-CC architecture reveals redundant trust establishment steps and unprotected data paths across the CPU-GPU bridge."
problem: "NVIDIA GPU Confidential Computing is proprietary and opaque, making it hard to audit security guarantees for AI workloads running in untrusted clouds."
key_results: "Targeted experiments on Ampere/Hopper GPUs reveal unprotected data transfer paths under the GPU-CC threat model; findings disclosed to NVIDIA PSIRT."
---

## Key Contributions

- **Blueprint reconstruction**: A coherent reverse-engineered view of NVIDIA GPU-CC architecture, documenting specialized engines (security processors, attestation hardware) that underpin its security mechanisms.
- **Bootstrap analysis**: Documents how hardware and software components coordinate to establish GPU-CC protections during initialization.
- **Bridge security experiments**: Targeted tests showing whether data transfers between trusted CPU and GPU domains remain protected, with responsible disclosure of all findings to NVIDIA PSIRT.

## Trade-offs

- The analysis is based on black-box experimentation; some architectural details may be incomplete or change across GPU generations.
- Security analysis covers only the threat model defined by NVIDIA for GPU-CC; side-channel or physical attacks are out of scope.

## Nuances

- GPU-CC aims to make enabling confidential compute seamless for end users, but this seamlessness comes at the cost of architectural transparency that security researchers need.
- Findings were responsibly disclosed; paper does not publish full exploit details.
