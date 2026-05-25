# Contributing to MLSys 26 Paper Index

This project is a community-maintained, semi-structured index of papers from [MLSys 2026](https://mlsys.org/virtual/2026). The goal is to make papers discoverable by observation, domain, and topic — not just by title.

## Ways to contribute

- **Add a new paper** — index a paper you read that's not yet in the list
- **Enrich an existing paper** — fill in missing fields (arxiv URL, organizations, citations, hardware)
- **Add your personal notes** — contribute to the `## Personal Notes` section
- **Improve summaries** — better problem statement, key results, or method description
- **Add new observations/domains/topics** — extend the registries if existing tags don't fit

## Workflow

1. Fork the repository
2. For a new paper:
   ```bash
   python scripts/new_paper.py \
     --url "https://mlsys.org/virtual/2026/oral/XXXX" \
     --title "Paper Title" \
     --by your-github-username
   ```
3. Edit the generated `data/papers/<slug>.md` file
4. Run validation: `python scripts/validate.py`
5. Optionally preview the site: `python scripts/generate_html.py && open site/index.html`
6. Open a pull request

## Requirements

```bash
python3 -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Quality bar for a paper submission

A paper file is mergeable when it has:
- [ ] All required fields filled (see `schema.md`)
- [ ] At least one `domain` tag
- [ ] A non-empty `problem` field (one sentence)
- [ ] A non-empty `## Summary` section (at least one paragraph)
- [ ] `validate.py` passes with no errors

Optional but appreciated:
- `key_results` with specific numbers
- `observations` cross-references
- `arxiv_url` and/or `code_url`

## Registries

Before adding new slugs, check `data/observations.yaml`, `data/domains.yaml`, and `data/topics.yaml`. Add a new entry to the registry *before* referencing it in a paper file. Registry entries require `label` and `description`.

## Non-indexed papers

Every paper from MLSys 2026 that is not yet indexed appears in the project as a GitHub Issue with the label `needs-indexing`. This is generated automatically. If you'd like to index a specific paper, comment on its issue.

## Code of conduct

Be accurate. If you're not sure about a technical claim, mark it with a `?` or omit it. The goal is to be useful, not to be comprehensive at the cost of correctness.
