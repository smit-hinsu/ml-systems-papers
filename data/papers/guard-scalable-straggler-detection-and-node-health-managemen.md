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
domain:
- fleet-efficiency
- observability
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: 1.7× FLOPs utilization gain; training step variance 20%→1% on tens of
  thousands of GPUs in multi-month foundation model pretraining.
models_evaluated: []
observations:
  cache: Offline node sweeping qualifies nodes before they join production
    jobs, preventing straggler-induced checkpoint rollbacks that waste compute already
    spent on the aborted run segment.
  balance: Step-time variance of 20% means fast nodes wait for the slowest
    each iteration; remediating fail-slow nodes before the sync barrier eliminates
    these stall bubbles.
official_category: ''
openreview_url: https://openreview.net/forum?id=JFEwQ821MS
organizations:
- Amazon
presentation_type: oral
principles:
- balance
- cache
problem: Fail-slow GPU behaviors silently inflate step-time variance; burn-in tests
  miss performance regressions that accumulate over multi-month training runs.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3831_b41kyKe.pdf
slug: guard-scalable-straggler-detection-and-node-health-managemen
status: draft
title: 'GUARD: SCALABLE STRAGGLER DETECTION AND NODE HEALTH MANAGEMENT FOR LARGE-SCALE
  TRAINING'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3831
---

## Background

Distributed training is synchronous: every GPU waits at each step for the slowest node. Hardware crashes are easy to detect; "fail-slow" nodes are not — they pass all functional health checks (NCCL tests, GPU burn-in) but run 5–20% slower due to degradation or thermal throttling. Standard burn-in checks whether a node works, not whether it keeps up with the fleet. Over multi-month pretraining runs at tens of thousands of GPUs, even a few fail-slow nodes compound into significant utilization loss.

## Key Contributions

- **Online performance monitoring**: Lightweight per-step telemetry collected during active training to continuously track step-time distributions across nodes; detects acute failures and gradual degradation in real time without requiring a separate diagnostic pass.
- **Offline node-sweep mechanism**: Systematically runs performance qualification workloads on candidate nodes before they join production training jobs; filters out nodes exhibiting fail-slow behavior that functional tests (NCCL, GPU burn-in) miss because they never fail outright.
- **Two-tier detection architecture**: Combining online monitoring (catches failures during a run) with offline sweeping (catches pre-existing degradation at onboarding) covers both acute and long-running failure modes, raising mean time to failure and reducing debugging overhead.
- Deployed on production foundation model pretraining at scale (tens of thousands of GPUs, multi-month runs); reduced training step variance from 20% to 1% and improved mean FLOPs utilization by up to 1.7×.

## Trade-offs

- Offline node sweeping adds pre-job qualification overhead; for short training runs the qualification time may not be amortized by the utilization gains during the job.
- The online monitoring overhead is described as lightweight but collecting per-step telemetry at tens-of-thousands-of-GPU scale still adds some coordination cost.

## Nuances

- Specific hardware and cluster topology are not disclosed; the fail-slow signature profiles and detection thresholds may need recalibration for different GPU generations or interconnect types.
- The 1.7× FLOPs utilization improvement is an upper bound (best case); average improvement and the distribution across job types are not detailed in the abstract.
- GUARD detects stragglers but remediation (eviction, replacement, rebalancing) is outside the paper's main scope; the operational pipeline for acting on detections is not fully specified.