---
agentic_models: []
arxiv_date: 2026-05
arxiv_url: https://arxiv.org/abs/2605.13708
authors:
- Haaris Mehmood
- Giorgos Tatsis
- Dimitrios Alexopoulos
- Karthikeyan Saravanan
- Jie Xu
- Anastasios Drosou
- Mete Ozay
award: ''
citations: 0
citations_updated: '2026-07-31'
code_url: ''
domain:
- llm-training
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 4.6× speedup over OPA (prior best protocol) for 100k-dimensional updates
  from 100k 5G clients; eliminates local masking and homomorphic encryption overhead
models_evaluated: []
observations:
  balance: DisAgg's optimal tradeoff selection distributes aggregation load across
    the Aggregator committee, preventing the server bottleneck that limits throughput
    in centralized secure aggregation.
official_category: ''
openreview_url: https://openreview.net/forum?id=H0BLKrOgik
optimization_type: []
organizations:
- Samsung
- Pragma IoT
presentation_type: oral
principles:
- balance
problem: Secure FL aggregation requires many communication rounds or expensive homomorphic
  encryption, making practical large-scale deployment too slow.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: disagg-distributed-aggregators-for-efficient-secure-aggregat
status: draft
title: 'DisAgg: Distributed Aggregators for Efficient Secure Aggregation'
topics:
- all-reduce
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3837
---

## Background

Federated learning keeps raw data on client devices, but gradient updates still leak it through inference attacks. So FL uses **secure aggregation**: clients mask their gradients with values that cancel in the sum, leaving the server only the aggregate. At scale — 100k+ clients, 100k-dimensional updates — generating those canceling masks needs multi-round coordination or homomorphic encryption, both far too slow for 5G deployments.

## Key Contributions

- **DisAgg protocol**: secret-shares each client's gradient update to a small Aggregator committee drawn from the client pool; Aggregators compute partial sums locally and return only aggregated shares to the server, eliminating the need for individual client masking or homomorphic encryption
- **Single-round design**: each FL iteration requires only one server interaction per client, matching the round efficiency of OPA while dramatically reducing per-round cryptographic and computation cost
- **Optimal tradeoff selection**: analytically balances communication cost (secret sharing bandwidth) against computation cost (partial sum aggregation) to minimize total overhead per round
- **4.6× speedup over OPA** on 100k-dimensional update vectors from 100k 5G clients, demonstrating feasibility at scale

## Trade-offs

- Privacy guarantee is against an honest-but-curious server plus a limited fraction of colluding Aggregators; if more Aggregators collude than the threshold, the secret-sharing scheme breaks and client updates are exposed.
- Adding an Aggregator committee increases communication fan-out from clients; each client must secret-share to multiple Aggregators rather than sending one masked vector to the server.

## Nuances

- The 4.6× speedup is measured relative to OPA for 100k-dimensional vectors and 100k clients — a 5G FL scenario that may not match typical cross-device FL deployments in ML.
- The protocol assumes Aggregators are a subset of current-round clients; in practice, identifying and coordinating a reliable committee without introducing liveness issues is a systems challenge not fully addressed in the abstract.
