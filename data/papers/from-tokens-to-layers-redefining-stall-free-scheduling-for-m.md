---
agentic_models: []
arxiv_url: ''
authors:
- Gunjun Lee
- Jiwon Kim
- Jaiyoung Park
- Younjoo Lee
- Jung Ho Ahn
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
openreview_url: https://openreview.net/forum?id=yyDbI3HXco
organizations: []
presentation_type: oral
problem: ''
project_url: ''
reading_status: want-to-read
research_or_industry: ''
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3732_cXYJO0z.pdf
slug: from-tokens-to-layers-redefining-stall-free-scheduling-for-m
status: draft
title: 'From Tokens to Layers: Redefining Stall-Free Scheduling for MoE Serving with
  Layered Prefill'
topics:
- moe
- continuous-batching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3732
---

<!-- DRAFT: fill in summary before publishing. See docs/summarizing.md -->

## Summary

Abstract
                        
                        
                            
                                
                                    
                                        Large Language Model (LLM) inference in production must meet stringent service-level objectives for both time-to-first-token (TTFT) and time-between-token (TBT) while maximizing throughput under fixed compute, memory, and interconnect budgets. Modern serving systems adopt stall-free scheduling techniques such as chunked prefill, which splits long prompt processing along the token dimension and interleaves prefill with ongoing decode iterations. While effective at stabilizing TBT, chunked prefill incurs substantial overhead in Mixture-of-Experts (MoE) models: redundant expert weight loads increase memory traffic by up to \textbf{39\%} and inflate energy consumption.