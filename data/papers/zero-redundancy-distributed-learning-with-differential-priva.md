---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Zhiqi Bu
- Justin Chiu
- Ruixuan Liu
- Sheng Zha
- George Karypis
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/awslabs/fast-differential-privacy
domain:
- llm-training
hardware:
- NVIDIA GPU
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: DP-ZeRO scales differentially private training to GPT-100B with the
  same computation and communication efficiency as standard ZeRO on multiple GPUs.
models_evaluated:
- GPT-100B (target scale)
observations:
  fuse: DP-ZeRO shards gradients, optimizer states, and parameters
    across workers like standard ZeRO, keeping per-GPU memory proportional to shard
    size rather than full model size even under DP noise accumulation.
  balance: Matching standard ZeRO's communication pattern eliminates
    the extra all-reduce rounds that naive DP distributed training introduces, preventing
    communication bottlenecks that would otherwise underutilize GPU compute.
official_category: ''
openreview_url: https://openreview.net/forum?id=VGacNNZfgo
organizations:
- AWS
- Amazon
presentation_type: oral
principles:
- fuse
- balance
problem: Differential privacy training on multiple GPUs is significantly less efficient
  than standard distributed training; existing DP methods are incompatible with ZeRO
  sharding and add high communication overhead.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: ''
slug: zero-redundancy-distributed-learning-with-differential-priva
status: draft
title: Zero redundancy distributed learning with differential privacy
topics:
- fsdp-zero
- all-reduce
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3803
---

## Key Contributions

- **DP-ZeRO**: systematic integration of differential privacy (DP) with Zero Redundancy Optimizer (ZeRO) stages; achieves the same communication and computation efficiency as standard ZeRO while maintaining formal DP guarantees, scaling to models with arbitrary parameter counts (demonstrated at GPT-100B scale).
- **Compatible DP gradient clipping and noise addition**: reformulates per-sample gradient processing to be compatible with ZeRO's gradient sharding; avoids the extra all-reduce passes that naive DP distributed training requires.
- **Mixed-precision DP training**: enables DP training in mixed-precision (FP16/BF16 + FP32 optimizer) without sacrificing DP correctness, matching the throughput efficiency of standard mixed-precision training.
- Code available at https://github.com/awslabs/fast-differential-privacy.

## Trade-offs

- DP noise addition is calibrated to the model size and privacy budget; very large models require proportionally more noise for equivalent privacy guarantees, potentially degrading model quality.
- DP-ZeRO maintains ZeRO's communication pattern but adds per-sample gradient clipping overhead that is unavoidable under DP; this overhead is O(batch size × model size) and may become a bottleneck at very large batch sizes.

## Nuances

- "Same computation and communication efficiency as standard ZeRO" is the goal; actual parity at GPT-100B scale is demonstrated but the absolute throughput numbers and comparison baselines are not specified in the abstract.
- The DP guarantees depend on correct implementation of noise addition and clipping across sharded gradients; numerical correctness in distributed settings requires careful verification.
