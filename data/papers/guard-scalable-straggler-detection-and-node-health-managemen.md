---
agentic_models: []
arxiv_url: ''
authors:
- guanliang liu
- Abhinandan Patni
- congzhu lin
- Zoe Zeng
- Jack Wittmayer
- Yinghong Liu
- josh wu
- Anthony Ko
- Alexander Zhipa
- Ashvin Nihalani
- Binxuan Huang
- Cong Cheng
- Mi Sun
- Vijay rajakumar
- Rejith Joseph
- Parthasarathy Govindarajen
award: ''
citations: null
citations_updated: ''
code_url: ''
date: 2026-05
domain:
- fleet-efficiency
hardware: []
indexed_by: ''
indexed_date: '2026-05-24'
key_results: ''
models_evaluated: []
principles:
- straggler-bubbles
official_category: ''
openreview_url: https://openreview.net/forum?id=JFEwQ821MS
organizations: []
presentation_type: oral
problem: ''
project_url: ''
reading_status: want-to-read
research_or_industry: ''
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3831_b41kyKe.pdf
slug: guard-scalable-straggler-detection-and-node-health-managemen
status: draft
title: 'GUARD: SCALABLE STRAGGLER DETECTION AND NODE HEALTH MANAGEMENT FOR LARGE-SCALE
  TRAINING'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3831
---

<!-- DRAFT: fill in summary before publishing. See docs/summarizing.md -->

## Summary

Abstract
                        
                        
                            
                                
                                    
                                        Training frontier-scale foundation models involves coordinating tens of thousands of GPUs over multi-month runs, where even minor performance degradations can accumulate into substantial efficiency losses. Existing health-check mechanisms, such as NCCL tests or GPU burn-in, primarily focus on functional correctness and often fail to detect fail-slow behaviors that silently degrade system performance. In this paper, we present Guard, a scalable system for detecting stragglers and ensuring node health in large-scale training clusters.