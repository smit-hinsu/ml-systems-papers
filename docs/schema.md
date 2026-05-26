# Paper Entry Schema

Every paper lives in `data/papers/<slug>.md` as a YAML frontmatter + Markdown body file.
This document defines every field: its type, valid values, and what to capture.

---

## Identity

### `title`
**Type:** string — **Required**

Full paper title exactly as it appears on the MLSys virtual page or arXiv.

### `slug`
**Type:** string — **Required**

Kebab-case identifier, max 60 characters, must match the filename stem.
Generated automatically by `new_paper.py` and `fetch_mlsys_slides.py`.

### `authors`
**Type:** list of strings — **Required**

Full author names in order. No truncation — include everyone.

### `organizations`
**Type:** list of strings — **Optional but fill when known**

Author affiliations. Use the institutional name as it appears in the paper.
Multiple organizations are fine; these become clickable org filters on the site.

---

## Links

### `venue_url`
**Type:** URL string — **Required**

The conference virtual page for this paper (e.g. `https://mlsys.org/virtual/2026/oral/<id>`).
Required: it is the primary identifier for the paper at its venue.

### `openreview_url`
**Type:** URL string — **Fill when known**

The `https://openreview.net/forum?id=<id>` page. Not the PDF link — use `/forum`.

### `arxiv_url`
**Type:** URL string — **Fill when known**

The `https://arxiv.org/abs/<id>` page. Not the PDF — use `/abs/`.

### `slides_url`
**Type:** URL string — **Fill when known**

Usually `https://mlsys.org/media/mlsys-<year>/Slides/<id>.pdf`.
Fetched automatically by `fetch_slides.py`.

### `code_url`
**Type:** URL string — **Fill when known**

GitHub or other public code repository.

### `project_url`
**Type:** URL string — **Fill when known**

Project/demo page if the authors maintain one (separate from code).

---

## Venue Metadata

### `venue`
**Type:** slug — **Required**

Must match a key in `data/venues.yaml`. Example: `mlsys-2026`.

### `official_category`
**Type:** string — **Fill when known**

The official venue track/category as labeled on the virtual site (e.g. "Research Papers",
"Industry Track"). Not a controlled vocabulary — copy it verbatim.

### `presentation_type`
**Type:** enum — **Required**

Valid values: `oral` | `poster` | `spotlight`

### `award`
**Type:** string — **Leave empty if none**

Award name as given (e.g. "Best Paper", "Outstanding Paper Award").

### `arxiv_date`
**Type:** string — **Auto-derived by `fetch_metadata.py`**

Format: `YYYY-MM` (e.g. `2024-10`). Derived from the arXiv ID when `arxiv_url` is set.
Leave empty if no arXiv preprint exists.

---

## Taxonomy

### `domain`
**Type:** list of slugs from `data/domains.yaml` — **Required, 1–2 values**

The primary ML systems area(s) this paper belongs to. Pick the fewest that are accurate.

| Slug | Use for |
|---|---|
| `llm-serving` | Inference and serving systems for LLMs |
| `llm-training` | Training infrastructure |
| `rl-training` | Reinforcement learning training |
| `recs-models` | Recommendation / embedding / ranking |
| `agentic-inference` | Multi-agent systems, tool use |
| `ml-compilers` | Compiler toolchains, graph optimization, autotuning (XLA, torch.compile) |
| `ml-kernels` | Individual kernel optimization, CUDA/Triton generation |
| `observability` | Profilers, tracers, debuggers, monitoring tools |
| `fleet-efficiency` | Cluster scheduling, resource utilization at scale |

### `principles`
**Type:** list of slugs from `data/principles.yaml` — **Required, pick all that apply**

General optimization principles the paper applies or validates. These are reusable
systems techniques — not paper-specific. Pick strictly: only include a principle if the
paper explicitly builds on it or measures it.

| Slug | Label | Category |
|---|---|---|
| `cache` | Cache to avoid repeated computation | efficiency |
| `pipeline` | Pipeline independent work to hide latency | efficiency |
| `skip` | Skip provably unnecessary work | efficiency |
| `quantize` | Quantize to trade precision for efficiency | efficiency |
| `approximate` | Approximate to trade quality for efficiency | efficiency |
| `speculate` | Speculate to hide sequential latency | efficiency |
| `batch` | Batch to amortize fixed overheads | efficiency |
| `fuse` | Fuse operations to minimize memory bandwidth | memory |
| `tier` | Keep hot data near compute | memory |
| `recompute` | Recompute to save storage | memory |
| `balance` | Balance load to maximize utilization | distributed |
| `specialize` | Specialize divergent workloads for independent optimizations | distributed |
| `elastic` | Scale elastically to fill spare capacity | distributed |
| `search-ai` | Search with AI for verifiable problems | tooling |
| `portable` | Abstract hardware to preserve deployment optionality | tooling |

**Slug stability**: slugs are short mechanism-words (`cache`, `pipeline`) stable across label
rewording. To rename a label, edit only `data/principles.yaml` — no paper files need to change.

### `observations`
**Type:** mapping of principle slug → one-sentence string — **Fill for each principle listed** — **max 200 chars per value**

Paper-specific observations: what the authors specifically noticed or measured in this
paper's context that made the principle applicable. This is NOT a restatement of the
principle's generic description — it captures the concrete, paper-scoped observation.

Shown on both the index card and paper page header. Keep it to one crisp sentence.

- ❌ `cache: "shared prefixes can be cached to avoid redundant prefill"` (just restates the principle)
- ✅ `cache: "agentic workloads share system prompt prefixes, but the radix cache fills only after a call completes — concurrent calls within the same turn don't benefit by default"` (168 chars)

### `topics`
**Type:** list of slugs from `data/topics.yaml` — **Required, pick all that apply**

Concrete algorithmic or systems methods the paper uses or improves. These are "what technique"
tags, not "what observation" tags. A paper using paged attention would get `kv-cache`; a paper
measuring the cost of AllReduce would get `all-reduce`.

See `data/topics.yaml` for the full list with categories.

---

## Evaluation Context

### `hardware`
**Type:** list of strings — **Fill from results section**

GPU/TPU/accelerator models on which the main results were measured.
Use the product name as commonly written: `H100`, `A100 80GB`, `TPU v4`, `RTX 4090`.

Examples: `["H100", "A100 80GB"]`, `["TPU v4"]`

### `models_evaluated`
**Type:** list of strings — **Fill from results section**

LLM or model checkpoints used in evaluation. Include size if given.
Examples: `["Llama-3-70B", "Mixtral-8x22B", "GPT-4o"]`

### `agentic_models`
**Type:** list of strings — **Only for agentic-inference papers**

The LLM(s) used as the agent backbone (i.e., the model making decisions), distinct from
models being served. Examples: `["GPT-4o", "Claude-3.5-Sonnet"]`

---

## Impact

### `citations`
**Type:** integer or null — **Auto-fetched by `fetch_metadata.py`**

Citation count from OpenAlex. `null` until first fetch.

### `citations_updated`
**Type:** date string (YYYY-MM-DD) or empty — **Auto-set by `fetch_metadata.py`**

Date of the last citation count update.

### `research_or_industry`
**Type:** enum — **Required**

Valid values: `research` | `industry` | `mixed`

- `research`: academic paper, university or national lab authors, novel contribution
- `industry`: production system from a tech company, primarily engineering report
- `mixed`: joint academic/industry or paper that is both a research contribution and a production deployment

---

## Quick-Scan Fields

These two fields appear prominently on the index and paper pages.
They are the highest-leverage fields to fill in well.

### `problem`
**Type:** string — **Required** — **max 160 chars**

One sentence. Practitioner voice — what breaks, costs too much, or takes too long?
Must be specific enough that you couldn't substitute it into a different paper.

- ❌ "existing systems are inefficient"
- ✅ "downstream agents must wait for upstream agents to finish prefill, causing serial latency stacking in multi-agent pipelines"

### `key_results`
**Type:** string — **Required** — **max 160 chars**

The single most important result. Should include: metric + number + hardware + baseline.
If the paper measures multiple things, pick the one that would make a colleague say "oh, interesting."

- ❌ "significant speedup over baseline"
- ✅ "40% end-to-end latency reduction and 3.5× speedup in a two-agent pipeline on H100 vs. sequential prefill"

---

## Workflow Fields

### `status`
**Type:** enum

Valid values: `draft` | `published`

- `draft`: stub or work-in-progress — not shown on the public site (only in `--dev` mode)
- `published`: summary reviewed and ready for the site

### `reading_status`
**Type:** enum

Valid values: `want-to-read` | `reading` | `read` | `understood`

- `want-to-read`: stub only — haven't opened the paper yet
- `reading`: in progress
- `read`: read the paper, entry may still be draft
- `understood`: read, and have a confident mental model of the system

### `indexed_by`
**Type:** string — **Required**

GitHub handle or name of whoever wrote or reviewed this entry.

### `indexed_date`
**Type:** date string (YYYY-MM-DD) — **Auto-set**

Date the stub was first created.

---

## Body Sections

The Markdown body (after the frontmatter) follows this structure.
All sections marked **Required for published** must be filled before setting `status: published`.
Each section has exactly one job — do not repeat content across sections.

### `## Key Contributions` — Required for published
3–5 bullets. Each must be a **concrete artifact**: a named algorithm, data structure,
protocol, or measurement — with a brief mechanism (one line). Not "we show X is possible."

The problem context and key numbers should be **implicit** here — a reader should understand
what was broken and what the result was without separate Problem or Key Contributions sections. Include
hardware + model + metric + baseline inline on the bullet that is the primary result.

### `## Trade-offs` — Optional, renders on site
Short bullets on what the approach gives up to achieve its gains: speed vs accuracy,
memory vs compute, throughput vs latency, complexity vs generality.
Leave empty if the paper doesn't make meaningful trade-offs.

### `## Nuances` — Optional, renders on site
Short bullets for implementation gotchas, subtle assumptions, conditions that break the
approach, and limitations — things a practitioner discovers only by reading carefully or
attempting an implementation. This is the home for academic "limitations" content; keep
it practitioner-focused rather than hedged.

Examples:
- "Requires contiguous KV blocks — incompatible with PagedAttention out of the box"
- "Only linear A→B pipelines evaluated; DAG topologies would require protocol changes"
- "Benchmarks use synthetic workloads; real request distributions may shift the speedup"

### `## Findings` — Optional, renders on site
For measurement, characterization, or survey papers: a bullet-point enumeration of the
concrete findings. Use this when the paper's primary contribution is data and analysis
rather than a new system or algorithm.

Each bullet should be a specific quantitative or qualitative finding — something the
authors measured or characterized, not a claim about their system's performance.

Examples:
- "Scheduling goodput exceeds 95% in Google's TPU fleet; runtime overhead (crashes,
  restarts, checkpointing) is the dominant inefficiency, not hardware utilization"
- "Disaggregation improves TTFT/throughput only for prefill-heavy workloads;
  generation-heavy traffic sees no benefit and higher overhead"

Omit for systems/algorithmic papers where `## Key Contributions` already captures results.

### Discussion files — internal only, never rendered
Per-paper Q&A lives in `data/discussions/<slug>.md`. These are questions you ask about the
paper during or after reading, with answers stored for future reference.

Format (append new entries with the date as a heading):
```
## YYYY-MM-DD

**Q:** Your question here.

**A:** Answer here.

---
```

These files are never read by the site generator. They are private research notes.
