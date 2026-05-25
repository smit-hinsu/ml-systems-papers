---
agentic_models: []
arxiv_url: ''
authors:
- Pratyush Patel
- Dayeol Lee
- Shintaro Iwasaki
- Arvind Krishnamurthy
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
openreview_url: https://openreview.net/forum?id=lELxqcgrsN
organizations: []
presentation_type: oral
problem: ''
project_url: ''
reading_status: want-to-read
research_or_industry: ''
slides_url: ''
slug: demystifying-the-mixture-of-experts-serving-tax
status: draft
title: Demystifying the Mixture of Experts Serving Tax
topics:
- moe
- tensor-parallelism
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3764
---

<!-- DRAFT: fill in summary before publishing. See docs/summarizing.md -->

## Summary

Abstract
                        
                        
                            
                                
                                    
                                        Mixture-of-Experts (MoEs) enable massive model sizes but incur higher serving overheads than dense models at the same per-token compute cost. This MoE tax varies with the model architecture, inference phase, and parallelism strategy. We comprehensively study the tax for different MoE models, finding that they perform 2–3× worse than FLOP-equivalent dense models.