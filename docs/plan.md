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
- [x] Taxonomy critic pass on original 22 papers (not yet done on bulk 113)
- [x] `## Background` section: NoC paper
- [x] Validation warnings on first 10 papers: zero
- [x] All 135 papers: 0 warnings, 0 errors (`validate.py` clean as of 2026-05-26)
- [x] Taxonomy critic pass on bulk 113 papers (in-progress agent, findings to be applied)

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
3. Verify `key_results` — hardware + model + metric + named baseline? ≤ 160 chars?
4. Verify `principles` — core contribution only, not tangential?
5. Verify `observations` — paper-specific insight, not principle restatement? ≤ 200 chars each?
6. Verify `domain` and `topics` — correct and complete?
7. **Add `optimization_type`** — one or more of: `algorithm`, `system`, `hardware`, `workflow`, `application`; leave empty only for pure measurement/tooling papers
8. Fill `code_url`, `slides_url` if findable
9. Run `python scripts/validate.py` — zero warnings for this paper
10. Set `status: published`
11. Capture any systematic error found → add to Global Checklist below

### Paper TODOs

| # | Paper | Remaining tasks |
|---|---|---|
| 1 | **flashagents** (published) | [ ] find arxiv_url [ ] verify taxonomy [ ] background? |
| 2 | **ml-fleet-tpu-goodput** | [ ] read paper [ ] verify taxonomy [ ] background (industry/fleet paper — may need context) [ ] find code_url |
| 3 | **freescale-recs** | [ ] read paper [ ] verify taxonomy [ ] background (recs domain — non-obvious for LLM engineers) [ ] find code_url |
| 4 | **moeblaze** | [ ] read paper [ ] verify taxonomy [ ] background? [ ] find code_url |
| 5 | **accelerating-large-scale-reasoning-model-inference-with-spar** | [ ] read paper [ ] verify taxonomy [ ] find code_url [ ] find slides_url |
| 6 | **kitty-accurate-and-efficient-2-bit-kv-cache-quantization-wit** | [ ] read paper [ ] verify taxonomy [ ] find slides_url |
| 7 | **pike-pytorch-llm-agents** | [ ] read paper [ ] verify taxonomy |
| 8 | **flexicache-leveraging-temporal-stability-of-attention-heads-** | [ ] read paper [ ] verify taxonomy [ ] find code_url [ ] find slides_url |
| 9 | **flashlight-pytorch-compiler-extensions-to-accelerate-attenti** | [ ] read paper [ ] verify taxonomy [ ] background (compiler domain) [ ] find code_url [ ] find slides_url |
| 10 | **cdlm-consistency-diffusion-language-models-for-faster-sampli** | [ ] read paper [ ] verify taxonomy [ ] background (diffusion LM — non-obvious) [ ] find slides_url |

---

## Track 2 — Data quality at scale

- [x] All 135 papers: 0 warnings, 0 errors in `validate.py` (2026-05-26)
- [x] All `key_results` "state-of-the-art" replaced with named baselines
- [x] All char-limit violations trimmed (problem ≤160, key_results ≤160, observations ≤200)
- [x] All `key_results` contain at least one digit
- [x] No unknown topic/principle slugs
- [x] Taxonomy critic pass on bulk 113 papers (2026-05-26)
- [x] Apply taxonomy critic findings: 34 papers corrected (2026-05-26)
  - 7 speculative-decoding papers gained `speculate` principle (was 0/135)
  - 5 quantization papers gained `quantize` principle (was 0/135)
  - `recompute`, `elastic`, `portable`, `approximate`, `specialize` now have 1-2 correct assignments each
  - ~17 wrong `cache` removals, ~6 wrong `balance` removals, ~2 wrong `fuse`/`pipeline` removals
  - 7 measurement/tooling papers correctly have no principles (blueprint, charon, csle, profinfer, osworld, driftbench, cost-aware)
  - reparo domain fixed: `llm-serving` → `edge-inference`
  - grinnder + g-hemp domains fixed: `llm-training`/`llm-serving` → `ml-kernels` (GNN papers; no dedicated domain exists yet)
- [ ] Identify ~20–30 papers needing `## Background` (hardware, compilers, specialized architectures, recs)
- [ ] Add `attention-kernels` tagging to all papers that do attention kernel work (currently 2 known)
- [ ] Consider adding `graph-learning` domain for grinnder + g-hemp (GNN papers misfit current taxonomy)

---

## Track 3 — Metadata completeness

- [ ] **`slides_url`**: all empty — requires one interactive login to mlsys.org, then headless:
  1. `! source .venv/bin/activate && python scripts/fetch_slides.py` — opens browser, log in, session saved to `data/.auth_mlsys-2026.json`
  2. Subsequent runs are headless and update all 135 papers
- [ ] **`arxiv_url`**: ~60 papers missing — Semantic Scholar title search, serial with 0.5s delays (batch agent)
- [ ] **`citations`**: run `scripts/fetch_metadata.py` after arxiv_url is populated; OpenAlex API
- [ ] **`code_url`**: ~110 papers missing — read OpenReview/arXiv page per paper to find GitHub link in abstract or PDF (batch agent); NOT general web search
- [ ] **`organizations`**: ~35 stubs have `organizations: []` — fill from OpenReview author affiliations

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
- [ ] **Topics in search index**: `topic_labels` already in search index; verify Fuse.js weights are tuned correctly
- [ ] **Analytics**: site live at https://smit-hinsu.github.io/ml-systems-papers/ — add snippet (GoatCounter or Plausible) to `analytics_html` field in `data/site.yaml`

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
- [ ] `## Background`: add when the problem domain isn't obvious from the title (hardware, compilers, recs, specialized architectures)
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

---

## Feedback loop — propagating learnings to later papers

After reviewing each batch of ~10 papers:
1. List the 2–3 most common errors found
2. Write a targeted agent prompt or script to detect and fix those errors in the remaining papers
3. Update `prompts/paper_summary.md` so future generation avoids the same errors
4. Update the "Common mistakes" section above
