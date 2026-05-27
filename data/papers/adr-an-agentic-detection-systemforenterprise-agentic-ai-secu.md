---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Chenning Li
- Pan Hu
- Justin Xu
- Baris Ozbas
- Olivia Liu
- Caroline Van
- Manxue Li
- Wei Zhou
- Mohammad Alizadeh
- Pengyu Zhang
- KK Sriramadhesikan
- Ming Zhang
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- agentic-inference
- observability
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 97.2% precision detecting credentials at Uber across 26 categories; 67%
  attack detection on ADR-Bench with zero false positives, 2–4× F1 over baselines
models_evaluated: []
observations:
  balance: Two-tier detector routes most sessions through a fast triage model, escalating
    ambiguous cases to the costly LLM reasoner only; sustains reliable detection across
    10,000+ daily agent sessions at Uber.
  specialize: ADR Sensor pre-structures telemetry into a fixed schema before passing
    to the LLM detector; each tier is independently optimized — sensor for throughput,
    LLM for semantic reasoning quality.
official_category: ''
openreview_url: https://openreview.net/forum?id=7B91Naeszw
organizations:
- Uber
- MIT
presentation_type: oral
principles:
- balance
- specialize
problem: Enterprise AI agents using MCP tools are invisible to EDR — which sees file
  writes but not agent reasoning or causal chains linking intent to tool execution.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3853_k9cXWDE.pdf
slug: adr-an-agentic-detection-systemforenterprise-agentic-ai-secu
status: draft
title: 'ADR: AN AGENTIC DETECTION SYSTEMFORENTERPRISE AGENTIC AI SECURITY'
topics:
- streaming
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3853
---

## Background

Enterprise AI agents take actions through tools via the Model Context Protocol (MCP). Traditional EDR tools watch file-system and network artifacts but are blind to agent reasoning — they can't see the causal chain between a prompt injection attack in a retrieved document and the tool call it triggers. The missing layer is semantic telemetry that captures why an agent made each tool call, paired with a detector that scales to tens of thousands of daily sessions.

## Key Contributions

- **ADR Sensor**: MCP-layer telemetry collector that captures agent reasoning, prompts, tool call arguments, and causal chains linking intent to execution — providing the observability missing from traditional EDR tools
- **ADR Explorer**: systematic pre-deployment red-teaming component that generates hard adversarial examples across 17 attack techniques and 133 MCP servers, building training data for robust detection without waiting for production incidents
- **ADR Detector**: two-tier online detection combining a fast triage classifier for cost-efficient first-pass filtering with a context-aware LLM reasoner for hard cases; scaled to 7,200+ hosts and 10,000+ sessions/day at Uber
- **ADR-Bench**: public evaluation benchmark of 302 tasks, 17 techniques, 133 MCP servers; ADR achieves 0 false positives while detecting 67% of attacks, outperforming ALRPHFS, GuardAgent, and LlamaFirewall by 2–4× in F1 score
- **Production deployment at Uber**: 10+ months of operation, uncovered hundreds of credential exposures across 26 categories with 97.2% precision; enables shift-left prevention before agent sessions reach production

## Findings

- Traditional EDR tools observe file-system writes but are blind to agent reasoning and the causal chain connecting adversarial prompts to malicious tool invocations.
- Static rule-based defenses fail to generalize across diverse MCP servers and novel attack variants; hard-example generation via ADR Explorer is necessary to build robust detectors.
- LLM-based detection alone is cost-prohibitive at enterprise scale; a two-tier fast-triage plus expensive-reasoner architecture makes the economics tractable.
- On AgentDojo, ADR detects all 93 prompt injection attacks with only 3 false alarms, confirming the approach generalizes beyond internal benchmarks.

## Trade-offs

- The two-tier detector's precision depends on the quality of the fast triage model; a miscalibrated triage will either pass malicious sessions or create false-positive escalation load.
- ADR requires instrumentation at the MCP protocol layer; agents using custom transports or non-MCP tool APIs require separate sensor coverage.

## Nuances

- Deployment results are from Uber's internal environment; attack distribution and agent tool usage may differ significantly in other enterprise contexts.
- The 67% attack detection rate on ADR-Bench means one-third of attacks remain undetected; the gap is largest for attacks that blend into normal behavioral patterns.