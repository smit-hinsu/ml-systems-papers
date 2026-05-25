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
- llm-driven-optimization
official_category: ''
openreview_url: https://openreview.net/forum?id=gEbKQeIdxB
organizations: []
presentation_type: oral
problem: ''
project_url: ''
reading_status: want-to-read
research_or_industry: ''
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3780.pdf
slug: optimizing-deployment-configurations-for-llm-inference
status: draft
title: Optimizing Deployment Configurations for LLM Inference
topics:
- tensor-parallelism
- pipeline-parallelism
- autotuning
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3780
---

<!-- DRAFT: fill in summary before publishing. See docs/summarizing.md -->

## Summary

Abstract
                        
                        
                            
                                
                                    
                                        Meta's Large Language Models (LLMs)---the Llama model family---serve nearly one billion monthly active users. Deploying these models for inference involves navigating a complex design space that spans diverse hardware options (e.g., H100, H200, MI300X), multiple parallelism strategies (tensor, pipeline, expert, context, and data parallelism), and nuanced runtime choices (e.g., continuous batching versus prefill-decode disaggregation)---all while leveraging workload-specific characteristics and meeting stringent service level objectives (SLOs). This paper presents insights we gained from developing and applying a systematic approach to analyze millions of deployment configurations and identify those that maximize throughput while meeting latency SLOs.