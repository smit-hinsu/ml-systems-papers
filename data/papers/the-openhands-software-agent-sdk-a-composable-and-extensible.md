---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Xingyao Wang
- Simon Rosenberg
- Juan Michelini
- Calvin Smith
- Hoang H. Tran
- Engel Nyst
- Rohit Malhotra
- Xuhui Zhou
- Valerie Chen
- Robert Brennan
- Graham Neubig
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/All-Hands-AI/OpenHands
domain:
- agentic-inference
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: V1 SDK substantially reduces system-attributable failures vs. V0 with
  negligible event-sourcing overhead in production deployment.
models_evaluated: []
agentic_models:
- Multiple LLM backends (model-agnostic routing)
observations:
  balance: Model-agnostic multi-LLM routing distributes agent workload
    across providers, preventing single-backend overload and maintaining throughput
    under variable model availability.
  pipeline: Seamless local-to-remote execution portability lets agents
    offload sandboxed tasks to remote instances, parallelizing agent execution with
    local orchestration.
official_category: ''
openreview_url: https://openreview.net/forum?id=pzVmWs6yGq
organizations:
- Carnegie Mellon University
presentation_type: oral
principles:
- balance
- pipeline
problem: Production software agents need sandboxed execution, flexible tool composition,
  multi-LLM routing, and lifecycle control that existing SDKs lack.
project_url: https://github.com/All-Hands-AI/OpenHands
reading_status: want-to-read
research_or_industry: mixed
slides_url: ''
slug: the-openhands-software-agent-sdk-a-composable-and-extensible
status: draft
title: 'The OpenHands Software Agent SDK: A Composable and Extensible Foundation for
  Production Agents'
topics:
- streaming
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3749
---

## Background

Software agents run multi-step tasks — code execution, web browsing, file editing, API calls — inside sandboxed environments, maintaining state across many tool calls for minutes to hours. Production deployment needs isolated sandboxes, composable tool interfaces, multi-LLM routing, and lifecycle controls (pause, resume, inspect) that general-purpose inference frameworks don't provide. Most existing agent frameworks bolt these on top of chat APIs, producing fragile integrations that fail at scale.

## Key Contributions

- **OpenHands SDK V1 architecture**: complete redesign of agent runtime with a minimal agent interface (few lines of code for default case), extensible to custom tools, memory management, and complex agent behaviors.
- **Native sandboxed execution**: integrated local and remote sandbox environments with seamless portability; eliminates the need for external container orchestration for security-critical agent tasks.
- **Model-agnostic multi-LLM routing**: built-in routing layer supports arbitrary LLM backends; agents are not tied to a single provider, enabling cost and availability optimization at runtime.
- **Lifecycle control and REST/WebSocket interfaces**: built-in services for agent lifecycle management (start, pause, resume, inspect) and connection to VS Code, VNC, browser, CLI, and API interfaces.
- **Built-in security analysis**: integrated static and dynamic security checks for agent-generated code, reducing the risk of harmful actions in production deployments.
- Production deployment data shows V1 substantially reduces system-attributable failures over V0, with negligible event-sourcing overhead.

## Trade-offs

- The full-featured SDK introduces more abstraction layers than minimal agent frameworks; latency per agent action is higher due to event sourcing and lifecycle management overhead.
- Model-agnostic routing requires explicit integration work to add new LLM backends; prompt format normalization across providers is not fully transparent.

## Nuances

- The "substantial reduction in system-attributable failures" metric is not quantified with specific numbers in the abstract; production deployment context is not fully disclosed.
- Evaluation benchmarks show "strong agent performance" but the paper does not ablate the SDK components' individual contributions to task success rates.
