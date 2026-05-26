# ML Systems Papers

A community-maintained, semi-structured index of ML systems papers. The current corpus covers all 135 MLSys 2026 oral presentations and is organized by principle, domain, and topic rather than by conference or date.

**Live site:** [mlsys26.hinsu.org](https://mlsys26.hinsu.org) *(coming soon)*

## What's here

Each paper gets:
- Structured metadata: domain, topics, principles, hardware, organizations, key results
- A one-paragraph problem statement
- A summary with key contributions, trade-offs, and nuances
- Cross-links to papers sharing the same principle or topic

Papers are browsable by:
- **Principle** — cross-cutting optimization ideas (e.g., "fusion reduces memory bandwidth", "kernel performance is verifiable by LLMs")
- **Domain** — LLM serving, LLM training, agentic inference, recommendation models, ML compilers, fleet efficiency
- **Topic** — KV cache, speculative decoding, FSDP, quantization, kernel fusion, etc.

## Current coverage

| Conference | Papers indexed |
|-----------|---------------|
| MLSys 2026 | 135 |

## Quick start

```bash
git clone https://github.com/smit-hinsu/ml-systems-papers
cd ml-systems-papers
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Build the site
python scripts/generate_html.py
open site/index.html

# Validate papers
python scripts/validate.py

# Add a new paper
python scripts/new_paper.py \
  --url "https://mlsys.org/virtual/2026/oral/XXXX" \
  --title "Paper Title" \
  --by your-github-username
```

## Repository structure

```
data/
  papers/           # one .md file per paper (YAML frontmatter + Markdown body)
  principles.yaml   # canonical principle registry
  domains.yaml      # domain taxonomy
  topics.yaml       # topic tags
  venues.yaml       # conference/venue registry
  site.yaml         # site-wide config (name, GitHub handle)
scripts/
  generate_html.py  # builds site/ from data/
  validate.py       # checks schema and registry references
  new_paper.py      # creates a paper template from a URL
  fetch_metadata.py # pulls citation counts from Semantic Scholar
  fetch_mlsys_slides.py  # scrapes MLSys virtual for slides + OpenReview links
templates/          # Jinja2 HTML templates
site/               # generated output (gitignored)
schema.md           # full field documentation
CONTRIBUTING.md     # how to add papers
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The fastest way to help: pick any unindexed paper and open a PR with a new file in `data/papers/`.

## Adding a new conference

The pipeline is venue-agnostic. To index papers from another conference:
1. Add the venue to `data/venues.yaml`
2. Run `python scripts/new_paper.py` for each paper, referencing the new venue slug
3. Add domain/principle/topic entries to the registries as needed
