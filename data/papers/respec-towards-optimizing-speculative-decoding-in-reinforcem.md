---
agentic_models: []
arxiv_date: 2025-10
arxiv_url: https://arxiv.org/abs/2510.26475
authors:
- Qiaoling Chen
- Zijun Liu
- Peng Sun
- Shenggui Li
- Guoteng Wang
- Ziming Liu
- Yonggang Wen
- Siyuan Feng
- Tianwei Zhang
award: ''
citations: 13
citations_updated: '2026-07-31'
code_url: ''
domain:
- rl-training
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 4.5x generation speedup on Qwen 3B–14B models while preserving
  reward convergence and training stability in RL-based LLM adaptation.
models_evaluated:
- Qwen-3B
- Qwen-7B
- Qwen-14B
observations:
  speculate: The RL policy shifts with every training step, so a drafter trained once
    goes stale and its acceptance rate falls away mid-run.
official_category: ''
openreview_url: https://openreview.net/forum?id=HhDSxs7x2R
optimization_type: []
organizations:
- Nanyang Technological University
- Tsinghua University
- Shanghai Qiji Zhifeng Co., Ltd.
- National University of Singapore
- Shanghai Innovation Institute
presentation_type: oral
principles:
- speculate
problem: Speculative decoding in RL training degrades at large batch sizes, suffers
  drafter staleness, and causes policy degradation from drafter-actor misalignment.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3836.pdf
slug: respec-towards-optimizing-speculative-decoding-in-reinforcem
status: draft
title: 'ReSpec: Towards Optimizing Speculative Decoding in Reinforcement Learning
  Systems'
topics:
- speculative-decoding
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3836
---

## Key Contributions

- **Dynamic SD configuration tuning**: adapts speculative decoding parameters (draft length, temperature) per training step based on current batch size and model state, avoiding the diminishing-returns regime at large batches
- **Knowledge distillation drafter evolution**: continuously updates the drafter model via distillation from the current actor to prevent staleness under continual RL policy updates; maintains high token acceptance rates
- **Reward-weighted update**: weights policy gradient updates by rollout rewards to counteract drafter-induced distribution shift that would otherwise degrade policy quality
- ReSpec achieves up to 4.5× speedup on Qwen models (3B–14B) while preserving reward convergence and training stability; generation stage is reduced from >75% of RL training time

## Trade-offs

- Knowledge distillation for drafter evolution adds overhead per training step; the net speedup depends on the balance between distillation cost and acceptance rate improvement.
- Dynamic configuration tuning requires a scheduler that adds decision-making overhead; suboptimal tuning at novel workload patterns may reduce gains.

## Nuances

- RL training with SD is evaluated on Qwen 3B–14B; very large models (>70B) with different batch size constraints may require different calibration of the three mechanisms.
- The 4.5× speedup is the peak figure; average speedup across different RL stages (early vs. late training) is not separately reported in the abstract.
- Drafter staleness is characterized as a distinct failure mode from standard serving SD; the paper is among the first to analyze SD behavior specifically under continual policy updates.
