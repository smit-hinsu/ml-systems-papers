# Discussion: FlashAgents

Internal Q&A — not rendered on site.

---

## 2026-05-24

**Q:** Does the efficiency win hold beyond two-agent linear pipelines?

**A:** Only linear A→B chains are evaluated in the paper. DAG or fan-out topologies (e.g. one orchestrator agent broadcasting to N parallel subagents) are not characterized. The incremental prefill mechanism as designed handles a single upstream source; handling multiple concurrent upstream token streams would require protocol changes. The radix-tree prefix cache component would generalize naturally to fan-out since the shared prefix is still identifiable.

---

**Q:** What hardware and models were used in evaluation?

**A:** Not captured yet — the abstract doesn't specify. Needs extraction from the full paper at https://openreview.net/forum?id=m14PPUfgEc

---
