# MLSys 2026 Paper Index — Work Plan

Working document. Strike items as they complete. Per-paper TODOs exist so we don't re-derive
what's left each session — update them as work happens.

---

## What's already done

### Infrastructure
- [x] Schema: all required fields, char limits, enum validation (`scripts/validate.py`)
- [x] Quality heuristics (`scripts/check_quality.py`, `--llm` mode)
- [x] Site generation with Jinja2 templates (`scripts/generate_html.py`)
- [x] Homepage: sort order (published > under-review > draft, then award > ptype > citations > date > title desc)
- [x] Homepage: paper cards show `problem` as 1-line summary; principles as compact chips
- [x] Homepage: `under-review` amber badge, `draft` pink badge in dev mode
- [x] Status workflow: `draft` → `under-review` → `published` (only `published` in prod build)
- [x] Taxonomy: 15 principles in `data/principles.yaml`
- [x] Domains registry: 10 domains including `edge-inference`
- [x] Topics registry: added `prefill-decode-disaggregation`, `scheduling`, `memory-management`, `expert-parallelism`, `profiling`, `benchmarking`, `storage`, `hardware`, `interconnect`, `attention-kernels`
- [x] Taxonomy critic pass on original 22 papers

### Content
- [x] First-pass summaries for all 135 papers
- [x] All 135 papers: 0 warnings, 0 errors (`validate.py` clean as of 2026-05-26)
- [x] Taxonomy critic pass on all 135 papers; 34 papers corrected
- [x] `## Background` sections added to all 135 papers, trimmed to ≤80 words
- [x] `optimization_type` field added to schema, registry, templates; empty on all papers pending review

### Infrastructure additions (this session)
- [x] `?dev=1` URL flag — shows draft/reviewing status badges client-side without separate build
- [x] `scripts/review.py` — per-paper review brief: data gaps, validation, heuristics, LLM check
- [x] `check_quality.py` LLM prompt updated: adds optimization_type suggestion, domain/topic check, 6000-char body
- [x] `optimization_type` registry (`data/optimization_types.yaml`): algorithm, system, hardware, workflow, application

---

## Track 1 — Per-paper review (quality gate)

Move each paper `under-review` → `published` after human review.

**Review command (runs all checks automatically):**
```bash
python scripts/review.py <slug>            # full brief with LLM check
python scripts/review.py --no-llm <slug>  # skip LLM call (faster)
```

**Review checklist per paper:**
1. **Pre-review data check** — `review.py` surfaces this automatically:
   - `arxiv_url` or `openreview_url` present? (need a PDF to verify against)
   - `code_url` present? If not, find it during review (OpenReview / arXiv abstract)
   - `organizations` filled? Required for taxonomy and research/industry classification
2. Read the paper (arXiv or OpenReview abstract + intro)
3. **Decide on `## Background`** — remove it if the domain is obvious from the title + key_results to an ML systems engineer; keep (≤80 words) only when context is genuinely non-obvious (hardware NoC, GNNs, ZK proofs, diffusion LMs, recs, etc.)
4. Verify `key_results` — hardware + model + metric + named baseline? ≤ 160 chars?
5. Verify `principles` — core contribution only, not tangential?
6. Verify `observations` — framed as an observation ("X happens because…", "authors found…"), paper-specific, not a principle restatement? ≤ 200 chars each?
7. Verify `## Key Contributions` doesn't duplicate `principles`/`observations` — bullets that restate a principle already captured in the structured fields should be trimmed or moved to an **`## Other Key Contributions`** sub-section for engineering/infrastructure contributions not expressed by a principle
9. Verify `domain` and `topics` — correct and complete?
10. **Add `optimization_type`** — one or more of: `algorithm`, `system`, `hardware`, `workflow`, `application`; leave empty only for pure measurement/tooling papers
11. Fill `code_url`, `slides_url` if findable
12. Run `python scripts/validate.py` — zero warnings for this paper
13. Set `status: published`
14. Capture any systematic error found → add to Global Checklist below

### Paper status (as of 2026-05-26)
- 1 published · 9 under-review · 125 draft
- Run `python scripts/review.py <slug>` before reading each paper

### Paper TODOs (first batch — oral/award papers)

| # | Paper | Remaining tasks |
|---|---|---|
| 1 | **flashagents** (published) | [ ] find arxiv_url [ ] add optimization_type |
| 2 | **ml-fleet-tpu-goodput** | [ ] read [ ] verify taxonomy [ ] add optimization_type [ ] find code_url |
| 3 | **freescale-recs** | [ ] read [ ] verify taxonomy [ ] add optimization_type [ ] find code_url |
| 4 | **moeblaze** | [ ] read [ ] verify taxonomy [ ] add optimization_type [ ] find code_url |
| 5 | **accelerating-large-scale-reasoning-model-inference-with-spar** | [ ] read [ ] verify taxonomy [ ] add optimization_type [ ] find code_url |
| 6 | **kitty-accurate-and-efficient-2-bit-kv-cache-quantization-wit** | [ ] read [ ] verify taxonomy [ ] add optimization_type |
| 7 | **pike-pytorch-llm-agents** | [ ] read [ ] verify taxonomy [ ] add optimization_type |
| 8 | **flexicache-leveraging-temporal-stability-of-attention-heads-** | [ ] read [ ] verify taxonomy [ ] add optimization_type [ ] find code_url |
| 9 | **flashlight-pytorch-compiler-extensions-to-accelerate-attenti** | [ ] read [ ] verify taxonomy [ ] add optimization_type [ ] find code_url |
| 10 | **cdlm-consistency-diffusion-language-models-for-faster-sampli** | [ ] read [ ] verify taxonomy [ ] add optimization_type |

Remaining 125 draft papers: add rows here as you work through them, or track in a separate session.

---

## Track 2 — Data quality at scale

- [x] All 135 papers: 0 warnings, 0 errors in `validate.py` (2026-05-26)
- [x] All `key_results` "state-of-the-art" replaced with named baselines
- [x] All char-limit violations trimmed (problem ≤160, key_results ≤160, observations ≤200)
- [x] All `key_results` contain at least one digit
- [x] No unknown topic/principle slugs
- [x] Taxonomy critic pass on all 135 papers; 34 corrected (2026-05-26)
- [x] `## Background` added to all 135 papers, trimmed to ≤80 words (2026-05-26)
- [ ] `attention-kernels` tagging — audit all papers doing attention kernel work (2 known; likely more)
- [ ] `graph-learning` domain — decision pending: add domain for grinnder + g-hemp, or leave as `ml-kernels`

---

## Track 3 — Metadata completeness

Stats as of 2026-05-26: slides 112/135 · arxiv 24/135 · code 29/135 · orgs 135/135

- [x] **`organizations`**: all 135 filled
- [x] **`slides_url`**: 112/135 filled (23 missing) — ran `fetch_slides.py` after mlsys.org login
- [ ] **`slides_url`** (remaining 23): re-run `fetch_slides.py` to pick up stragglers; may need fresh login
- [ ] **`arxiv_url`**: 111/135 missing — Semantic Scholar title search, serial with 0.5s delays (batch agent)
- [ ] **`citations`**: 0/135 — run `scripts/fetch_metadata.py` after arxiv_url populated; OpenAlex API
- [ ] **`code_url`**: 106/135 missing — batch agent reads OpenReview/arXiv page per paper for GitHub link; NOT general web search

---

## Track 4 — Usability

### Done
- [x] Sort order on homepage
- [x] Compact principle chips replacing verbose observation blocks
- [x] Status badges (reviewing / draft) in dev mode
- [x] Brand clickable (links to index)
- [x] Hero redesign: compact inline title + tagline + badge count; search immediately below
- [x] Card layout: domain/topic tags after meta row; principles in separate labelled section after key_results
- [x] Filter UX: dismissable chip with colour-coded badge shows active filter; click × to clear
- [x] Paper detail page: `## Background` section rendered with blue callout box (via JS)

### TODO
- [ ] **`optimization_type` filter**: tags render on cards and paper pages; no UI filter chip yet in the section nav — add when enough papers are tagged to make filtering useful
- [ ] **Analytics**: add GoatCounter snippet to `analytics_html` in `data/site.yaml` (needs account URL)
- [ ] **Fuse.js weights**: `topic_labels` in search index; verify weights are well-tuned

---

## Global checklist — adding or reviewing any paper

Use this to avoid the most common generation errors found during review.

### Field rules

**`problem`** (≤ 160 chars)
- [ ] Practitioner voice — "X breaks / costs Y at scale" not "This paper addresses..."
- [ ] No opener: "Large language models...", "Modern systems...", "Recent advances..."
- [ ] Describes a cost or breakage, not a research gap
- [ ] Substitution test: would this fit a different paper? If yes, rewrite

**`key_results`** (≤ 160 chars)
- [ ] Must include: metric, comparison baseline, model/workload, hardware
- [ ] Pattern: `Nx [metric] vs. [baseline] on [model] on [hardware]`
- [ ] No "state-of-the-art" — name the specific baseline
- [ ] Numbers required — validate.py checks this

**`principles`**
- [ ] Only principles that are the core mechanism of the paper's contribution
- [ ] Test: could a colleague read the paper and say "yes, this paper is fundamentally about [principle]"?
- [ ] `balance` ≠ any distributed paper; `cache` ≠ any paper that uses caching; `pipeline` ≠ any parallel system
- [ ] 2–4 principles typical; 1 is fine; 5+ usually means over-tagging

**`observations`** (≤ 200 chars each)
- [ ] Framed as an observation: "X happens because…", "authors measured…", "the bottleneck is…" — not a feature description
- [ ] Paper-specific: what did *this* paper notice that made the principle applicable?
- [ ] Fails if it could be copy-pasted to a different paper using the same principle
- [ ] Must not restate the principle description — validate.py checks word-overlap

**`domain`**
- [ ] 1–2 domains max; pick the tightest fit
- [ ] `llm-serving` ≠ any inference paper — use for serving *systems* (batching, scheduling, disaggregation)

**`topics`**
- [ ] Concrete technique tags only — what method does the paper use?
- [ ] Add to `data/topics.yaml` first if the slug doesn't exist

**`optimization_type`** (new field — fill during review)
- [ ] `algorithm` — new formula, method, or computation strategy
- [ ] `system` — engineering change without fundamental algorithmic novelty
- [ ] `hardware` — hardware design or deep hardware-software co-design
- [ ] `workflow` — training recipe, eval methodology, operational process
- [ ] `application` — domain-specific trick exploiting application-layer properties
- [ ] Multiple values are expected for most papers; empty only for pure measurement papers
- [ ] `review.py` LLM check suggests values — verify before accepting

### Content rules

- [ ] `## Key Contributions`: each bullet has a **bold named artifact** — `**SystemName**:`, `**AlgorithmName**:`
- [ ] `## Key Contributions` must not duplicate `principles`/`observations` — if a bullet just restates a principle already in the structured fields, remove it or consolidate into an `## Other Key Contributions` section for engineering/infrastructure work not captured by a principle
- [ ] `## Background`: keep only when domain is non-obvious to an ML systems engineer; remove if title + key_results make context clear
- [ ] `## Findings`: add *only* for measurement/characterization papers; omit for system-building papers
- [ ] No repetition across sections — each section has one job
- [ ] `research_or_industry`: use `industry` when it's a production system report with little algorithmic novelty

### Metadata
- [ ] Fill `code_url` if a GitHub repo exists (check OpenReview, arXiv abstract, paper PDF)
- [ ] Fill `arxiv_url` if the paper is on arXiv
- [ ] Run `python scripts/validate.py` — zero warnings for this paper before publishing
- [ ] Run `python scripts/check_quality.py --llm --slug SLUG` for a second opinion

### Common mistakes found in review
*(append here as we find them)*

- **`skip` principle overused**: assigned to any paper with sparsity or pruning, even when the paper's core contribution is the quantization method, not the skipping decision.
- **Observation = principle restatement**: e.g. `cache: shared prefixes can be cached` — adds no paper-specific information.
- **Observation framed as a feature, not a finding**: e.g. `pipeline: overlaps prefill and decode` describes what the system does, not what the authors observed. Rewrite as: `pipeline: prefill and decode have no data dependency between requests, so their GPU time can be overlapped without correctness risk`.
- **Key Contributions duplicates principles**: if `cache` is a principle and a bullet says "we cache KV states to avoid recomputation", the bullet adds nothing — either remove it or expand it to describe the specific caching mechanism in a way the principle doesn't capture.

---

## Feedback loop — propagating learnings to later papers

After reviewing each batch of ~10 papers:
1. List the 2–3 most common errors found
2. Write a targeted agent prompt or script to detect and fix those errors in the remaining papers
3. Update `prompts/paper_summary.md` so future generation avoids the same errors
4. Update the "Common mistakes" section above
