---
agentic_models: []
arxiv_url: https://arxiv.org/abs/2507.02770
authors:
- Zhongshu Gu
- Enriquillo Valdez
- Salman Ahmed
- Julian James Stephen
- Michael Le
- Hani Jamjoom
- Shixuan Zhao
- Zhiqiang Lin
award: ''
citations: 3
citations_updated: '2026-07-31'
code_url: ''
domain:
- observability
- hardware
hardware:
- NVIDIA GPU (Ampere, Hopper)
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Experiments on 2 GPU architectures (Ampere, Hopper) reveal unprotected
  data transfer paths under GPU-CC threat model; findings disclosed to NVIDIA PSIRT.
models_evaluated:
- AI workloads under GPU-CC
observations:
  measure: NVIDIA ships GPU-CC as a closed box, so a tenant renting untrusted cloud
    GPUs cannot check whether CPU-to-GPU transfers are really encrypted without rebuilding
    the architecture from outside.
official_category: ''
openreview_url: https://openreview.net/forum?id=t9RDCO1aL7
optimization_type: []
organizations:
- IBM Research
- Ohio State University
presentation_type: oral
principles: []
principles_review:
- measure
problem: NVIDIA GPU Confidential Computing is proprietary and opaque, making it hard
  to audit security guarantees for AI workloads running in untrusted clouds.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3741.pdf
slug: blueprint-bootstrap-and-bridge-a-security-look-at-nvidia-gpu
status: draft
title: 'Blueprint, Bootstrap, and Bridge: A Security Look at NVIDIA GPU Confidential
  Computing'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3741
---

## Background

NVIDIA GPU Confidential Computing (GPU-CC) extends Trusted Execution Environments to GPUs, keeping models and inputs encrypted from the cloud operator. It rests on proprietary, undocumented mechanisms: security processors, attestation hardware, encrypted PCIe channels. Whether data moving between the CPU TEE and GPU secure memory is actually protected, or exposed at unguarded bridges, can only be settled by reverse-engineering the architecture.

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
