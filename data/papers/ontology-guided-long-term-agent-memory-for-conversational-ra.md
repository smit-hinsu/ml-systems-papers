---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Shuang Cao
- Rui Li
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- agentic-inference
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Lifts Recall@10 to 0.70 vs. 0.58 for dense-only; improves nDCG@10 from
  0.41 to 0.51; 47% less cross-modality disagreement; 81% cost reduction vs. long-context
models_evaluated: []
observations:
  schedule: Most conversational queries need only a few stored facts, but the system
    pays full long-context prompt cost on every one because nothing decides which
    queries are actually hard.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=wpZHLPz4N0
organizations:
- Apple
presentation_type: oral
principles: []
principles_review:
- schedule
problem: Dense retrieval and long-context prompting fail to recall implicit user preferences
  across sessions due to missing lexical overlap with earlier stored facts.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3738.pdf
slug: ontology-guided-long-term-agent-memory-for-conversational-ra
status: draft
title: Ontology-Guided Long-Term Agent Memory for Conversational RAG
topics:
- prefix-caching
- kv-cache
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3738
---

## Key Contributions

- **Dialogue-aware memory graph**: extracts durable user facts from conversations into a lightweight ontology-structured memory graph; enables semantic lookup across sessions without re-reading raw conversation history
- **Query enrichment**: augments retrieval queries with conversational cues (e.g., topic continuity signals) to bridge the lexical gap between current queries and earlier preference expressions
- **Hybrid retrieval**: combines sparse and dense retrieval against the memory graph, outperforming dense-only on Implicit Preference Recall benchmark (Recall@10: 0.70 vs. 0.58)
- **Budget-aware router**: balances retrieval quality against serving cost; routes easy queries to lightweight graph lookups and hard queries to costlier LLM expansion, achieving 81% cost reduction vs. long-context methods

## Findings

- Dense-only retrieval misses implicit preferences when current queries lack lexical overlap with earlier stored facts; ontology-structured memory with hybrid retrieval closes this gap significantly.
- Long-context prompting is expensive and often redundant when user facts can be directly indexed; the budget router avoids it for ~81% of queries with no nDCG loss.
- Cross-modality disagreement between retrieval signals drops 47% with hybrid retrieval, indicating better consistency across retrieval methods.

## Trade-offs

- Memory graph extraction quality depends on the LLM used for fact extraction; noisy or incorrect fact extraction degrades recall in ways that are hard to detect without ground truth.
- Ontology-based structuring requires domain-specific schema design; generalizing to new conversation domains may require schema adaptation.