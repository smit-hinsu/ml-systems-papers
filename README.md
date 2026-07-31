# ML Systems Papers

A community-maintained, semi-structured index of ML systems papers. The current corpus covers all 135 MLSys 2026 oral presentations and is organized by principle, domain, and topic rather than by conference or date.

## What's here

Each paper gets:
- Structured metadata: domain, topics, principles, optimization type, hardware, organizations, key results
- A one-line problem statement in practitioner voice
- A summary with key contributions, trade-offs, and nuances
- Cross-links to papers sharing the same principle or topic

Papers are browsable by:
- **Principle** — 16 cross-cutting optimization ideas that recur regardless of domain (e.g. "Cache to avoid repeated computation", "Speculate to hide sequential latency", "Simplify to remove mechanisms that cost more than they save"). Each paper's `observations` field records what *this* paper noticed that made the principle apply.
- **Domain** — 10 domains: LLM serving, LLM training, RL training, recommendation models, agentic inference, ML compilers, ML kernels, observability, fleet efficiency, edge inference
- **Topic** — 27 concrete technique tags: KV cache, speculative decoding, FSDP/ZeRO, quantization, kernel fusion, expert parallelism, etc.
- **Optimization type** — algorithm, system, hardware, workflow, application

## Current status

All 135 papers have full summaries and pass `validate.py` with zero errors and zero warnings.
Entries move through a review gate — `draft` → `under-review` → `published` — and the production
build publishes only reviewed papers. Use `--dev` to preview everything.

| | Count |
|---|---|
| Papers indexed (MLSys 2026) | 135 |
| `published` | 1 |
| `under-review` | 9 |
| `draft` | 125 |

Metadata completeness: `organizations` 135/135 · `slides_url` 112/135 · `arxiv_url` 68/135 · `code_url` 29/135 · `citations` 0/135.

*(counts as of 2026-07-31)*

## Quick start

```bash
git clone https://github.com/smit-hinsu/ml-systems-papers
cd ml-systems-papers
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Build the site (production: published papers only)
python scripts/generate_html.py
open site/index.html

# Build with drafts included, status badges shown
python scripts/generate_html.py --dev

# Validate papers — schema, registries, char limits
python scripts/validate.py

# Content quality heuristics (--llm for a per-paper LLM critique)
python scripts/check_quality.py

# Per-paper review brief before publishing
python scripts/review.py <slug>

# Add a new paper
python scripts/new_paper.py \
  --url "https://mlsys.org/virtual/2026/oral/XXXX" \
  --title "Paper Title" \
  --by your-github-username
```

## Repository structure

```
data/
  papers/                 # one .md file per paper (YAML frontmatter + Markdown body)
  principles.yaml         # canonical principle registry (the primary taxonomy)
  domains.yaml            # domain taxonomy
  topics.yaml             # concrete technique tags
  optimization_types.yaml # algorithm / system / hardware / workflow / application
  venues.yaml             # conference/venue registry
  site.yaml               # site-wide config (name, GitHub handle, analytics)
scripts/
  generate_html.py   # builds site/ from data/ (--dev includes drafts)
  validate.py        # schema, registry references, char limits
  check_quality.py   # content heuristics, optional LLM critique
  review.py          # per-paper review brief: data gaps, validation, LLM check
  new_paper.py       # creates a paper template from a URL
  fetch_metadata.py  # pulls citation counts from OpenAlex
  fetch_arxiv.py     # resolves arXiv URLs by title match
  fetch_slides.py    # scrapes MLSys virtual for slides URLs (needs a logged-in browser)
templates/           # Jinja2 HTML templates
site/                # generated output (gitignored)
docs/
  schema.md          # full field documentation
  summarizing.md     # quality bar for paper summaries
  plan.md            # working plan and review checklist
prompts/
  paper_summary.md   # the LLM prompt used to generate paper entries
CONTRIBUTING.md      # how to add papers
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/schema.md](docs/schema.md). The fastest way to help: pick any unindexed paper and open a PR with a new file in `data/papers/`. Run `python scripts/validate.py` before submitting.

## Adding a new conference

The pipeline is venue-agnostic. To index papers from another conference:
1. Add the venue to `data/venues.yaml`
2. Run `python scripts/new_paper.py` for each paper, referencing the new venue slug
3. Add domain/principle/topic entries to the registries as needed
