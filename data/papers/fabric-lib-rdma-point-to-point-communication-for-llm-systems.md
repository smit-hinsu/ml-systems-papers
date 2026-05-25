---
agentic_models: []
arxiv_url: ''
authors:
- Nandor Licker
- Kevin Hu
- Vladimir Zaytsev
- Lequn Chen
award: ''
citations: null
citations_updated: ''
code_url: ''
date: 2026-05
domain:
- llm-serving
- llm-training
hardware: []
indexed_by: ''
indexed_date: '2026-05-24'
key_results: ''
models_evaluated: []
principles:
- communication-compute-overlap
official_category: ''
openreview_url: https://openreview.net/forum?id=SjVa05wEiY
organizations: []
presentation_type: oral
problem: ''
project_url: ''
reading_status: want-to-read
research_or_industry: ''
slides_url: ''
slug: fabric-lib-rdma-point-to-point-communication-for-llm-systems
status: draft
title: 'fabric-lib: RDMA Point-to-Point Communication for LLM Systems'
topics:
- all-reduce
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3807
---

<!-- DRAFT: fill in summary before publishing. See docs/summarizing.md -->

## Summary

Abstract
                        
                        
                            
                                
                                    
                                        Emerging Large Language Model (LLM) system patterns, such as disaggregated inference, Mixture-of-Experts (MoE) routing, and asynchronous reinforcement fine-tuning, require flexible point-to-point communication beyond simple collectives. Existing implementations are locked to specific Network Interface Controllers (NICs), hindering integration into inference engines and portability across hardware providers. We present fabric-lib, which bridges the functionality of common NICs to expose a uniform interface.