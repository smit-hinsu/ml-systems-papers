---
agentic_models: []
arxiv_url: ''
authors:
- Jianshu She
- Zonghang Li
- HONGCHAO DU
- Shangyu Wu
- Wenhao Zheng
- Eric Xing
- Zhengzhong Liu
- Huaxiu Yao
- Chun Jason Xue
- Qirong Ho
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
- prefix-reuse
official_category: ''
openreview_url: https://openreview.net/forum?id=dzjCkSEDyG
organizations: []
presentation_type: oral
problem: ''
project_url: ''
reading_status: want-to-read
research_or_industry: ''
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3787_G7LPmPu.pdf
slug: pla-serve-a-prefill-length-aware-llm-serving-system
status: draft
title: 'PLA-Serve: A Prefill-Length-Aware LLM Serving System'
topics:
- continuous-batching
- kv-cache
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3787
---

<!-- DRAFT: fill in summary before publishing. See docs/summarizing.md -->

## Summary

Abstract
                        
                        
                            
                                
                                    
                                        Length-Aware Prefill Serving (LAPS) identifies and disaggregates requests with different prompt lengths in LLM serving to reduce TTFT latency. While recent systems have decoupled the prefill and decode stages to improve throughput, they still rely on unified scheduling policies that fail to adapt to heterogeneous workload characteristics. We observe that prompt-length variations lead to distinct performance bottlenecks, motivating an adaptive scheduling strategy.