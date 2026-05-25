---
agentic_models: []
arxiv_url: ''
authors: []
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
- cpu-memory-tradeoff
official_category: ''
openreview_url: https://openreview.net/forum?id=IZaXDwDtL1
organizations: []
presentation_type: oral
problem: ''
project_url: ''
reading_status: want-to-read
research_or_industry: ''
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3834_VmkjzHq.pdf
slug: ship-sram-based-huge-inference-pipelines-for-fast-llm-servin
status: draft
title: 'SHIP: SRAM-Based Huge Inference Pipelines for Fast LLM Serving'
topics:
- kv-cache
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3834
---

<!-- DRAFT: fill in summary before publishing. See docs/summarizing.md -->

## Summary

Abstract
                        
                        
                            
                                
                                    
                                        The proliferation of large language models (LLMs) demands inference systems with both low latency and high efficiency at scale. GPU-based serving relies on HBM for model weights and KV caches, creating a memory bandwidth bottleneck during decode. To break through this bottleneck, we present the first large-scale, SRAM-based LLM inference deployment—Groq’s public cloud—serving hundreds of billions of tokens daily.