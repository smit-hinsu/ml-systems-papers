# Paper Schema Reference

Each paper is a single Markdown file at `data/papers/<slug>.md` with YAML frontmatter and a Markdown body.

## Frontmatter Fields

### Identity

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `title` | string | ✅ | Full paper title |
| `slug` | string | ✅ | URL-safe identifier; must match filename |
| `authors` | list[string] | ✅ | Full author names in order |
| `organizations` | list[string] | — | Author affiliations |

### Links

| Field | Type | Notes |
|-------|------|-------|
| `mlsys_url` | string | ✅ Required. `https://mlsys.org/virtual/2026/oral/<id>` (login required for PDF/slides) |
| `openreview_url` | string | Primary paper link: `https://openreview.net/forum?id=XXXXX` — find by searching openreview.net |
| `arxiv_url` | string | Preprint URL if the authors posted one separately on arXiv |
| `slides_url` | string | Slides PDF or link — author-provided (MLSys virtual requires login) |
| `code_url` | string | GitHub or other code repository |
| `project_url` | string | Project/demo page |

### MLSys Metadata

| Field | Type | Values |
|-------|------|--------|
| `mlsys_official_category` | string | Official MLSys track name |
| `presentation_type` | enum | `oral` · `poster` · `spotlight` |
| `award` | string | `best-paper`, `outstanding`, or empty |
| `date` | string | ISO date `YYYY-MM-DD` of presentation |

### User Taxonomy

All values are **slugs** referencing the canonical registries in `data/`.

| Field | Type | Registry |
|-------|------|----------|
| `domain` | list[slug] | `data/domains.yaml` |
| `techniques` | list[slug] | `data/techniques.yaml` |
| `insights` | list[slug] | `data/insights.yaml` |

To add a new domain/technique/insight, **first add it to the registry**, then reference it in papers.

### Evaluation

| Field | Type | Notes |
|-------|------|-------|
| `hardware` | list[string] | e.g. `[H100, A100, TPU-v5]` |
| `models_evaluated` | list[string] | Open-source models used in evaluation |
| `agentic_models` | list[string] | For agentic workloads: `[gemini, claude, gpt-4o]` |

### Impact

| Field | Type | Notes |
|-------|------|-------|
| `citations` | int or null | Citation count at index time |
| `citations_updated` | string | ISO date of last citation count update |
| `research_or_industry` | enum | `research` · `industry` · `mixed` |

### Quick-Scan Fields

| Field | Type | Notes |
|-------|------|-------|
| `problem` | string | ✅ One sentence: what specific problem does this solve? |
| `key_results` | string | Headline quantitative results, concise |

### Reading / Indexing

| Field | Type | Values |
|-------|------|--------|
| `reading_status` | enum | `want-to-read` · `reading` · `read` · `understood` |
| `indexed_by` | string | ✅ GitHub username of indexer |
| `indexed_date` | string | ISO date `YYYY-MM-DD` |

## Body Structure

The Markdown body uses these headings (add/omit as needed):

```markdown
## Summary
1-2 paragraphs: what the paper does and why it matters.

## Key Contributions
Bulleted list of main contributions.

## Method
How it works.

## Results
Key numbers.

## Limitations
Acknowledged weaknesses.

## Personal Notes
Your own annotations (not rendered differently — just a convention).
```

## Adding a New Paper

```bash
python scripts/new_paper.py \
  --url "https://mlsys.org/virtual/2026/oral/XXXX" \
  --title "Paper Title" \
  --by your-github-username
```

Then edit the generated file, run `python scripts/validate.py`, and submit a PR.

## Adding a New Insight / Domain / Technique

Edit the appropriate registry file in `data/`. Required fields:
- `label`: human-readable name
- `description`: 1-2 sentence explanation
- `category` (insights and techniques only)

Then reference the new slug in your paper files.
