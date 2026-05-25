---
agentic_models: []
arxiv_url: ''
authors:
- Tiyasa Mitra
- Ritika Borkar
- Nidhi Bhatia
- Shivam Raj
- hongkuan zhou
- Yan Ru Pei
- Vishwanath Venkatesan
- Kyle Kranen
- Ramon Matas
- Dheevatsa Mudigere
- Ritchie Zhao
- Maximilian Golub
- Arpan Dutta
- Suresh Nambi
- Sailaja Madduri
- Dharmesh Jani
- Brian Pharris
- Itay Neeman
- Bita Darvish Rouhani
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
- communication-compute-overlap
official_category: ''
openreview_url: https://openreview.net/forum?id=NqC5tcBsa0
organizations: []
presentation_type: oral
problem: ''
project_url: ''
reading_status: want-to-read
research_or_industry: ''
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3819_593EcQk.pdf
slug: beyond-the-buzz-a-pragmatic-take-on-inference-disaggregation
status: draft
title: 'Beyond the Buzz: A Pragmatic Take on Inference Disaggregation'
topics:
- continuous-batching
- kv-cache
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3819
---

<!-- DRAFT: fill in summary before publishing. See docs/summarizing.md -->

## Summary

Abstract
                        
                        
                            
                                
                                    
                                        As inference scales to multi-node deployments, prefill-decode disaggregation — splitting inference into distinct phases — offers a promising path to improving the throughput-interactivity Pareto frontier. Despite growing enthusiasm and a surge of open-source efforts, large-scale deployment of disaggregated serving remains limited due to the complexity of the optimization search space and system-level coordination. In this paper, we present the first systematic study of disaggregated inference at scale, evaluating hundreds of thousands of design points across diverse workloads and hardware configurations.