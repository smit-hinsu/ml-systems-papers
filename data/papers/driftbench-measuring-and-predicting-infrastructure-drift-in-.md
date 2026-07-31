---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Gianluigi Vitale
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
- observability
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: PRI achieves R²=0.909 for unseen hardware and R²=0.763 for unseen precision;
  blocked a real upgrade where 23.85% of safety prompts changed classification
models_evaluated: []
observations: {}
official_category: ''
openreview_url: https://openreview.net/forum?id=Xfzzp6grRP
optimization_type: []
organizations:
- Universitas Mercatorum
presentation_type: oral
principles: []
problem: Production LLM deployments lack a way to predict output consistency risk
  when upgrading hardware, precision, or frameworks, leading to silent regressions.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3799_Hct4euu.pdf
slug: driftbench-measuring-and-predicting-infrastructure-drift-in-
status: draft
title: 'DriftBench: Measuring and Predicting Infrastructure Drift in LLM Serving Systems'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3799
---

## Key Contributions

- **DriftBench dataset**: 236,985 prompt-response pairs across 105 infrastructure configurations spanning 5 LLMs, 4 GPU platforms, 3 frameworks, 3 precision levels — the first systematic characterization of output consistency across infrastructure changes
- **Portability Risk Index (PRI)**: a predictive metric for output drift risk under infrastructure changes; achieves R²=0.909 generalization to unseen GPU hardware and R²=0.763 to unseen precision levels
- **Systematic/idiosyncratic dichotomy**: hardware and precision changes produce predictable, systematic drift (R²≥0.76) suitable for predict-once risk assessment; framework and model changes produce idiosyncratic drift (R²<0.48) requiring per-change measurement
- **Production validation**: blocked a real high-drift infrastructure upgrade where 23.85% of safety-critical prompts flipped between safe and unsafe classifications — demonstrating operational value

## Findings

- Infrastructure changes are not uniformly risky: hardware and precision swaps show systematic, generalizable drift patterns, while framework or model swaps are essentially unpredictable from other configurations.
- Nearly 1 in 4 safety prompts changed safety classification when a specific infrastructure upgrade was applied — a silent correctness regression that would not have been caught without systematic drift measurement.
- The PRI metric generalizes across unseen hardware dimensions (R²=0.909) but degrades for unseen precision dimensions (R²=0.763), suggesting hardware drift is more structurally predictable.

## Trade-offs

- DriftBench is a measurement and prediction tool only; it does not provide mitigation strategies for high-drift configurations — operators who discover high PRI must still find an alternative upgrade path independently.
- The 105-configuration dataset is large but not exhaustive; novel GPU architectures, quantization schemes, or framework versions not in the training set may fall outside the PRI model's calibration.

## Nuances

- The paper explicitly scopes to measuring and predicting drift, not fixing it — a deliberate choice that leaves mitigation as future work.
- R² for framework/model changes is <0.48, meaning PRI is essentially unable to predict risk for those change types; practitioners must always re-measure when swapping frameworks or models.