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
citations: null
citations_updated: ''
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
  balance: Drafter staleness under continual actor updates causes policy divergence;
    evolving the drafter via knowledge distillation keeps it aligned with the current
    actor, maintaining accept rates.
  cache: Dynamic SD configuration tuning avoids fixed-overhead speculative decoding
    at large batch sizes where drafting yields diminishing returns; configurations
    are tuned per-step.
  speculate: Draft model is updated alongside the RL policy to track its distribution
    shift; keeping drafter and target in sync prevents acceptance rate collapse as
    the target model changes during RL training.
official_category: ''
openreview_url: https://openreview.net/forum?id=HhDSxs7x2R
organizations:
- Nanyang Technological University
- Tsinghua University
- Shanghai Qiji Zhifeng Co., Ltd.
- National University of Singapore
- Shanghai Innovation Institute
presentation_type: oral
principles:
- cache
- balance
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

## Background

RL-based LLM fine-tuning (RLHF, GRPO, PPO) generates thousands of rollout sequences per gradient step — autoregressive generation consumes over 75% of wall-clock training time. Speculative decoding is an obvious accelerant, but RL continuously updates the actor model. A draft model calibrated at step 0 diverges from the actor by step 100; acceptance rates collapse, and at the large batch sizes typical in RL rollouts the verifier is already compute-saturated even with a perfect drafter.

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