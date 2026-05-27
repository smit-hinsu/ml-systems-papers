---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Yi Ding
- Aijia Gao
- Thibaud Ryden
- Michal Sedlak
- Essam Ewaisha
- Igor Marnat
- Henry Hoffmann
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- fleet-efficiency
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Acela improves upgrade window utilization 1.25×, schedules 33% more upgrades,
  completes 41% more, and reduces cancellations 2.4× vs. Meta's existing scheduler
models_evaluated: []
observations: {}
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=l72e5oROLT
organizations:
- Meta
- University of Chicago
presentation_type: oral
principles: []
problem: Software upgrades in datacenters stall due to poor duration predictions —
  overestimates waste maintenance windows and underestimates cause SLO violations.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3765.pdf
slug: cost-aware-duration-prediction-for-software-upgrades-in-data
status: draft
title: Cost-aware Duration Prediction for Software Upgrades in Datacenters
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3765
---

## Background

Datacenter maintenance schedulers pack software upgrades (OS patches, firmware updates) into maintenance windows by predicting how long each upgrade takes. Mispredictions are asymmetric: underestimates risk SLO violations when machines stay offline too long; overestimates waste windows by leaving capacity idle. Standard regression models optimizing symmetric accuracy don't capture this asymmetry, and straggler machines that take far longer than peers compound the problem.

## Key Contributions

- **Acela framework**: cost-aware upgrade duration prediction that accounts for asymmetric misprediction costs — overestimating and underestimating upgrade duration carry different penalties for scheduling efficiency and SLO compliance
- **Cost-aware model selection**: Acela evaluates multiple predictive models and selects among them based on the deployment context's cost asymmetry rather than symmetric accuracy metrics
- **Straggler mitigation**: detects and corrects straggler-induced overestimations that would otherwise inflate predicted durations across the scheduling queue and reduce throughput
- **Production validation at Meta**: deployed on Meta's production datacenter systems; 1.25× upgrade window utilization, +33% scheduled upgrades, +41% completed upgrades, 2.4× fewer cancellations vs. existing scheduler

## Findings

- Software upgrade scheduling is characterized by a fundamentally asymmetric loss function: underestimating duration risks SLO violations while overestimating wastes scheduling windows, requiring different treatment than symmetric regression problems.
- Stragglers — upgrades that take far longer than predicted — are a key source of overestimation that propagates conservatism across the scheduling queue.
- Cost-aware model selection outperforms both the existing production scheduler and a symmetric-loss predictor across all measured production metrics.

## Trade-offs

- Acela's model selection requires characterizing the cost asymmetry for each upgrade type; new upgrade categories need calibration before Acela can be applied.
- Straggler correction may under-allocate time for genuinely slow upgrades in edge cases; the false-positive straggler detection rate is not characterized in the abstract.

## Nuances

- Results are from Meta's production infrastructure; generalization to other datacenter operators with different hardware, upgrade types, or SLO structures is not validated.
- The paper frames scheduling as a constrained optimization problem, but the abstract does not detail the specific constraint structure used.