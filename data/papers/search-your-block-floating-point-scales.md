---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Tanmaey Gupta
- Hayden Prairie
- Shirley Wu
- Reyna Abhyankar
- Qingyang Wu
- Austin Silveria
- Pragaash Ponnusamy
- Jue Wang
- Ben Athiwaratkun
- Leon Song
- Tri Dao
- Daniel Y. Fu
- Chris De Sa
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: ScaleSearch reduces NVFP4 quantization error by 27%; ScaleSearchAttention
  improves Wikitext-2 PPL by 0.77 for Llama 3.1 70B; MATH500 up 15 pts for Qwen3-8B.
models_evaluated:
- Llama 3.1 70B
- Qwen3-8B
observations:
  tier: Fine-grained scale search uses mantissa bits in BFP microscaling formats to
    minimize quantization error for the block value distribution, reducing the gap
    between stored and effective precision.
  fuse: ScaleSearchAttention uses 4-bit representation for attention, reducing memory
    bandwidth while maintaining near-zero performance loss via optimized scale
    selection.
official_category: ''
openreview_url: https://openreview.net/forum?id=innqECyZPK
organizations:
- Together AI
- Cornell University
presentation_type: oral
principles:
- tier
- fuse
problem: Standard BFP quantization uses maximum-magnitude scale factors that are suboptimal
  for the actual value distribution, causing unnecessary quantization error.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: search-your-block-floating-point-scales
status: draft
title: 'Search Your Block Floating Point Scales!'
topics:
- quantization
- sparse-attention
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3770
---

## Background

Block floating point (BFP) quantization assigns a shared scale factor to a block of values so only mantissa bits need to be stored per value. NVIDIA's NVFP4 format (native on Blackwell GPUs) uses this approach for 4-bit inference. The standard scale choice — the maximum-magnitude value in the block — prevents overflow but wastes mantissa precision on blocks with skewed distributions where most values are far smaller than the max.

## Key Contributions

- **ScaleSearch**: fine-grained scale factor search that uses mantissa bits in BFP microscaling formats to minimize quantization error for the given block value distribution; reduces NVFP4 quantization error by 27%
- **ScaleSearchAttention**: NVFP4-based attention algorithm combining ScaleSearch with adapted prior techniques; achieves near-zero performance loss for causal language modeling; improves Wikitext-2 PPL by up to 0.77 for Llama 3.1 70B
- **Integration with PTQ**: ScaleSearch is compatible with Post-Training Quantization pipelines; improves MATH500 performance by up to 15 points for Qwen3-8B
- Leverages first-class GPU hardware support for BFP microscaling formats (NVFP4) now available in modern accelerators

## Trade-offs

- Scale search adds compute overhead compared to maximum-magnitude scale selection; the search cost must be amortized over inference requests.
- NVFP4 format support is hardware-specific; benefits apply primarily to hardware with native BFP acceleration (e.g., NVIDIA Blackwell or Hopper with BFP support).

## Nuances

- The 15-point MATH500 improvement is the upper bound across evaluated configurations; average improvement across benchmarks and models is not separately stated.
- Scale search operates offline (as part of PTQ calibration) rather than dynamically at inference time; activation distributions at inference may differ from calibration data.
