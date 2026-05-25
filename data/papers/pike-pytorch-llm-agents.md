---
agentic_models: []
arxiv_url: https://arxiv.org/abs/2511.16964
authors:
- Kirill Nagaitsev
- Luka Grbcic
- Samuel Williams
- Costin Iancu
award: ''
citations: 0
citations_updated: '2026-05-24'
code_url: https://github.com/pike-project/pike
date: '2026-05-19'
domain:
- ml-compilers
hardware:
- H100
indexed_by: smithinsu
indexed_date: '2026-05-24'
observations:
- kernel-verifiability
- llm-driven-optimization
key_results: 2.88× speedup over PyTorch Eager; 1.85× over torch.compile on H100
mlsys_official_category: ''
mlsys_url: https://mlsys.org/virtual/2026/oral/3823
models_evaluated: []
openreview_url: https://openreview.net/forum?id=MJxhiX3sSd
organizations:
- Lawrence Berkeley National Laboratory
presentation_type: oral
problem: Automate PyTorch inference optimization by framing it as a multi-agent LLM
  task with code execution feedback.
project_url: ''
reading_status: read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3823.pdf
slug: pike-pytorch-llm-agents
topics:
- llm-code-generation
title: Optimizing PyTorch Inference with LLM-Based Multi-Agent Systems
---

## Summary

PIKE presents a logical framework for comparing multi-agent systems that optimize PyTorch inference. The key finding is that **exploit-heavy strategies paired with error-fixing agents** perform best: agents that aggressively try compiler passes and transformations, combined with a separate agent that detects and corrects errors, outperform conservative or purely exploratory strategies.

The system operates by having LLM agents propose transformations to a PyTorch model (e.g., operator fusion, layout changes, compile flags), execute the transformed code, measure speedup, and iteratively refine. The feedback loop between code generation and benchmarking is what makes the approach tractable.

## Key Contributions

- A formal taxonomy of multi-agent strategies for compiler optimization
- Evidence that exploit-heavy + error-fixing is the Pareto-optimal agent combination
- Open-source implementation (PIKE) demonstrating 2.88× speedup over eager PyTorch on H100

## Method

Agents are given the PyTorch model source and a performance feedback signal (latency on target hardware). They generate modified versions using transformations like `torch.compile`, operator fusion, and quantization. An error-fixing agent catches exceptions and regenerates valid code. The framework is hardware-aware — it benchmarks on the actual target (H100).

## Results

- 2.88× speedup over PyTorch Eager
- 1.85× over `torch.compile` baseline
- Hardware: H100 GPU

## Limitations

- Evaluation scope not fully characterized (which model architectures, which sizes?)
- Relies on LLM quality — results may vary with different backbone models
- Optimization time (agent calls) not fully analyzed

## Personal Notes

<!-- Add your own observations, questions, and connections to other work here -->