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

---

## Track 1 — Per-paper review (quality gate)

Move each paper `under-review` → `published` after human review.

**Review checklist per paper:**
1. **Pre-review data check** — before reading, surface what's missing so the reviewer knows what they can't verify:
   - Is `arxiv_url` or `openreview_url` present? If neither, the reviewer has no PDF to check against.
   - Is `code_url` present? If not, note it as a find-during-review task.
   - Are `organizations` filled? If empty, taxonomy and industry/research classification can't be confirmed.
   - Flag these gaps upfront so the reviewer can push back or fill them before signing off.
2. Read the paper (arXiv or OpenReview abstract + intro)
3. Verify `key_results` — hardware + model + metric + baseline? ≤ 160 chars?
4. Verify `principles` — core contribution only, not tangential?
5. Verify `observations` — paper-specific insight, not principle restatement? ≤ 200 chars each?
6. Verify `domain` and `topics` — correct and complete?
7. Add `## Background` if the problem domain isn't obvious from the title
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

## Track 2 — Data quality at scale (after first 10 are reviewed)

Run these after reviewing the first 10 to establish the right quality bar before touching the remaining 125.

- [ ] Taxonomy critic pass on bulk 113 papers (agent scan for principle misapplications, generic observations, domain misclassifications)
- [ ] Batch trim char-limit violations (LLM agent — one pass for `problem`, one for `key_results`, one for `observations`)
- [ ] Fix `key_results` with no hardware or model (`check_quality.py` flags these)
- [ ] Fix `key_results` using "state-of-the-art" without a named baseline
- [ ] Identify ~20–30 papers needing `## Background` (hardware, compilers, specialized architectures, recs)
- [ ] Audit unknown topic slugs: `python scripts/validate.py 2>&1 | grep "unknown.*slug"`
- [ ] Add `attention-kernels` tagging to all papers that do attention kernel work (currently 2 known)

---

## Track 3 — Metadata completeness (automatable, no paper reading required)

- [ ] **`arxiv_url`**: ~60 papers missing — Semantic Scholar title search (serial, 0.5s delay)
- [ ] **`citations`**: run `scripts/fetch_metadata.py` after arxiv_url is populated; OpenAlex API
- [ ] **`code_url`**: ~110 papers missing — web search per paper (GitHub link usually in OpenReview or arXiv abstract); consider a batch agent
- [ ] **`slides_url`**: all empty — run `scripts/fetch_slides.py` after interactive login to mlsys.org (requires headed browser)
- [ ] **`organizations`**: ~35 stubs have `organizations: []` — fill from OpenReview author affiliations

---

## Track 4 — Usability

### Done
- [x] Sort order on homepage
- [x] 1-line `problem` summary on cards
- [x] Compact principle chips replacing verbose observation blocks
- [x] Status badges (reviewing / draft) in dev mode

### TODO
- [ ] **Remove "All Papers" nav link** — clicking the "ML Systems Papers" brand already navigates to the index; the link is redundant (`base.html.jinja2` line 213)
- [ ] **Redesign hero section** — current layout stacks title, tagline, paper count, then search below. Integrate into a single compact header: site name + tagline inline, paper count as a small badge, search box immediately below. Reduce vertical space consumed before papers appear.
- [ ] **Paper detail page**: show `code_url` / `slides_url` as action buttons; show citation count; render `## Background` section visually distinct (e.g., slightly different background)
- [ ] **Card layout — move domain/topic tags after authors**: currently tags appear at the bottom of the card after principles. Move domain and topic chips to immediately after the authors/orgs/venue meta row, so the paper's classification is visible before the summary and results.
- [ ] **Card layout — dedicated principles section**: move principles out of the tags row into their own labelled section between key_results and the domain/topic tags. Only the principle name should be the clickable/filterable element — not the full observation text (which is removed from cards anyway). This reduces tag-row clutter and gives principles visual prominence.
- [ ] **Filter UX**: clicking a principle chip filters the grid but there's no persistent sidebar — consider adding a compact filter strip above the grid showing active filters with X to clear each
- [ ] **Topics in search index**: `topic_labels` already in search index; verify Fuse.js weights are tuned correctly
- [ ] **Footer/deploy**: configure custom domain `mlsys26.hinsu.org` CNAME; add analytics snippet to `data/site.yaml`

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
