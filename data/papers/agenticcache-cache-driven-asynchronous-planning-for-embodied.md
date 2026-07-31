---
agentic_models: []
arxiv_date: 2026-04
arxiv_url: https://arxiv.org/abs/2604.24039
authors:
- Hojoon Kim
- Yuheng Wu
- Thierry Tambe
award: ''
citations: 1
citations_updated: '2026-07-31'
code_url: https://github.com/hojoonleokim/MLSys26_AgenticCache
domain:
- agentic-inference
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 22% avg task success improvement across 12 configs (4 benchmarks × 3
  models); 65% latency reduction and 50% fewer tokens via cached plan reuse
models_evaluated: []
observations:
  cache: Embodied tasks exhibit strong plan locality; AgenticCache reuses cached plan
    transitions to skip per-step LLM calls, cutting token usage by 50% and latency
    by 65% across benchmarks.
  pipeline: A background Cache Updater asynchronously validates and refines cached
    plans while the agent executes, hiding LLM inference latency behind task execution
    rather than blocking each planning step.
official_category: ''
openreview_url: https://openreview.net/forum?id=UfABxFoSXH
optimization_type: []
organizations:
- Harvard University
presentation_type: oral
principles:
- cache
- pipeline
problem: Per-step LLM calls in embodied AI agents impose severe latency and token
  cost because each planning step waits synchronously for a full LLM response.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3806_NIaKgZ6.pdf
slug: agenticcache-cache-driven-asynchronous-planning-for-embodied
status: draft
title: 'AgenticCache: Cache-Driven Asynchronous Planning for Embodied AI Agents'
topics:
- prefix-caching
- kv-cache
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3806
---

## Background

An embodied agent — a robot or simulated actor — calls an LLM at every step to pick its next action, then blocks until the response arrives. That synchronous call dominates step latency. Embodied tasks have strong plan locality: a bounded environment produces similar action sequences across episodes, so a cached plan can stand in for a fresh LLM call.

## Key Contributions

- **Plan locality hypothesis**: demonstrates that in embodied tasks the next plan is largely predictable from the current one; quantifies this across 4 multi-agent benchmarks to motivate caching
- **AgenticCache planning framework**: runtime cache of frequent plan transitions that agents query first; cache hits replace LLM calls entirely, cutting per-step latency by 65% and token usage by 50%
- **Asynchronous Cache Updater**: background process that calls the LLM to validate and refine cached entries while the agent continues task execution, keeping the cache fresh without blocking the critical path
- **22% average task success improvement**: evaluated across 12 configurations (4 benchmarks × 3 models), showing that faster planning actually improves task outcomes by reducing decision latency in time-sensitive embodied tasks

## Trade-offs

- Cache effectiveness degrades in open-ended or rapidly changing environments where plan locality is low; the cache hit rate directly determines the latency and cost savings.
- The asynchronous Cache Updater may serve stale plans briefly; in safety-critical applications, a stale plan could cause incorrect or harmful actions before the update completes.

## Nuances

- The 22% success improvement and 65% latency reduction are averages across all 12 configurations; individual benchmarks and model pairings may show substantially different trade-offs.
- Results depend on the simulated embodied environment; real-world robotics deployments with lower plan predictability are not evaluated.
