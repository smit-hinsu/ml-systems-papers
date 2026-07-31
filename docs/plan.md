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
- [x] `scripts/review.py` — per-paper review brief: data gaps, validation, heuristics, LLM check (prompt updated: observation framing + Key Contributions conciseness rules)
- [x] `check_quality.py` LLM prompt updated: adds optimization_type suggestion, domain/topic check, 6000-char body
- [x] `optimization_type` registry (`data/optimization_types.yaml`): algorithm, system, hardware, workflow, application

---

## Track 0 — Ship v1 (all 135 papers public)

**Decision (2026-07-31):** v1 publishes *all* 135 papers, not just human-reviewed ones. Review
continues after launch as a quality pass, not a gate.

- [ ] **Commit the working tree** — 51 modified + 3 untracked files are uncommitted (last commit
      `d6b0ebe`, local == origin/main). Contains: `simplify` principle added to registry and 5 papers,
      68 `arxiv_url` values, `review.py` updates, prompt updates, README rewrite. Untracked:
      `scripts/fetch_arxiv.py`, `scripts/fetch_arxiv_urls.py`.
- [x] **Decided how "publish everything" is implemented** (2026-07-31): the prod build renders
      **all** papers regardless of `status`, and `status` stays in the data as the internal review
      tracker — never rendered in prod. Review badges appear only under `--dev` / `?dev=1`.
      No mass-flip of the 135 files, so the record of which papers were actually reviewed survives.
- [ ] `generate_html.py`: drop the status filter from the prod path; render every paper
- [ ] Suppress status badges in prod templates (keep them behind `--dev` / `?dev=1`)
- [ ] Keep `status` out of the prod search index and any `data-*` attributes — "not in the prod
      build" means not in the shipped HTML at all, not merely hidden with CSS
- [ ] Naming wart to revisit: `status: published` now means "human-reviewed", not "visible on the
      site". Consider renaming the field to `review_status` with values `unreviewed` /
      `under-review` / `reviewed` once v1 is out.
- [ ] Add a short "these entries are AI-generated and under review" note to the site header/footer
- [ ] Build prod, spot-check, push → GitHub Actions deploy

---

## Track 1 — Per-paper review (quality pass, no longer a launch gate)

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
6. Verify `observations` — captures the *motivating insight* (what the paper noticed about the problem that made the principle applicable), not the solution; e.g. "agent B waits for A to complete despite having spare GPU capacity" not "we overlap prefill and decode"; ≤ 200 chars each?
7. Verify `domain` and `topics` — correct and complete?
8. **Add `optimization_type`** — one or more of: `algorithm`, `system`, `hardware`, `workflow`, `application`; leave empty only for pure measurement/tooling papers
9. Fill `code_url`, `slides_url` if findable
10. Run `python scripts/validate.py` — zero warnings for this paper
11. Set `status: published`
12. Capture any systematic error found → add to Global Checklist below

### Paper status (as of 2026-07-31)
- 1 published · 9 under-review · 125 draft — unchanged since 2026-05-26
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

### `simplify` back-tag sweep (incomplete)

`simplify` was added to the registry and applied to only **5 of 135** papers
(dataflow-is-all-you-need, fp8-flow-moe, intattention, matrix-p2p, parallelkittens). The sweep
never covered the rest of the corpus.

- [ ] Sweep all 135 papers for `simplify` candidates — papers whose win comes from *removing* a
      mechanism (a scheduler, a conversion stage, a specialization) rather than adding one
- [ ] Each new tag needs a matching `observations.simplify` entry (validator requires one)

### Full taxonomy consistency audit (all 135, not just under-review)

Current per-principle distribution is badly skewed, which is the signature of the over-tagging
failure mode already documented in CLAUDE.md:

| Principle | Papers | | Principle | Papers |
|---|---|---|---|---|
| `balance` | 57 | | `speculate` | 7 |
| `cache` | 48 | | `simplify` | 5 |
| `pipeline` | 38 | | `quantize` | 5 |
| `fuse` | 37 | | `recompute` | 2 |
| `tier` | 33 | | `specialize` | 1 |
| `skip` | 23 | | `portable` | 1 |
| `search-ai` | 15 | | `elastic` | 1 |
| | | | `approximate` | 1 |
| | | | `batch` | **0** |

- [ ] **`balance` audit (57 papers, 42% of corpus)** — the exact mistake CLAUDE.md warns about:
      "`balance` ≠ any distributed paper". Expect a large fraction to be untagged.
- [ ] **`cache` audit (48)** — same failure mode: "`cache` ≠ any paper that uses caching"
- [ ] **`pipeline` audit (38)** — "`pipeline` ≠ any parallel system"
- [ ] **`batch` has zero papers** — either it is genuinely unused (then consider removing it from
      the registry) or continuous/dynamic batching papers were tagged `balance`/`pipeline` instead
- [ ] **Under-used principles (`approximate`, `elastic`, `portable`, `specialize` at 1 each)** —
      check whether papers that should carry them were absorbed into the popular principles
- [ ] Re-check every paper has ≤4 principles (CLAUDE.md: "5+ usually means over-tagging")
- [ ] Verify every `principles:` entry has a matching `observations:` key — currently clean (0 gaps)

### Principle hierarchy

Deferred to Track 6 below — not required for v1.

---

## Track 3 — Metadata completeness

Stats as of 2026-07-31 (verified): slides 112/135 · arxiv 68/135 · code 29/135 · orgs 135/135 ·
openreview 135/135 · venue 135/135 · project 1/135

- [x] **`organizations`**: all 135 filled
- [x] **`slides_url`**: 112/135 filled (23 missing) — ran `fetch_slides.py` after mlsys.org login
- [ ] **`slides_url`** (remaining 23): re-run `fetch_slides.py` to pick up stragglers; may need fresh login
- [ ] **`arxiv_url`**: 68/135 filled (67 missing). Use `python scripts/fetch_arxiv.py` (arXiv API,
      1.5s delays, title-match validation); many remaining papers are industry-only and may have no
      arXiv ID. Note: `scripts/fetch_arxiv.py` and `fetch_arxiv_urls.py` are **untracked** — commit them.
- [ ] **`arxiv_url` malformed**: `kitty-accurate-and-efficient-2-bit-kv-cache-quantization-wit.md` has
      a bare ID `'2511.18643'` instead of a URL. Add a URL-format check to `validate.py` so this
      class of error can't recur.
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

## Track 5 — Media: posters, images, video recordings (future)

Not needed for v1. Each item needs a schema field before any fetching starts.

- [ ] **`poster_url`**: MLSys posts poster PDFs/PNGs on the virtual site per presentation. Same
      auth constraint as slides — extend `fetch_slides.py` rather than writing a new scraper, since
      it already handles the logged-in browser session.
- [ ] **`video_url`**: link to the published recording when the conference posts it (MLSys
      typically publishes talk videos on the virtual site and/or YouTube after the event). Needs a
      check for availability before a bulk pass — recordings may not exist yet for MLSys 2026.
- [ ] **Card/social images**: generate a per-paper image for link previews and card thumbnails.
      Two options: (a) render the poster's first page to a thumbnail, (b) generate an OG image from
      the paper's title + principles + key_results with PIL or headless Chrome. Option (b) is
      self-contained and works for all 135 regardless of poster availability — prefer it, and treat
      posters as an enrichment.
- [ ] **`og:image` meta tags** in `templates/base.html` once images exist — this is what makes
      shared links look right in Slack/Twitter/LinkedIn
- [ ] Storage decision: committed to the repo under `site/assets/` vs. generated at build time.
      Generated-at-build keeps the repo small but slows CI; 135 small WebPs is probably fine to commit.

---

## Track 6 — Principle hierarchy (future, post-v1)

Proposed representation, not yet implemented. Nothing here blocks v1.

**Tasks**
- [ ] Add `data/principle_groups.yaml` (6 groups: label + description)
- [ ] Rename `category:` → `group:` in `data/principles.yaml`; set the group for all 16 principles
- [ ] `validate.py`: papers may reference **leaf** slugs only — reject group slugs in `principles:`;
      every principle must declare a `group` that exists; enforce depth exactly 2
- [ ] `generate_html.py` + templates: group sections on the principles page, group label on
      paper-page chips, group filter pages (union of the group's leaves)
- [ ] Update `CLAUDE.md` principles table and `docs/schema.md` with the group column
- [ ] Update `prompts/paper_summary.md` — generation still picks leaves only; groups are
      navigation, so the prompt's taxonomy list does not change shape
- [ ] Confirm existing leaf URLs are unchanged (no link rot)

**The problem.** Some principles are subtypes of others — `quantize` is a special case of
`approximate` (trade fidelity for speed); `fuse` and `tier` are both about the memory hierarchy.
The flat list hides this, and the existing `category:` field (efficiency / memory / distributed /
tooling) is a weak, unnamed proxy for it: buckets with no descriptions and no page of their own.

**The constraint.** Papers keep tagging **leaf** principles only. A paper is `quantize`, never the
parent — parents are for navigation and reading, not tagging.

### Representation: two-level tree, single parent, groups replace categories

Add `data/principle_groups.yaml`, and in `principles.yaml` rename `category:` → `group:`. This
*replaces* a concept instead of adding one, and paper files don't change at all (they never
referenced `category`).

```yaml
# data/principle_groups.yaml
eliminate:
  label: "Eliminate the work"
  description: >
    The cheapest computation is the one that never runs. These principles find
    work that does not need to happen and remove it.
```

```yaml
# data/principles.yaml — only the field name and value change
cache:
  label: "Cache to avoid repeated computation"
  group: eliminate          # was: category: efficiency
  description: >
    ...
```

### Proposed tree (counts are current tags, pre-audit)

| Group | Leaves | Papers |
|---|---|---|
| **Eliminate the work** — find work that needn't happen | `cache` 48, `skip` 23, `simplify` 5 | 76 |
| **Trade exactness for speed** — same work, cheaper and less exact | `quantize` 5, `approximate` 1 | 6 |
| **Move data less** — the bottleneck is bandwidth, not FLOPs | `fuse` 37, `tier` 33, `recompute` 2 | 72 |
| **Hide latency** — work is fixed; overlap it | `pipeline` 38, `speculate` 7 | 45 |
| **Fill the machine** — work is fixed; remove idle time | `balance` 57, `batch` 0, `elastic` 1, `specialize` 1 | 59 |
| **Change who optimizes** — meta/tooling | `search-ai` 15, `portable` 1 | 16 |

This resolves the `approximate` / `quantize` case the natural way: both become siblings under a
parent named for the trade-off, so no leaf slug has to be renamed or re-parented into another leaf.
CLAUDE.md's slug-stability rule holds — group slugs are new, leaf slugs are untouched.

### Rendering

- **Principles page**: one section per group — group label as a heading, its one-sentence
  description, then the leaf cards with paper counts. The group heading itself links to a group
  page showing the union of its leaves' papers, with a leaf breakdown at the top.
- **Paper page**: chips gain a muted group label above the cluster, so a reader sees
  `Trade exactness for speed › Quantize to trade precision for efficiency` in context.
- **Existing leaf URLs are unchanged**, so nothing that is already linked breaks.

### Validation rules

- `principles:` in a paper may reference **leaf slugs only** — reject group slugs
- Every principle must declare a `group:` that exists in the registry
- Depth is exactly 2 — groups cannot nest

### Open question: `skip` has two plausible parents

`skip` sits under *Eliminate the work* when the skipped work is provably irrelevant, but under
*Trade exactness for speed* when it's sparse attention dropping tokens that do affect the output.
A multi-parent DAG would express this, at the cost of ambiguous per-group counts and a messier
page. **Recommendation: stay single-parent** (`skip` → Eliminate) and let each paper's
`observations.skip` carry the lossy-vs-lossless nuance.

---

## Global checklist — adding or reviewing any paper

Use this to avoid the most common generation errors found during review.

### Writing style (applies to every field and section)

Orwell's six rules are the house style — full text in `docs/summarizing.md`, enforced in
`prompts/paper_summary.md`.

- [ ] No print-worn metaphors: *unlocks, paves the way, at the heart of, seamlessly, leverages, harnesses*
- [ ] Short word over long: *utilize*→use, *methodology*→method, *in order to*→to
- [ ] Cut every cuttable word: *in the context of, it is worth noting that, a variety of*
- [ ] Active voice — name the actor
- [ ] No vague-academic register (*paradigm, holistic, novel framework, non-trivial*); terms of
      art (KV cache, prefill, all-reduce) are required and always beat this rule
- [ ] Break any rule sooner than write something inaccurate

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
- [ ] Captures the *motivating insight* about the problem — what the paper noticed that made the principle applicable
- [ ] Describes the problem/situation, not the solution: "agent B idles waiting for A despite spare GPU capacity" ✓ vs. "we overlap prefill and decode" ✗
- [ ] Paper-specific: fails if it could copy-pasted to a different paper using the same principle
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
- [ ] `## Key Contributions` assumes readers have read the principles and observations — skip re-explaining the principle or its motivation; focus on the specific mechanism, design decision, or artifact that delivers it
- [ ] Test: if a bullet could be fully replaced by just reading the principle label + observation, rewrite it to add the concrete detail that isn't already there
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
- **Observation describes the solution, not the problem**: e.g. `pipeline: overlaps prefill and decode` describes what the system does. Rewrite as the motivating insight: `pipeline: downstream agents idle waiting for upstream output despite having spare GPU capacity — the dependency is on the token stream, not the full response`.
- **Key Contributions restates the principle**: if `pipeline` is already a principle and an observation explains why, a bullet saying "we pipeline prefill and decode to hide latency" adds nothing. Instead: "**Incremental prefill protocol**: token-by-token forwarding via a modified SGLang HTTP endpoint; downstream scheduling begins after the first token, not after EOS".

---

## Feedback loop — propagating learnings to later papers

After reviewing each batch of ~10 papers:
1. List the 2–3 most common errors found
2. Write a targeted agent prompt or script to detect and fix those errors in the remaining papers
3. Update `prompts/paper_summary.md` so future generation avoids the same errors
4. Update the "Common mistakes" section above
