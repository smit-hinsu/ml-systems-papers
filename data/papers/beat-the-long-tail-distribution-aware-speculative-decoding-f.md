---
agentic_models: []
arxiv_url: https://arxiv.org/abs/2511.13841
authors:
- Zelei Shao
- Vikranth Srivatsa
- Sanjana Srivastava
- Qingyang Wu
- Alpay Ariyak
- Xiaoxia wu
- Ameen Patel
- Jue Wang
- Percy Liang
- Tri Dao
- Ce Zhang
- Yiying Zhang
- Ben Athiwaratkun
- Chenfeng Xu
- Junxiong Wang
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- rl-training
hardware:
- GPU
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: DAS cuts RL rollout time by up to 50% on math and code tasks with identical
  training curves, tested on LLMs.
models_evaluated:
- LLM (math/code reasoning)
observations:
  cache: Suffix tree drafter reuses token patterns from past rollouts, avoiding recomputation
    of common prefixes across RL training epochs.
  skip: Length-aware policy assigns aggressive draft budgets only to the long-tail
    trajectories that dominate makespan, ignoring short ones.
  speculate: Suffix-tree drafter models the RL rollout long-tail token distribution;
    high acceptance rates on rare tokens close the gap between distribution-naive
    speculation and optimal throughput.
official_category: ''
openreview_url: https://openreview.net/forum?id=kMeqqPBjSl
organizations:
- University of Illinois Urbana-Champaign
- UC San Diego
- Stanford University
- University of Chicago
- UC Berkeley
- Cornell University
presentation_type: oral
principles:
- cache
- skip
- speculate
problem: RL rollout phase is dominated by a small fraction of long trajectories, bottlenecking
  wall-clock time while most rollouts finish quickly.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3766.pdf
slug: beat-the-long-tail-distribution-aware-speculative-decoding-f
status: draft
title: 'Beat the long tail: Distribution-Aware Speculative Decoding for RL Training'
topics:
- speculative-decoding
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3766
---

## Background

RL post-training uses a rollout phase where the model generates many candidate responses to training prompts. Rollout lengths vary enormously — a math problem might take 50 or 5,000 tokens — so a few long stragglers dominate wall-clock time while the GPU idles waiting for the batch. Speculative decoding could speed individual generations, but standard draft models assume a stable token distribution. During RL training the target distribution shifts every gradient step, collapsing acceptance rates for static drafters.

## Key Contributions

- **DAS (Distribution-Aware Speculative Decoding)**: Builds an adaptive nonparametric drafter from recent rollouts via an incrementally maintained suffix tree, enabling speculation without altering model outputs during RL post-training.
- **Length-aware speculation policy**: Allocates more aggressive draft budgets to the long-tail trajectories that dominate makespan, exploiting stable prompt-level rollout patterns across epochs.

## Trade-offs

- The suffix tree drafter benefits most when rollout patterns are stable across epochs; early training phases with rapidly shifting distributions may see lower acceptance rates.
- Memory overhead from maintaining the suffix tree grows with vocabulary size and rollout history length.

## Nuances

- DAS preserves identical training curves — the output distribution is unchanged, so it is purely a latency optimization with no accuracy trade-off.
- The 50% speedup applies to the rollout phase only; gradient update time is unaffected.