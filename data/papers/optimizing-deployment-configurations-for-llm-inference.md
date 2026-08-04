---
agentic_models: []
arxiv_url: ''
authors:
- Sungmin Cho
- Jaewon Lee
- Chunqiang Tang
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
- fleet-efficiency
hardware:
- H100
- H200
- MI300X
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Exhaustive search over millions of configs for Llama on H100/H200/MI300X
  identifies throughput-maximizing parallelism under production SLOs at Meta.
models_evaluated:
- Llama (family)
observations:
  measure: Hardware, parallelism degrees, and runtime policy multiply into millions
    of candidate deployments for one Llama model; testing them on production GPUs
    costs more than any of them wins back.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=gEbKQeIdxB
organizations:
- Meta
presentation_type: oral
principles:
- measure
problem: No framework exists to navigate hardware, parallelism, and runtime choices
  to find throughput-maximizing configs under strict latency SLOs at scale.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3780.pdf
slug: optimizing-deployment-configurations-for-llm-inference
status: draft
title: Optimizing Deployment Configurations for LLM Inference
topics:
- tensor-parallelism
- pipeline-parallelism
- autotuning
- continuous-batching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3780
---

## Key Contributions

- **Configuration search framework**: systematically analyzes millions of deployment configurations spanning hardware type, tensor/pipeline/expert/context/data parallelism degrees, and runtime policies (continuous batching vs. prefill-decode disaggregation) to identify throughput-maximizing deployments under latency SLOs for Llama models at Meta scale
- **Workload-driven SLO modeling**: characterizes how request mix (prompt length distribution, concurrency, output length) interacts with parallelism strategy to determine the feasible configuration space; reveals that optimal configurations vary substantially across workload shapes
- **Cross-hardware portability analysis**: evaluates how configuration decisions transfer across H100, H200, and MI300X; documents hardware-specific performance cliffs where a configuration shift yields disproportionate gains or degradations
- Production deployment insights from serving nearly one billion monthly active users, providing ground truth for which configuration choices matter most at scale

## Trade-offs

- The search framework is cost-effective only at Meta's deployment scale; smaller organizations serving fewer models and workload shapes may not amortize the engineering overhead of building and maintaining such a system
- Offline configuration simulation relies on performance models that may not capture all runtime effects (e.g., cache misses, host–device transfer contention); selected configurations may require empirical validation before production cutover

## Nuances

- Specific throughput numbers and hardware comparison data are not disclosed in the available abstract; the paper likely presents relative improvements and Pareto curves rather than absolute figures
- Authors are not listed in the available abstract; this appears to be a Meta systems paper with contributions from a larger team
- The focus is on Llama models; generalization to MoE models (e.g., Llama-MoE variants) or other architectures may require re-running the search with additional parallelism dimensions