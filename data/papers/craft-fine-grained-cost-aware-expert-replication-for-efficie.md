---
agentic_models: []
arxiv_url: ''
authors:
- Adrian Zhao
- Zhenkun Cai
- Zhenyu Song
- Lingfan Yu
- Haozheng Fan
- Jun Wu
- Yida Wang
- Nandita Vijaykumar
award: ''
citations: null
citations_updated: ''
code_url: ''
date: 2026-05
domain:
- llm-serving
hardware: []
indexed_by: ''
indexed_date: '2026-05-24'
key_results: ''
models_evaluated: []
principles:
- straggler-bubbles
official_category: ''
openreview_url: https://openreview.net/forum?id=zdRvzU9ZCe
organizations: []
presentation_type: oral
problem: ''
project_url: ''
reading_status: want-to-read
research_or_industry: ''
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3731_3lg6KXh.pdf
slug: craft-fine-grained-cost-aware-expert-replication-for-efficie
status: draft
title: 'CRAFT: Fine-Grained Cost-Aware Expert Replication For Efficient Mixture-of-Experts
  Serving'
topics:
- moe
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3731
---

<!-- DRAFT: fill in summary before publishing. See docs/summarizing.md -->

## Summary

Abstract
                        
                        
                            
                                
                                    
                                        Mixture-of-Experts (MoE) has recently emerged as the mainstream architecture for efficiently scaling large language models while maintaining near-constant computational cost. Expert parallelism distributes parameters by partitioning experts across devices, but this introduces token-level load imbalance during inference. Expert replication is a widely adopted load-balancing technique in serving frameworks that alleviates load imbalance in large-scale deployments by replicating experts with high loads.