---
agentic_models: []
arxiv_url: ''
authors:
- Jiayi Yuan
- Cameron Shinn
- Kai Xu
- Jingze Cui
- George Klimiashvili
- Guangxuan Xiao
- Perkz Zheng
- Bo Li
- Zhou Yuxin
- Zhouhai Ye
- Weijie You
- Tian Zheng
- Dominic Brown
- Pengbo Wang
- Markus Hoehnerbach
- Richard Cai
- Julien Demouth
- John D. Owens
- Xia Hu
- Song Han
- Timmy Liu
- Huizi Mao
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
- attention-sparsity
official_category: ''
openreview_url: https://openreview.net/forum?id=6INSBXTQ4x
organizations: []
presentation_type: oral
problem: ''
project_url: ''
reading_status: want-to-read
research_or_industry: ''
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3854.pdf
slug: blasst-dynamic-blocked-attention-sparsity-via-softmax-thresh
status: draft
title: 'BLASST: Dynamic BLocked Attention Sparsity via Softmax Thresholding'
topics:
- sparse-attention
- kv-cache
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3854
---

<!-- DRAFT: fill in summary before publishing. See docs/summarizing.md -->

## Summary

Abstract
                        
                        
                            
                                
                                    
                                        The growing demand for long-context inference capabilities in Large Language Models (LLMs) has intensified the computational and memory bottlenecks inherent to the self-attention mechanism. To address this challenge, we introduce BLASST, a drop-in, dynamic sparse attention mechanism that accelerates inference by using only a fixed scalar threshold to skip attention blocks. Our method targets practical inference deployment by removing the barriers to adoption present in existing works.