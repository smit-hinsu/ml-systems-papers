---
agentic_models: []
arxiv_date: 2025-11
arxiv_url: https://arxiv.org/abs/2511.16964
authors:
- Kirill Nagaitsev
- Luka Grbcic
- Samuel Williams
- Costin Iancu
award: ''
citations: 4
citations_updated: '2026-07-31'
code_url: https://github.com/pike-project/pike
domain:
- ml-kernels
- agentic-inference
hardware:
- H100
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: PIKE-B achieves 2.88× speedup over PyTorch Eager and 1.85× over torch.compile
  on H100 across 30+ model tasks via exploit-heavy LLM multi-agent optimization
models_evaluated:
- DeepSeek-V3
- Llama-3
- Mamba-2
observations:
  search-ai: A generated kernel can be compiled, run, and diffed against the reference,
    so a wrong candidate costs one benchmark run rather than expert review.
official_category: ''
openreview_url: https://openreview.net/forum?id=MJxhiX3sSd
optimization_type: []
organizations:
- Lawrence Berkeley National Laboratory
presentation_type: oral
principles:
- search-ai
problem: Writing optimized CUDA/Triton kernels requires deep hardware expertise; no
  framework exists for AI agents to iteratively generate, test, and improve them.
project_url: ''
reading_status: read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3823.pdf
slug: pike-pytorch-llm-agents
status: under-review
title: Optimizing PyTorch Inference with LLM-Based Multi-Agent Systems
topics:
- llm-code-generation
- autotuning
- kernel-fusion
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3823
---

## Key Contributions

- **PIKE logical framework**: five-stage pipeline — Library, Seed Selection, Prompt Construction, Evaluation, Post-processing — for comparing multi-agent PyTorch optimization strategies; formalizes the explore/exploit ratio as the primary design variable
- **Exploit-heavy + Error-Fixing Agent (EFA) combination**: PIKE-B strategy with high exploitation ratio achieves 2.88× speedup over PyTorch Eager and 1.85× over torch.compile on H100; EFA corrects invalid solutions by re-prompting up to 5 times
- **KernelBench evaluation at two granularities**: Level 3-pike (30 tasks: MLP, RNN, attention, Mamba) averaging 85 lines and Level 5 (14 frontier models: DeepSeek-V3, Llama 3, RWKV, SD3) averaging 493 lines
- Agents self-discover optimization patterns including FP16+fused flash attention, monolithic CUDA/Triton kernel fusion, and input-size-reducing operation reordering

## Trade-offs

- PIKE-B requires more LLM API calls than exploration-oriented strategies, increasing optimization wall-clock time and cost per task
- EFA success depends on the LLM being able to diagnose compilation errors from error summaries; complex correctness bugs (e.g., numerical precision issues) may not be fixable within the 5-attempt budget

## Nuances

- 2.88× speedup is an average across tasks of varying complexity; individual task speedups range widely, and the hardest frontier models (Level 5) likely show lower average gains
- Evaluation is inference-only on a single H100; multi-GPU or training-time optimization is out of scope, limiting applicability to production scenarios with tensor or pipeline parallelism
- torch.compile is the main baseline, but vendor libraries (cuBLAS, cuDNN, TensorRT) are not included as baselines, so the claimed improvements may be overstated relative to best-in-class hand-tuned alternatives
