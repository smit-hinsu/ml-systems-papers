# ML Systems Papers — Project Guide for Claude

This is a semi-structured, static-site paper index for ML systems research, currently covering
all 135 oral presentations from MLSys 2026. The site is generated from YAML+Markdown files in
`data/papers/`, organized by optimization principle, domain, and topic rather than by date or
conference track. The target audience is senior ML systems engineers deciding whether to read a paper.

---

## Project architecture

```
data/
  papers/          # 135 .md files — one per paper (YAML frontmatter + Markdown body)
  principles.yaml  # 15 cross-cutting optimization principles (the core taxonomy)
  domains.yaml     # 9 ML systems domains
  topics.yaml      # ~20 concrete technique tags
  venues.yaml      # conference registry
  site.yaml        # site-wide config (title, GitHub, analytics)
scripts/
  generate_html.py # Jinja2 → site/ (run with --dev to include draft papers)
  validate.py      # schema + registry + char-limit checks (run after any edit)
  check_quality.py # heuristic content quality checks (vague language, missing numbers)
  new_paper.py     # creates a stub from a venue URL
  fetch_slides.py  # Playwright-based scraper for slides URLs (requires browser login)
  fetch_metadata.py # fetches citation counts from OpenAlex
  summarize_paper.py # helper for running the LLM summarization prompt
templates/         # Jinja2 templates (base, index, paper, tag, search pages)
site/              # generated output (gitignored; never edit by hand)
prompts/
  paper_summary.md # the master LLM prompt for generating paper entries
docs/
  schema.md        # complete field reference
  summarizing.md   # quality bar guide for human-written summaries
```

**Build the site:**
```bash
source .venv/bin/activate
python scripts/generate_html.py          # production: skips drafts
python scripts/generate_html.py --dev    # dev: includes all 135 draft papers
open site/index.html                     # or serve with: python -m http.server 8123 -d site
```

**Validate after any edit:**
```bash
python scripts/validate.py
```
Errors block publishing; warnings on draft papers are advisory. All 135 papers must pass
before committing.

---

## The taxonomy: why principles are the spine

The index is organized primarily around **principles** — 15 general optimization ideas that
recur across papers regardless of domain or era:

| Slug | Label | Category |
|---|---|---|
| `cache` | Cache to avoid repeated computation | efficiency |
| `pipeline` | Pipeline independent work to hide latency | efficiency |
| `skip` | Skip provably unnecessary work | efficiency |
| `fuse` | Fuse operations to minimize memory bandwidth | memory |
| `tier` | Keep hot data near compute | memory |
| `recompute` | Recompute to save storage | memory |
| `quantize` | Quantize to trade precision for efficiency | efficiency |
| `approximate` | Approximate to trade quality for efficiency | efficiency |
| `speculate` | Speculate to hide sequential latency | efficiency |
| `batch` | Batch to amortize fixed overheads | efficiency |
| `balance` | Balance load to maximize utilization | distributed |
| `specialize` | Specialize divergent workloads for independent optimizations | distributed |
| `elastic` | Scale elastically to fill spare capacity | distributed |
| `search-ai` | Search with AI for verifiable problems | tooling |
| `portable` | Abstract hardware to preserve deployment optionality | tooling |

**Slug stability.** Slugs are short mechanism-words (`cache`, `pipeline`) chosen to be stable
even if labels change. If the wording of a label needs updating, edit only `data/principles.yaml`
— no paper files need to change.

**Why principles, not topics?** Topics (kv-cache, speculative-decoding, etc.) describe
*what* a paper does. Principles describe *why* it works. A reader searching for "papers that
improve GPU utilization" is looking for `balance`, not a specific technique. Two papers that
both exploit the same principle are intellectually related even if they use completely different
mechanisms.

**The observations field is the bridge.** Each paper's `observations` dict maps principle
slugs to one-sentence paper-specific insights — not restatements of the principle, but what
*this* paper specifically noticed that made the principle applicable:

```yaml
# BAD — just restates the principle
observations:
  cache: "shared prefixes can be cached to avoid redundant prefill"

# GOOD — paper-specific
observations:
  cache: "agentic workloads share system prompt prefixes, but the radix cache
    fills only after a call completes — concurrent calls within the same turn don't benefit"
```

**Picking principles strictly.** Principles should only appear when the paper explicitly builds
on or measures that principle. The most common mistake is assigning `balance` to any paper that
mentions load balancing tangentially, or `cache` to any paper that uses any form of caching.
The test: could a colleague read the paper and say "yes, this paper's core contribution is
about caching to avoid repeated computation"?

---

## Schema design decisions

### Character limits are UI constraints, not style guidelines

`problem` (160 chars) and `key_results` (160 chars) appear in index cards. `observations` values
(200 chars) appear in paper-page headers. These limits are hard: the template truncates at
these lengths. Staying within them forces useful compression — a 180-char problem field is a
sign that two sentences were smuggled in as one.

### `problem` must be practitioner voice

The problem field should read like something an engineer would say at a whiteboard, not like
an academic abstract introduction. Reject anything that:
- Opens with "Large language models..." or "Modern systems..."
- Describes a research gap rather than a cost or breakage
- Could be substituted into a different paper without noticing

The test: would a systems engineer at Google/Meta recognize this as their real problem?

### `key_results` must have hardware + model + metric + baseline

Vague results are useless. A reader scanning the index needs to know if the speedup applies
to their hardware and their model scale. Pattern: `N× [metric] vs. [baseline] on [model] at
[batch/context] on [hardware]`. Numbers are required by `validate.py`.

### `status: draft` vs `status: published`

`draft` papers are excluded from the production site build; they only appear with `--dev`. All
135 current papers are `status: draft`. Before publishing any paper, the entry needs:
- All required fields filled
- `## Key Contributions` section written
- `validate.py` passing with no errors for that file

The intent is that `status: published` is a quality gate — the entry has been reviewed by a
human, not just auto-generated.

### `research_or_industry`

Use `industry` when the paper primarily reports a production system from a tech company with
little novel algorithmic contribution (e.g., CATWILD, GUARD, SHIP, ml-fleet-tpu-goodput).
Use `research` for university papers and papers with clear algorithmic novelty. Use `mixed`
for joint academic/industry papers where the contribution is both novel and deployed.

---

## Content generation pipeline

### Approach: OpenReview API + Semantic Scholar + arXiv

The full-scale generation process used for MLSys 2026 worked as follows:

1. **Discover all papers**: The MLSys 2026 virtual site (`mlsys.org/virtual/2026`) is
   JS-rendered and requires login — scraping it directly gives only shell HTML. Instead:
   - Fetched the static **calendar page** (`/virtual/2026/calendar`) which lists all oral IDs
     and titles in plain HTML
   - Fetched all papers from the **OpenReview v2 API** (no auth required):
     `https://api2.openreview.net/notes?content.venueid=MLSys.org/2026/Conference`
   - Matched titles between the two sources to get the full set with `venue_url` + `openreview_url`

2. **Create stubs**: `new_paper.py` creates a minimal frontmatter-only `.md` file with
   slug, title, venue_url, openreview_url, and empty content fields.

3. **Enrich stubs**: For each paper:
   - Search Semantic Scholar for arXiv ID: `https://api.semanticscholar.org/graph/v1/paper/search?query=TITLE&fields=title,externalIds`
   - If arXiv ID found: fetch abstract page for author affiliations
   - If not: use OpenReview `authorids` field — email domains reveal organizations
     (e.g., `congzhul@amazon.com` → Amazon, `kimham@kth.se` → KTH)
   - For academic profile IDs (`~Name_Surname1`), use the OpenReview profiles API:
     `https://api2.openreview.net/profiles?id=~Name_Surname1` — returns `content.history`
     with institution names

4. **Generate summaries**: Use the prompt in `prompts/paper_summary.md` with the abstract
   as input. The prompt produces a complete `.md` entry with all frontmatter and body sections.

5. **Validate and fix**: `python scripts/validate.py` — fix all errors; warnings are advisory
   for drafts. `python scripts/check_quality.py` — heuristic checks for vague language.

6. **Taxonomy critic pass**: After bulk generation, run a read-only review agent across all
   papers to find: principle misapplications, observations that just restate principles, missing
   principles, wrong domain classifications. Apply corrections manually.

### The summarization prompt (`prompts/paper_summary.md`)

The prompt encodes all quality rules in a single `<prompt>` block. Key design decisions:

- **Anti-patterns table**: A table of wrong→right examples is more effective than prose rules.
  The model has seen these patterns in training; naming them directly suppresses them.
- **Sections have one job**: Each section (`## Key Contributions`, `## Trade-offs`,
  `## Nuances`, `## Findings`) has an explicit scope. Repetition across sections is the most
  common generation failure — the prompt names this explicitly.
- **`## Findings` is optional and conditional**: Only for measurement/characterization papers.
  The prompt specifies when to include vs. omit it. Adding this reduced the most common content
  error: calling everything "Key Contributions" even when the paper's contribution is data.
- **Taxonomy inline in the prompt**: Valid principle slugs, domain slugs, and topic slugs are
  all listed in the prompt with brief descriptions. Without this, models invent slugs or pick
  the closest-sounding wrong one.
- **Observations guidance is explicit**: The prompt gives a bad→good example pair specifically
  for observations because this is the hardest field to get right. Models default to restating
  the principle; the example shows what paper-specificity looks like.

**Evolving the prompt**: When correcting a generated entry, ask whether a rule or example could
prevent that class of error. Edit `prompts/paper_summary.md` and note the change in the
"Prompt iteration log" at the bottom of `docs/summarizing.md`.

### Parallel agent generation

For bulk generation of 100+ papers, split into batches of ~18 and run as parallel background
agents. Key lessons:

- **Session limits**: Agents (especially if doing many web fetches) hit API rate limits partway
  through large batches. Design batches to be resumable — each paper is written independently,
  so partial completion is fine; just relaunch for the remaining stubs.
- **Permissions**: Sub-agents inherit from `.claude/settings.local.json`. The current config
  allows `WebFetch(*)` and broad `Bash(*)` patterns. Without this, agents block on permission
  prompts and cannot proceed. Do not revert this to narrow allowlists — it breaks agents.
- **Skill interference**: Prompts that mention "permissions" or "settings" can accidentally
  trigger the `fewer-permission-prompts` skill in sub-agents. Keep agent prompts task-focused:
  start with "Your ONLY job is to write paper files", read the batch JSON, write files, validate.
  Never mention skills or settings in agent prompts.
- **Agent results vs. summaries**: An agent's completion summary often describes what it
  *intended* to do or what skill it triggered — not what it actually wrote. Always verify
  by counting stub files (`for f in data/papers/*.md; do ... done | wc -l`) rather than trusting
  the agent's self-report.
- **Rate limiting external APIs**: Add 0.3–1s delays between calls to Semantic Scholar
  (returns 429 quickly), OpenReview (more forgiving), and arXiv. Do not parallelize API calls
  within a single agent — fetch serially with delays.

---

## Validation and quality checks

### `scripts/validate.py` — schema correctness

Checks every `.md` file in `data/papers/`. Severity model:
- **Error** (exit code 1): blocks publishing; only applies to `status: published` papers.
  Covers: missing required fields, invalid enum values, unknown registry slugs.
- **Warning** (exit code 0): advisory; applies to all papers including drafts.
  Covers: character limit violations, vague language in `key_results`, missing digits,
  observations that word-overlap too closely with their principle description,
  cross-paper duplicate observation text.

Run this after every edit. The output format is `filename: description` for both warnings
and errors. Fix all errors for published papers; fix warnings in the same edit when convenient.

### `scripts/check_quality.py` — content heuristics

Runs on top of `validate.py` with additional checks:
- `key_results` names neither hardware nor a model → WARN
- `key_results` has `outperforms` without naming a specific baseline → WARN
- `## Key Contributions` bullets lack a bold-named artifact (`**Name**:`) → WARN
- Problem field is empty or starts with a forbidden prefix → FAIL

Can also run in `--llm` mode to use Claude Haiku for per-paper critique:
```bash
python scripts/check_quality.py --llm --slug flashagents
```
The LLM check evaluates: problem voice specificity, Key Contributions specificity,
observation specificity, and missing nuances.

### What validators do NOT check

- Whether the observations are accurate (requires reading the paper)
- Whether the principles were chosen correctly (requires domain knowledge)
- Whether the key_results number is actually in the paper (no citation)
- Whether organizations are correct (no ground truth)

The taxonomy critic pass (spawned as a review agent after bulk generation) fills some of
these gaps by cross-checking principles against observations for consistency.

---

## Site generation

`scripts/generate_html.py` reads all `.md` files, renders them through Jinja2 templates, and
writes `site/`. The output is a fully static site with no JavaScript dependencies except an
optional analytics snippet.

**Key flags:**
- `--dev`: include `status: draft` papers (excluded by default). Use during development and to
  preview new papers before publishing. The paper count in the footer shows `N/M papers indexed`
  where N = papers with `reading_status: read` or `understood`, M = total displayed.
- No flag needed for production — run plain `python scripts/generate_html.py` before deployment.

**Deployment:** GitHub Pages at `smit-hinsu.github.io/ml-systems-papers`. GitHub Actions
(`.github/workflows/deploy.yml`) rebuilds and deploys on every push to `main`.

**Custom domain:** `mlsys26.hinsu.org` — configure via CNAME record pointing to
`smit-hinsu.github.io`. Add a `CNAME` file to `site/` or configure in GitHub Pages settings.

**Analytics:** `data/site.yaml` has an `analytics_html` field. Paste the analytics provider
snippet (Plausible, GoatCounter, etc.) there. It renders in the `<head>` of every page.

---

## Taxonomy maintenance

### Adding a new principle

Principles are stable — they represent general CS optimization ideas that transcend any
specific ML system. Before adding a new one, verify it cannot be expressed as a combination of
existing principles. New principles require:
1. Add to `data/principles.yaml` with `label`, `category`, and `description`
2. Update `prompts/paper_summary.md` (the taxonomy section)
3. Update `docs/schema.md` (the principles table)

### Adding a new domain or topic

`data/domains.yaml` and `data/topics.yaml` are the canonical registries. Add entries there
first. Reference the slug in paper files after the registry entry exists — `validate.py` will
catch forward references.

Topics use `all-reduce` style formatting (see `data/topics.yaml`). Note that as of the current
state, `topics.yaml` contains `all-reduce` as a slug but several paper files reference
`memory-management`, `prefill-decode-disaggregation`, `expert-parallelism`, `sparse-attention`,
`pruning` — these were added by the generation agents and need to be added to the registry
to pass validation. Before editing paper files to fix these, add the missing slugs to `topics.yaml`.

### Registry drift from bulk generation

Bulk AI generation introduces slugs not in the registries. After any large generation pass:
```bash
python scripts/validate.py 2>&1 | grep "unknown.*slug"
```
For each unknown slug, decide: add it to the registry (if it belongs), or edit the paper
files to use an existing slug. Do not silently add every generated slug — evaluate each one.

---

## Lessons learned from MLSys 2026 generation

### What worked

- **OpenReview v2 API** for bulk paper discovery. No auth required; returns abstracts, authors,
  forum IDs. Key: use `api2.openreview.net`, not `api.openreview.net` (v1 returns nothing).
- **Calendar page title matching** to link OpenReview forum IDs to venue oral IDs. The calendar
  (`/virtual/2026/calendar`) has all titles and oral IDs in static HTML; normalize both sides
  (lowercase, strip punctuation) before matching.
- **OpenReview `authorids` for organizations**. Email domains are reliable for industry authors.
  For academic profile IDs (`~Name1`), the profiles API returns `content.history[].institution`.
- **Splitting 135 papers into 6–8 batches** of ~18 papers each, run as parallel background
  agents. Each batch takes 8–15 minutes; 6 in parallel completes 100+ papers in ~15 minutes.
- **The `## Findings` section** for characterization papers (beyond-the-buzz, ml-fleet,
  demystifying-moe-tax) was added after the first generation pass. It solved a persistent
  content confusion where measurement papers were written as if they built a system.

### What failed

- **mlsys.org virtual site scraping**: The site is JS-rendered (Django + jQuery). Raw HTTP
  fetches return only shell HTML — no slides URLs, no OpenReview links. Even Playwright
  headless couldn't get action buttons, which are gated behind session authentication.
  **Do not attempt to scrape mlsys.org without a logged-in browser session.**
  Alternative: use OpenReview API + calendar page (see above).

- **First-pass principle selection was systematically wrong**. The initial generation assigned
  `cache` to anything involving caching, `pipeline` to anything with parallelism, and `balance`
  to anything distributed. A post-generation taxonomy critic pass (a single read-only review
  agent across all papers) fixed ~15 high-priority errors. Lesson: always run a critic pass
  after bulk generation. Never trust principle assignments without review.

- **Agents triggering wrong skills**: When agent prompts mention "permissions" or
  "allow/deny", the `fewer-permission-prompts` skill sometimes fires instead of the intended
  task. The agent's completion summary then describes the skill's output rather than the
  paper files written. Guard against this by opening prompts with "Your ONLY job is to write
  paper files. Do NOT run any skills or slash commands."

- **Trusting agent completion summaries**: Several agents reported doing work they didn't do.
  Batch B (18 papers) reported running `fewer-permission-prompts` but actually wrote all 18
  papers. Batch A re-launch got confused and ran the skill. Always verify by checking file
  modification times or line counts, not agent summaries.

- **Sub-agent WebFetch permissions**: The initial `.claude/settings.local.json` had narrowly
  scoped allowlists (individual curl commands by exact URL). Sub-agents hit permission prompts
  and blocked. Fixed by broadening to `WebFetch(*)` and pattern-based `Bash(*)`. Current
  `settings.local.json` allows all the tools agents need.

- **Semantic Scholar rate limits**: The API returns 429 quickly under parallel load. Always
  use serial fetches with 0.3–1s delays. For bulk lookups, Semantic Scholar is unreliable
  as a primary source — use it only to find arXiv IDs.

### Schema evolution during the project

The schema started with different field names (`mlsys_url`, `mlsys_official_category`,
`techniques`, `insights`) that were renamed during the first development session
(`venue_url`, `official_category`, `topics`, `principles`). The `data/schema.md` file
still has some legacy field names (`mlsys_url` in some tables) — these are documentation
artifacts. The canonical field names are in `docs/schema.md`.

The `arxiv_date` field was added by generation agents and appears in several paper files
that weren't in the original schema. It is harmless and will be used when `fetch_metadata.py`
is run, but it's not validated or displayed currently.

---

## Rejected design alternatives

### Rejected: per-paper discussion files rendered on the site

An early design had `data/discussions/<slug>.md` as private Q&A files. These were intentionally
excluded from `generate_html.py`. The schema documentation describes them as "internal only,
never rendered." Kept in the schema docs for completeness but not actively used.

### Rejected: insights as the primary taxonomy instead of principles

An early iteration called the core taxonomy "insights" (stored in `data/insights.yaml`,
referenced as `insights:` in paper files). This was renamed to `principles` because "insight"
implies something discovered in the paper, while "principle" communicates that these are
general, reusable ideas. The old field name still appears in `README.md` and some template
code — these are documentation artifacts.

### Rejected: techniques registry (renamed to topics)

Early schema had a `techniques` field (stored in `data/techniques.yaml`). Renamed to `topics`
and `data/topics.yaml` to better reflect that these are concrete method/algorithm tags, not
claimed technical novelties. The old name appears in `README.md` and `CONTRIBUTING.md`.

### Rejected: scraping mlsys.org for bulk discovery

The canonical approach tried first was Playwright headless scraping of the conference virtual
site. This works for page titles but fails for action URLs (slides, OpenReview links) which are
behind session auth. After confirming the limitation, switched to OpenReview API + calendar
page combination. The `fetch_slides.py` script still uses Playwright for updating
`slides_url` fields but requires the user to run it interactively after logging in.

### Rejected: one agent per paper (135 agents in parallel)

Spawning 135 individual agents would saturate rate limits immediately. Batches of 18 with 6
parallel agents struck the right balance: enough parallelism to complete quickly, small enough
batches that a session limit mid-batch only loses ~9 papers.

### Rejected: MFU as the primary fleet metric

The `ml-fleet-tpu-goodput` paper is the canonical reference for why MFU was insufficient: it
conflates scheduling, runtime, and program efficiency into one number, making waste
non-actionable. The MPG decomposition (Scheduling × Runtime × Program Goodput) is the design
adopted in that paper's taxonomy.

---

## Current state and next steps

### State (as of May 2026)

| Category | Count |
|---|---|
| Total papers | 135 |
| Full content written | ~130 |
| Remaining stubs | ~3–5 (batch A in progress) |
| Stubs with `organizations: []` | ~35 (stubs only; all full papers have orgs filled) |
| Validation errors (errors, not warnings) | 0 for published; ~100 warnings on drafts |
| Status: published | 0 — all papers are draft |

### Immediate next steps

1. **Confirm all stubs are done**: Run `for f in data/papers/*.md; do lines=$(wc -l < "$f"); if [ "$lines" -le 60 ]; then echo "$f"; fi; done` — any remaining stubs need manual summaries or agent re-runs.

2. **Fix validation warnings**: Run `python scripts/validate.py` and triage warnings:
   - Character limit overruns (problem/key_results/observations slightly over limit) — trim inline
   - "state-of-the-art" in key_results — replace with specific named baseline
   - Unknown topic slugs from generation — add to `data/topics.yaml` or fix the paper

3. **Taxonomy critic pass on new papers**: The original 22 papers had a critic pass; the 113
   generated in bulk have not. Spawn a review agent with access to all `data/papers/*.md` files
   and `data/principles.yaml` to flag principle misapplications, generic observations, and
   domain misclassifications.

4. **Publish and deploy**: Flip papers to `status: published` after review, run
   `generate_html.py` without `--dev`, push to trigger GitHub Actions deploy.

5. **slides_url**: Still empty for most papers. Run `python scripts/fetch_slides.py` after
   logging in to `mlsys.org` via a headed browser (the script will prompt for this).

6. **Custom domain**: Configure CNAME `mlsys26.hinsu.org` → `smit-hinsu.github.io` in
   DNS, and set custom domain in GitHub Pages settings.

7. **Analytics**: Sign up for GoatCounter (free, open-source) or Plausible, paste snippet
   into `analytics_html` in `data/site.yaml`.

### README and CONTRIBUTING are stale

`README.md` still references the old field names (`insights`, `techniques`) and shows the
paper count as 8. Update before deploying publicly. `CONTRIBUTING.md` references
`data/observations.yaml` (doesn't exist; correct is `data/principles.yaml`) and
`## Summary` section (renamed to `## Key Contributions`).

---

## Git workflow

**Never commit without being asked.** All commits go directly to `main` (no PR workflow for
the primary maintainer). Verify git identity before committing:
```bash
git config user.name   # should be "Smit Hinsu"
git config user.email  # should be "smittvhinsu@gmail.com"
```

Do not add `Co-Authored-By: Claude` or any Claude attribution to commit messages.
