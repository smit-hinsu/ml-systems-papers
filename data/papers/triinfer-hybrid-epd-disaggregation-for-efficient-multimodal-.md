---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Xianzhe Dong
- Tongxuan Liu
- Yuting Zeng
- Weizhe Huang
- Xiaoyang Zhao
- Siyu Wu
- Liangyu Liu
- Yang Liu
- Yu Wu
- Hailong Yang
- Ke Zhang
- Jing Li
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/dongxianzhe/triinfer
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 3.7× higher inference throughput vs. vLLM and SGLang while meeting
  90th-percentile SLO under real multimodal workloads.
models_evaluated: []
observations:
  balance: Scheduling encode, prefill, and decode onto separate heterogeneous
    instances eliminates resource contention between vision encoding (compute-bound)
    and token decoding (memory-bandwidth-bound), raising overall GPU utilization.
  pipeline: Stage-level batching enables parallel execution of visual
    and language model stages; visual encoding and language prefill can proceed concurrently
    on separate instances.
official_category: ''
openreview_url: https://openreview.net/forum?id=nNovi8fvGN
organizations:
- University of Science and Technology of China
- JD.com
- Beihang University
presentation_type: oral
principles:
- balance
- pipeline
problem: Monolithic MLLM serving couples image encoding, prefill, and decode on the
  same GPUs, causing resource contention and low utilization due to heterogeneous
  stage demands.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: triinfer-hybrid-epd-disaggregation-for-efficient-multimodal-
status: draft
title: 'TriInfer: Hybrid EPD Disaggregation for Efficient Multimodal Large Language
  Model Inference'
topics:
- continuous-batching
- pipeline-parallelism
- kv-cache
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3756
---

## Key Contributions

- **Hybrid Encode-Prefill-Decode (EPD) disaggregation**: schedules the three MLLM inference stages onto separate, heterogeneous GPU instances, allowing each stage to be independently scaled and optimized for its distinct compute/memory characteristics.
- **Stage-level batching strategy**: batches requests independently per stage; enables parallel execution of visual encoding and language prefill across separate instances, improving load balance and reducing inter-stage idle time.
- **Flexible resource reallocation**: dynamically adjusts GPU allocation per stage based on workload demand, resolving bottlenecks that shift between encode, prefill, and decode under diverse multimodal traffic patterns.
- Evaluated on real multimodal inference workloads; achieves up to 3.7× higher throughput than vLLM and SGLang while meeting the 90th-percentile request SLO.

## Trade-offs

- Three-stage disaggregation introduces cross-instance KV-cache and intermediate feature transfer overhead; the benefit depends on whether stage heterogeneity savings exceed communication costs.
- Separate encode instances require managing an additional GPU pool and routing layer; operational complexity is higher than monolithic serving systems.

## Nuances

- Evaluation is on "real multimodal inference workloads" but the specific models, image resolutions, and request mix are not detailed in the abstract; results may not generalize to all MLLM configurations.
- The paper targets serving (inference); training disaggregation with heterogeneous stages is a different problem not addressed here.
