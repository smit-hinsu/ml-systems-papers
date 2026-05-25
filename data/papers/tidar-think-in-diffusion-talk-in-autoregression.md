---
agentic_models: []
arxiv_url: ''
authors:
- Jingyu Liu
- Xin Dong
- Zhifan Ye
- Rishabh Mehta
- Yonggan Fu
- vartika singh
- Ce Zhang
- Pavlo Molchanov
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
principles: []
official_category: ''
openreview_url: https://openreview.net/forum?id=onfxEjoE4L
organizations: []
presentation_type: oral
problem: ''
project_url: ''
reading_status: want-to-read
research_or_industry: ''
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3751_1jPpJd3.pdf
slug: tidar-think-in-diffusion-talk-in-autoregression
status: draft
title: 'TiDAR: Think in Diffusion, Talk in Autoregression'
topics:
- speculative-decoding
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3751
---

<!-- DRAFT: fill in summary before publishing. See docs/summarizing.md -->

## Summary

Abstract
                        
                        
                            
                                
                                    
                                        Diffusion language models hold the promise of fast parallel generation, while autoregressive (AR) models typically excel in quality due to their causal structure aligning naturally with language modeling. This raises a fundamental question: can we achieve a synergy with high throughput, higher GPU utilization, and AR level quality? Existing methods fail to effectively balance these two aspects, either prioritizing AR using a weaker model for sequential drafting (speculative decoding), leading to lower drafting efficiency, or using some form of left-to-right (AR-like) decoding logic for diffusion, which still suffers from quality degradation and forfeits its potential parallelizability.