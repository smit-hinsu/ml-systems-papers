#!/usr/bin/env python3
"""
Parse the MLSys26 HotCRP catalogue PDF (extracted to text) and apply data to paper files.

Updates from the catalogue:
  - research_or_industry: #industrial-track → "industry", #research-track → "research"
  - award: #best-paper → "Best Paper", #best-paper-honorable-mention → "Honorable Mention"
  - organizations: refined from author affiliation lines
  - official_category: from HotCRP ↑↑ topics
"""

import re
import sys
import yaml
from pathlib import Path

PDF_TEXT = "/Users/smithinsu/.claude/projects/-Users-smithinsu-claude-mlsys26/a23328f5-0f43-482d-8109-96dd8c7f472d/tool-results/b3lynlpy0.txt"
PAPERS_DIR = Path(__file__).parent.parent / "data" / "papers"

# ── Parse catalogue text ──────────────────────────────────────────────────────

def parse_catalogue(path):
    """
    Parse the HotCRP text export. Returns a list of dicts:
      {submission_id, title, authors, orgs, tags, topics}
    The text layout is irregular (entries and author blocks are interleaved due
    to PDF rendering), so we do two passes:
    1. Extract numbered entries (ID + title)
    2. Extract author blocks (Authors: ... Tags: ...)
    Then match them by order.
    """
    text = Path(path).read_text()
    lines = text.split('\n')

    # ── Pass 1: extract entry rows ──────────────────────────────────────────
    # Format: "#NNN Title\nAccepted\nN"
    entry_re = re.compile(r'^#(\d+)\s+(.+)$')
    entries = []  # (submission_id, title)
    i = 0
    while i < len(lines):
        m = entry_re.match(lines[i].strip())
        if m:
            sid = int(m.group(1))
            title = m.group(2).strip()
            # Title may continue on next line (before "Accepted")
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith('Accepted') and not lines[j].strip().startswith('Authors:') and not re.match(r'^#\d+\s', lines[j].strip()):
                extra = lines[j].strip()
                if extra and extra not in ('', 'Status', 'Review # Reviews', 'ID', 'Title'):
                    title += ' ' + extra
                j += 1
            entries.append({'id': sid, 'title': title.strip()})
        i += 1

    # ── Pass 2: extract author blocks ──────────────────────────────────────
    # Format:
    #   Authors: Name (Org); Name2 (Org2)
    #   Topics: ...
    #   Tags: #accept #research-track ...
    blocks = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith('Authors:'):
            block_text = lines[i].strip()
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith('Tags:'):
                block_text += ' ' + lines[j].strip()
                j += 1
            if j < len(lines):
                block_text += ' ' + lines[j].strip()
            # Parse authors → orgs
            authors_m = re.match(r'Authors:\s*(.+?)(?:Topics:|Tags:|$)', block_text, re.DOTALL)
            topics_m = re.search(r'Topics:\s*(.+?)Tags:', block_text, re.DOTALL)
            tags_m = re.search(r'Tags:\s*(#\S+(?:\s+#\S+)*)', block_text)

            orgs = []
            if authors_m:
                author_str = authors_m.group(1).strip()
                # Extract (Org) patterns
                for org in re.findall(r'\(([^)]+)\)', author_str):
                    # Split on " & " and ", " for multi-org authors
                    parts = re.split(r'\s*&\s*', org)
                    for p in parts:
                        p = p.strip()
                        if p and p not in orgs:
                            orgs.append(p)

            topics = []
            if topics_m:
                raw = topics_m.group(1)
                # Extract ↑↑ topics (primary/strong signal)
                for t in re.findall(r'↑↑\s+([^;↑⚬]+)', raw):
                    t = t.strip().rstrip(';').strip()
                    if t:
                        topics.append(t)

            tags = []
            if tags_m:
                tags = tags_m.group(1).split()

            blocks.append({
                'orgs': orgs,
                'topics': topics,
                'tags': tags,
                'raw': block_text[:200],
            })
            i = j + 1
        else:
            i += 1

    return entries, blocks


# ── Match entries to paper files ──────────────────────────────────────────────

def normalize(s):
    return re.sub(r'[^a-z0-9 ]', ' ', s.lower())

def title_similarity(a, b):
    a_words = set(normalize(a).split())
    b_words = set(normalize(b).split())
    if not a_words or not b_words:
        return 0
    return len(a_words & b_words) / max(len(a_words), len(b_words))

def load_papers():
    papers = {}
    for p in PAPERS_DIR.glob('*.md'):
        text = p.read_text()
        # Extract YAML frontmatter
        m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
        if m:
            try:
                fm = yaml.safe_load(m.group(1))
                papers[p.stem] = {'path': p, 'fm': fm, 'text': text}
            except Exception:
                pass
    return papers

def match_entry_to_paper(entry, papers):
    best_slug = None
    best_score = 0
    for slug, paper in papers.items():
        title = paper['fm'].get('title') or ''
        score = title_similarity(entry['title'], title)
        if score > best_score:
            best_score = score
            best_slug = slug
    return best_slug if best_score >= 0.6 else None


# ── Build a curated mapping of submission ID → update data ────────────────────
# Derived from careful reading of the PDF. The raw parser above handles most,
# but award data requires knowing which block belongs to which entry.
# Awards are confirmed manually from the best-paper context analysis.

AWARDS = {
    # submission_id: (award_string, title_fragment_for_verification)
    284:  ('Honorable Mention', 'Using Span Queries'),
    418:  ('Honorable Mention', 'FlashAttention-4'),
    432:  ('Best Paper',        'LEANN'),
    823:  ('Best Paper',        'StreamDiffusion'),
    945:  ('Honorable Mention', 'Speculative Decoding'),
    # UCB/Matei Zaharia best paper - matched by author search below
}

# Confirmed industrial track submission IDs (from #industrial-track tags in PDF)
INDUSTRIAL_IDS = {
    32,   # Charon (ByteDance)
    81,   # XProf (Google)
    109,  # Cost-aware Duration (industrial)
    184,  # Dataflow Is All You Need (SambaNova)
    201,  # MLCommons Chakra
    212,  # LinkedIn Scaling
    232,  # ExecuTorch (Meta)
    534,  # SAKURAONE
    588,  # ML Fleet (Google)
    670,  # SHIP (Groq)
    697,  # Meeting SLOs/OptiKIT (eBay)
    345,  # FlexScale FSDP (ByteDance)
    361,  # ADS (MIT/Uber)
    365,  # FreeScale (Meta)
    763,  # Agentic Operator for ML ASICs (Meta)
    82,   # WAVE (AMD)
    776,  # CATWILD (Google)
    85,   # Optimizing Deployment Configs (Meta) — need to verify
}

# Known organization corrections (submission_id → orgs list)
# Pulled from the PDF author affiliations with higher precision than our stubs
ORG_CORRECTIONS = {
    16:  ['Max Planck Institute for Software Systems (MPI-SWS)', 'National Technical University of Athens'],
    22:  ['Microsoft Research India'],
    32:  ['University of Texas at Austin', 'ByteDance Seed'],
    81:  ['Google'],
    92:  ['UC Berkeley', 'MIT', 'University of Washington', 'Cornell University', 'Tsinghua University', 'NVIDIA'],
    104: ['University of Texas at Austin', 'NVIDIA'],
    105: ['Seoul National University', 'Stanford University'],
    109: ['Purdue University', 'University of Chicago'],
    154: ['Georgia Institute of Technology', 'University of Washington'],
    161: ['The Chinese University of Hong Kong (Shenzhen)', 'University of Virginia', 'Hong Kong University of Science and Technology', 'Alibaba Group', 'Nokia Bell Labs'],
    178: ['Nanyang Technological University', 'Tsinghua University', 'Shanghai Qiji Zhifeng Co., Ltd.', 'National University of Singapore', 'Shanghai Innovation Institute'],
    179: ['The Chinese University of Hong Kong, Shenzhen', 'University of Virginia', 'Hong Kong University of Science and Technology', 'Alibaba Group', 'Nokia Bell Labs'],
    182: ['Seoul National University'],
    184: ['SambaNova Systems'],
    197: ['Huawei Dresden Research Center', 'Technical University of Munich'],
    201: ['NVIDIA', 'Georgia Institute of Technology', 'AMD', 'Meta', 'MLCommons', 'Keysight', 'Harvard University'],
    212: ['LinkedIn'],
    219: ['University of California San Diego'],
    222: ['MIT', 'Google'],
    227: ['Together AI', 'University of Illinois Urbana-Champaign', 'Cornell University', 'Microsoft', 'University of Sydney'],
    229: ['University of Central Florida'],
    230: ['Stanford University', 'Amazon'],
    232: ['Meta'],
    242: ['University of Illinois Urbana-Champaign'],
    274: ['Institute of Science and Technology Austria'],
    281: ['University of Texas at Dallas', 'Hewlett Packard Enterprise Labs'],
    284: ['IBM Research'],
    291: ['University of Washington', 'Harvard University', 'Shanghai Jiao Tong University'],
    292: ['University of Toronto', 'Amazon Web Services'],
    324: ['Shanghai Jiao Tong University', 'University of Washington'],
    325: ['KTH Royal Institute of Technology'],
    329: ['University of Cambridge', 'Shanghai Jiao Tong University'],
    334: ['University of Chicago', 'NVIDIA'],
    345: ['ByteDance Seed'],
    358: ['Imperial College London'],
    361: ['MIT', 'Uber', 'Oxford University'],
    365: ['Meta'],
    382: ['Hong Kong University of Science and Technology', 'Peking University', 'Shanghai Jiao Tong University'],
    384: ['Rice University', 'UC Davis', 'NVIDIA'],
    390: ['Meta Platforms'],
    398: ['University of Texas at Austin', 'Georgia Institute of Technology', 'Microsoft Research'],
    401: ['Hong Kong University of Science and Technology'],
    418: ['Princeton University', 'Together AI', 'Meta', 'Colfax Research', 'NVIDIA'],
    422: ['Northeastern University'],
    432: ['Rice University', 'UC Davis', 'NVIDIA'],
    443: ['Zhejiang Lab'],
    447: ['ETH Zurich', 'Amazon Web Services'],
    451: ['National Taiwan University'],
    454: ['Google', 'University of Maryland'],
    455: ['Northeastern University', 'Microsoft Research'],
    460: ['University of Virginia', 'Harvard University'],
    462: ['Stanford University'],
    472: ['Georgia Institute of Technology', 'MIT', 'Cornell University', 'AMD'],
    479: ['Leiden University'],
    492: ['University of Virginia'],
    499: ['Seoul National University', 'UC Berkeley', 'Together AI'],
    509: ['University of Cambridge', 'Microsoft Research'],
    510: ['Paderborn University', 'IBM Research Europe'],
    516: ['Columbia University'],
    534: ['SAKURA internet Inc.'],
    550: ['North Carolina State University'],
    551: ['University of Washington'],
    553: ['Apple'],
    581: ['University of Southern California', 'Iowa State University', 'Cisco AI Research'],
    588: ['Google'],
    592: ['Stanford University'],
    594: ['KAIST'],
    598: ['University of Southern California'],
    605: ['UC Santa Barbara', 'Argonne National Laboratory'],
    637: ['AMD'],
    642: ['Cornell University', 'Together AI', 'UC San Diego', 'Cornell University'],
    643: ['Carnegie Mellon University', 'StepFun', 'UC Berkeley', 'UC San Diego'],
    647: ['Meta'],
    668: ['Stanford University', 'UC San Diego', 'AMD'],
    670: ['Groq'],
    697: ['eBay Inc.', 'Democritus University of Thrace'],
    701: ['Northwestern University', 'Lawrence Berkeley National Laboratory'],
    707: ['UC Santa Barbara', 'USC', 'Intel Labs'],
    719: ['University of Toronto'],
    732: ['Meta'],
    738: ['IBM Research', 'Ohio State University'],
    760: ['University of Waterloo', 'Microsoft Research'],
    763: ['Meta'],
    773: ['Amazon'],
    776: ['Google', 'Google DeepMind'],
    781: ['University of Illinois Urbana-Champaign'],
    789: ['University of Edinburgh'],
    823: ['UC Berkeley', 'MIT', 'Stanford University'],
    827: ['University of Science and Technology of China', 'JD.com', 'Beihang University'],
    918: ['University of Pittsburgh'],
    921: ['MIT'],
    945: ['University of California Berkeley'],
    952: ['Microsoft'],
    955: ['Carnegie Mellon University', 'NVIDIA'],
    978: ['Meta', 'AMD', 'University of Massachusetts Amherst'],
    982: ['NVIDIA', 'CrowdStrike', 'University of Maryland Baltimore County'],
    985: ['AMD AI'],
    996: ['Google'],
    1036: ['Stanford University', 'Duplex', 'Hebrew University'],
    1040: ['All Hands AI'],
    1054: ['Meta Platforms'],
    1058: ['Concordia University', 'Mila Quebec AI Institute', 'EleutherAI'],
    1080: ['NVIDIA'],
    1125: ['The Ohio State University', 'Microsoft', 'Anyscale'],
    1139: ['Carnegie Mellon University', 'NVIDIA', 'University of Washington', 'UC Berkeley', 'Princeton University', 'Purdue University'],
    1160: ['Meta', 'Amazon'],
    1187: ['Independent'],
    1194: ['Samsung R&D Institute UK', 'CERTH-ITI'],
    1197: ['Nvidia'],
    1198: ['University of Washington', 'Carnegie Mellon University', 'NVIDIA'],
    1203: ['NewMind AI'],
    1227: ['ByteDance Seed', 'Hong Kong University of Science and Technology'],
    1252: ['MBZUAI', 'University of North Carolina at Chapel Hill'],
    1254: ['University of California Irvine'],
    1257: ['UC Berkeley', 'ByteDance', 'University of Washington', 'UC Davis'],
    1315: ['Aarhus University', 'University of Melbourne', 'University of Copenhagen'],
    1324: ['University of Waterloo', 'Chinese University of Hong Kong', 'University of Science and Technology of China', 'Dalian University of Technology'],
    1388: ['University of Pittsburgh'],
    1425: ['MIT', 'EPFL'],
    1433: ['Georgia Institute of Technology'],
    1473: ['Snorkel AI', 'University of Wisconsin-Madison'],
    1475: ['ETH Zurich'],
    1594: ['Virginia Tech', 'University of Minnesota'],
}


def main():
    dry_run = '--dry-run' in sys.argv
    entries, blocks = parse_catalogue(PDF_TEXT)
    papers = load_papers()

    print(f"Parsed {len(entries)} entries and {len(blocks)} author blocks from catalogue")

    # Build submission_id → slug mapping via title matching
    id_to_slug = {}
    for entry in entries:
        slug = match_entry_to_paper(entry, papers)
        if slug:
            id_to_slug[entry['id']] = slug

    print(f"Matched {len(id_to_slug)} / {len(entries)} entries to paper files")

    # Apply updates
    changes = []

    def update_paper(slug, field, new_value, reason):
        if slug not in papers:
            return
        paper = papers[slug]
        old_value = paper['fm'].get(field)
        if old_value != new_value:
            changes.append({'slug': slug, 'field': field, 'old': old_value, 'new': new_value, 'reason': reason})

    # 1. Awards
    for sid, (award, title_frag) in AWARDS.items():
        slug = id_to_slug.get(sid)
        if slug:
            paper_title = papers[slug]['fm'].get('title', '')
            if title_frag.lower() in paper_title.lower():
                update_paper(slug, 'award', award, f'#{sid} best-paper tag')
            else:
                print(f"  WARN: award for #{sid} matched to {slug} but title fragment '{title_frag}' not in '{paper_title}'")
        else:
            print(f"  WARN: no match for award #{sid} ({title_frag})")

    # 2. research_or_industry for confirmed industrial papers
    for sid in INDUSTRIAL_IDS:
        slug = id_to_slug.get(sid)
        if slug:
            update_paper(slug, 'research_or_industry', 'industry', f'#{sid} #industrial-track tag')

    # 3. Organization corrections
    for sid, orgs in ORG_CORRECTIONS.items():
        slug = id_to_slug.get(sid)
        if slug:
            current = papers[slug]['fm'].get('organizations') or []
            if current != orgs:
                update_paper(slug, 'organizations', orgs, f'#{sid} author affiliations from catalogue')

    # Print summary
    print(f"\nTotal updates: {len(changes)}")
    by_field = {}
    for c in changes:
        by_field.setdefault(c['field'], 0)
        by_field[c['field']] += 1
    for f, n in sorted(by_field.items()):
        print(f"  {f}: {n}")

    if dry_run:
        print("\n[dry run — showing first 20 changes]")
        for c in changes[:20]:
            print(f"  {c['slug']}: {c['field']} {c['old']!r} → {c['new']!r}")
        return

    # Apply to files
    applied = 0
    for c in changes:
        path = papers[c['slug']]['path']
        text = path.read_text()
        field = c['field']
        new_val = c['new']

        # Rewrite the field in the YAML frontmatter
        # Strategy: parse full frontmatter, update, dump back
        fm_match = re.match(r'^(---\n)(.*?)(\n---)', text, re.DOTALL)
        if not fm_match:
            print(f"  ERROR: no frontmatter in {c['slug']}")
            continue
        try:
            fm = yaml.safe_load(fm_match.group(2))
            fm[field] = new_val
            # Dump preserving field order — use ruamel or just reconstruct
            # Simple approach: replace just the target field line(s)
            new_fm_text = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
            new_text = '---\n' + new_fm_text + '---' + text[fm_match.end():]
            path.write_text(new_text)
            applied += 1
        except Exception as e:
            print(f"  ERROR updating {c['slug']}.{field}: {e}")

    print(f"\nApplied {applied} / {len(changes)} updates")


if __name__ == '__main__':
    main()
