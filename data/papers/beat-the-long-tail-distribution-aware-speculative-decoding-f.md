---
slug: beat-the-long-tail-distribution-aware-speculative-decoding-f
title: "Beat the long tail: Distribution-Aware Speculative Decoding for RL Training"
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
organizations:
- University of Illinois Urbana-Champaign
- UC San Diego
- Stanford University
- University of Chicago
- UC Berkeley
- Cornell University
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3766
openreview_url: https://openreview.net/forum?id=kMeqqPBjSl
arxiv_url: 'https://arxiv.org/abs/2511.13841'
presentation_type: oral
official_category: ''
award: ''
status: draft
reading_status: want-to-read
research_or_industry: research
indexed_by: smithinsu
indexed_date: '2026-05-24'
citations: null
citations_updated: ''
code_url: ''
project_url: ''
slides_url: ''
domain:
- rl-training
hardware:
- GPU
models_evaluated:
- LLM (math/code reasoning)
agentic_models: []
topics:
- speculative-decoding
principles:
- cache
- skip
observations:
  cache: "Suffix tree drafter reuses token patterns from past rollouts, avoiding recomputation of common prefixes across RL training epochs."
  skip: "Length-aware policy assigns aggressive draft budgets only to the long-tail trajectories that dominate makespan, ignoring short ones."
problem: "RL rollout phase is dominated by a small fraction of long trajectories, bottlenecking wall-clock time while most rollouts finish quickly."
key_results: "DAS cuts RL rollout time by up to 50% on math and code tasks with identical training curves, tested on LLMs."
---

## Key Contributions

- **DAS (Distribution-Aware Speculative Decoding)**: Builds an adaptive nonparametric drafter from recent rollouts via an incrementally maintained suffix tree, enabling speculation without altering model outputs during RL post-training.
- **Length-aware speculation policy**: Allocates more aggressive draft budgets to the long-tail trajectories that dominate makespan, exploiting stable prompt-level rollout patterns across epochs.

## Trade-offs

- The suffix tree drafter benefits most when rollout patterns are stable across epochs; early training phases with rapidly shifting distributions may see lower acceptance rates.
- Memory overhead from maintaining the suffix tree grows with vocabulary size and rollout history length.

## Nuances

- DAS preserves identical training curves — the output distribution is unchanged, so it is purely a latency optimization with no accuracy trade-off.
- The 50% speedup applies to the rollout phase only; gradient update time is unaffected.
