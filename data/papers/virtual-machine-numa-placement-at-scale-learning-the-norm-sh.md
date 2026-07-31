---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Yibo Zhao
- Tianyuan Wu
- Hui Xue
- Qi Chen
- Zhenhua Han
- Zikai Xu
- Yuntai Chang
- Rui Gao
- Steve Deng
- Ray Jui-Hao Chiang
- Mingxia Li
- Yuqing Yang
- Cheng Tan
- Fan Yang
- Peng Cheng
- Yongqiang Xiong
- Lili Qiu
- Lidong Zhou
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- fleet-efficiency
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Catur reduces average resource defect by 34.2%–50.0% vs. default hypervisor
  heuristics, evaluated on 100 million VM production traces.
models_evaluated: []
observations:
  balance: RL-based NUMA placement learns from 100M VM production traces
    to assign VMs to NUMA nodes that minimize remote memory access, reducing average
    resource defect by up to 50% vs. heuristic policies.
  search-ai: Reinforcement learning optimizes a measurable objective (NUMA resource
    defect rate) on production workloads, with drift-aware continuous training adapting
    to evolving VM placement patterns.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=guCUThRvX5
organizations:
- Microsoft Research
presentation_type: oral
principles:
- balance
- search-ai
problem: Poor VM NUMA placement causes up to 30% performance degradation from remote
  memory access; optimal placement at scale is intractable with heuristics.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: ''
slug: virtual-machine-numa-placement-at-scale-learning-the-norm-sh
status: draft
title: 'Virtual Machine NUMA Placement at Scale: Learning the Norm, Shielding the
  Tail'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3777
---

## Background

Server CPUs split cores and memory into NUMA nodes; remote-node memory is 2–3× slower, and a VM whose vCPUs and memory straddle nodes loses 20–30% performance. Placing VMs well is NP-hard bin-packing, and a cloud provider does it for millions of VMs across server generations with different topologies. The heuristics hypervisors ship with generalize poorly across the range of VM sizes and workload mixes in a real fleet.

## Key Contributions

- **Catur RL-based NUMA placement system**: uses reinforcement learning trained on 100 million VM production traces to learn optimal NUMA placement policies that minimize remote memory access across diverse VM configurations and NUMA topologies.
- **Robust action space design**: prevents model collapse under large, sparse VM configuration spaces by constraining and structuring the RL action space.
- **Reward shaping**: addresses learning inefficiency in sparse reward environments by decomposing the NUMA resource defect signal into shaped intermediate rewards.
- **Drift-aware continuous training**: detects shifts in workload patterns and triggers policy updates, maintaining placement quality as VM configurations and tenant mixes evolve over time.
- **Speculative shielding**: proactively identifies tail VM configurations at risk of poor placements and applies conservative fallback policies, mitigating anomalous performance degradation.
- Evaluated on 100M VM production traces; reduces average resource defect by 34.2%–50.0% vs. state-of-the-art hypervisor policies.

## Findings

- Poor NUMA placement causes up to 30% VM performance degradation in production; heuristic hypervisor policies fail to generalize across diverse VM sizes and NUMA structures.
- Drift-aware continuous training is necessary in production: fixed policies degrade as workload patterns evolve without retraining.
- Speculative shielding disproportionately benefits tail VM configurations; average metrics alone underestimate the importance of protecting anomalous cases.

## Trade-offs

- RL training on production traces requires large-scale data collection and continuous retraining infrastructure; the operational cost of maintaining Catur exceeds simpler heuristic policies.
- Speculative shielding uses conservative fallback policies for tail cases, potentially leaving performance gains on the table for those configurations.

## Nuances

- The 34.2%–50.0% resource defect reduction is measured on production traces from a specific cloud environment; data center topology and VM mix diversity at other providers may shift the achievable range.
- The RL model is trained offline on historical traces; real-time adaptation to sudden workload spikes relies on drift detection latency, which is not characterized.
