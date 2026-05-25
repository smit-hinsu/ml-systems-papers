# Paper Summary Prompt

Use this with `scripts/summarize_paper.py`, or paste the contents of the `<prompt>` block
into Claude (web or API) together with the paper text and your notes.

---

<prompt>
You are writing a paper entry for the ML Systems Papers index. The reader is a senior ML
systems engineer or researcher deciding whether to read the full paper. Your job is to give
them enough to understand the approach and evaluate whether it's relevant to their work —
without making them open the PDF.

## Rules

### problem
One sentence, **max 160 chars**. Practitioner voice: what breaks, costs too much, or takes too long right now?

- ❌ "existing approaches have performance limitations"
- ✅ "GPU kernels hand-written in CUDA take weeks to tune per architecture and don't transfer across hardware generations"

### key_results
One sentence, **max 160 chars**. Hardware + model/workload + metric + baseline — all in one sentence. Numbers required.

- ❌ "outperforms baselines"
- ✅ "37% higher token throughput than vLLM on Llama-3-70B at batch 64 on H100, <1% accuracy degradation"

### ## Key Contributions
3–5 bullets. Each must be a **concrete artifact**: a named algorithm, data structure,
protocol, or measurement — with a one-line mechanism. Not "we show X is possible."

The problem being solved and the key numbers should both be **implicit** in these bullets —
the reader should understand what was broken and what the result was without separate
Problem or Results sections. Include hardware + model + metric + baseline inline when a
contribution is the primary result. If hardware or baselines are absent from the paper, say
so explicitly rather than omitting.

- ❌ "a new scheduling algorithm that improves throughput"
- ✅ "SRPT preemption scheduler: predicts remaining decode steps via a small proxy model and
  preempts long-running requests — 40% lower P99 latency vs. FCFS on Llama-3-70B/H100"

### ## Trade-offs
2–4 short bullets on what the approach explicitly gives up to achieve its gains. Think in
terms of: speed vs accuracy, memory vs compute, throughput vs latency, complexity vs
generality. Omit if the paper doesn't make meaningful trade-offs.

- ❌ "there are some limitations"
- ✅ "2–3% accuracy drop at int4 quantization; savings vanish at batch size < 8"

### ## Nuances
2–4 short bullets covering implementation gotchas, subtle assumptions, conditions that
break the approach, and limitations — things a practitioner would only discover by reading
carefully or attempting an implementation. Omit if nothing notable.

### ## Findings
*Only for measurement, characterization, or survey papers.* Bullet-point list of the
concrete findings — what was measured or characterized, not what the system achieves.
Each bullet should be a specific quantitative or qualitative fact. Omit this section
entirely for algorithmic or systems-design papers.

- ❌ "the system improves throughput for prefill-heavy workloads" (system claim)
- ✅ "disaggregation improves TTFT/throughput for prefill-heavy workloads but adds net overhead for generation-heavy traffic, where co-location outperforms" (measurement finding)

**Conciseness rules across all sections:**
- Each section has one job. Don't repeat across sections.
- If a sentence appears in two places, it belongs in one: the more specific section.
- ## Key Contributions names mechanisms and bakes in the problem context and key numbers.
- ## Trade-offs covers what was given up — it doesn't re-explain mechanisms.
- ## Nuances is for practitioners — it doesn't restate trade-offs.

## Anti-patterns

| Wrong | Right |
|---|---|
| "uses a novel scheduling algorithm" | "preempts requests using SRPT scheduling based on predicted remaining decode steps, estimated via a small proxy model" |
| "leverages modern GPU architecture" | "exploits H100 TMA to overlap data movement with compute in the attention kernel" |
| "scales to large models" | "tested on Llama-3-70B and Mixtral 8×22B, single-node 8×H100" |
| "significantly reduces memory" | "reduces peak KV cache memory by 3.2× via 4-bit quantization of keys and 8-bit of values" |
| "inspired by prior work" | "extends PagedAttention (vLLM) with copy-on-write semantics for beam search" |

## Taxonomy

Pick slugs only from these lists. If the paper doesn't fit a slug, leave the list shorter rather
than picking the closest wrong thing.

**domain** — pick 1–2:
- `llm-serving` — inference and serving systems for large language models
- `llm-training` — training systems and infrastructure
- `rl-training` — reinforcement learning training infrastructure
- `recs-models` — recommendation / embedding / ranking models
- `agentic-inference` — multi-agent LLM systems, tool use, agentic workloads
- `ml-compilers` — compiler toolchains, graph-level optimization, autotuning, profiling (XLA, torch.compile, JAX)
- `ml-kernels` — individual kernel optimization, CUDA/Triton kernel generation, operator-level performance
- `observability` — profiling, tracing, debugging, and monitoring tools for ML systems
- `fleet-efficiency` — cluster efficiency, utilization, job scheduling at scale

**principles** — pick all that genuinely apply. These are general optimization principles that the paper uses or validates. Pick slugs from `data/principles.yaml`:
- `avoid-redundant-work` — results for repeated inputs can be cached so they are computed only once (e.g., KV cache prefix reuse)
- `overlap-independent-work` — two operations that don't depend on each other can run concurrently, hiding the latency of the slower one (e.g., comm-compute overlap)
- `exploit-sparsity` — when inputs or intermediates are sparse or near-zero, the corresponding computation can be skipped (e.g., MoE top-k routing, sparse attention)
- `reduce-data-movement` — moving data between compute and memory is often more expensive than the computation itself; fusing/tiling reduces round-trips
- `exploit-memory-hierarchy` — keep frequently accessed data in the fastest memory tier; evict cold data to slower, larger tiers (e.g., KV cache tiering, register-level fusion)
- `balance-utilization` — when parallel workers have unequal work, faster workers idle waiting for the slowest; eliminating imbalance is often the dominant lever at scale
- `ai-solves-verifiable` — when an objective is deterministic and benchmarkable, AI agents can explore the solution space more effectively than hand-crafted heuristics

**observations** — for each principle slug you picked, write one sentence (**max 200 chars**) as `observations.<slug>` capturing what the authors *specifically observed* in this paper's context. This is NOT a restatement of the principle — it is the paper-specific insight: what they noticed that made the principle applicable, or what the measurement revealed.

- ❌ `prefix-reuse: "shared prefixes can be cached to avoid redundant prefill"` — just restates the principle
- ✅ `prefix-reuse: "agentic workloads have redundant prefill across calls sharing a system prompt, but the radix cache fills only after a call completes — so concurrent calls within the same turn don't benefit by default"`

**topics** — pick all that apply (concrete methods the paper uses):

Distributed:
- `tensor-parallelism`, `pipeline-parallelism`, `fsdp-zero`, `communication-overlap`, `all-reduce`

Memory:
- `kv-cache`, `prefix-caching`, `quantization`, `cpu-offload`

Efficiency:
- `kernel-fusion`, `speculative-decoding`, `sparse-attention`, `continuous-batching`

Architecture:
- `moe` — Mixture-of-Experts

Serving:
- `streaming` — token streaming

Automation:
- `llm-code-generation`, `autotuning`

## Output format

Output ONLY the completed `.md` entry — start your response with `---` on line 1 and end
with the last line of the body. No preamble, no explanation, no code fences.

Fill every field; use `""` for strings you cannot determine and `[]` for empty lists.
Use `null` for numeric fields with unknown values. Do not add fields that aren't shown.
Preserve any field values already filled in the stub — only fill in empty ones (except
`problem`, `key_results`, and the body sections, which you should always write fresh).

```
---
title: "<full title from paper>"
slug: "<kebab-case, max 60 chars>"
authors: ["Author One", "Author Two"]
organizations: ["Org A", "Org B"]

venue_url: ""
openreview_url: ""
arxiv_url: ""
slides_url: ""
code_url: ""
project_url: ""

venue: "mlsys-2026"
official_category: ""
presentation_type: oral
award: ""
arxiv_date: ""

domain: [slug1, slug2]
topics: [slug1, slug2]
principles: [slug1, slug2]
observations:
  slug1: "what the authors specifically observed in this paper's context (not a restatement of the principle)"
  slug2: "paper-specific observation"

hardware: []
models_evaluated: []
agentic_models: []

citations: null
citations_updated: ""
research_or_industry: "research"

problem: "<one sentence>"
key_results: "<one sentence with numbers>"

status: draft
reading_status: want-to-read
indexed_by: ""
indexed_date: ""
---

## Key Contributions

- <named artifact + one-line mechanism; include problem context and key numbers inline>
- <concrete artifact>
- <concrete artifact>

## Findings

(omit this section for systems/algorithmic papers; include only for measurement/characterization/survey papers)
- <specific quantitative or qualitative finding>
- <another finding>

## Trade-offs

- <what is given up to achieve the gains>
- <another trade-off, if any>

## Nuances

- <implementation gotcha, subtle assumption, or limitation>
- <another nuance, if any>
```

---

Now summarize this paper.

Paper text:

{{PAPER_TEXT}}

---

Personal notes (optional):

{{NOTES}}
</prompt>
