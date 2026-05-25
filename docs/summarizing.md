# How to Write a Good Paper Entry

This guide defines the quality bar for summaries in this index. The target audience is **ML systems engineers and researchers** — people who build or evaluate production infrastructure. A good entry gives them enough to decide whether to read the paper and roughly how the approach works, without making them open the PDF first.

## The core principle

Every claim must be specific enough to be useful. If you could substitute the sentence into a different paper without noticing, it's not specific enough.

**Bad:** "uses an LLM agent to optimize kernel performance"  
**Good:** "applies an OpenEvolve-style evolutionary loop: GPT-4o proposes kernel mutations, a correctness verifier filters invalid variants, and tournament selection keeps the top candidates over N rounds"

**Bad:** "achieves significant throughput improvement"  
**Good:** "2.1× end-to-end throughput on A100 80GB at batch size 32 vs. vLLM baseline with continuous batching"

If the paper names a specific system, algorithm, or prior work — include it. If a result has hardware, model size, and metric — include all three.

## The workflow

1. **Read the paper yourself.** There is no shortcut here. Take rough notes on what surprised you or what you'd want to tell a colleague.

2. **Run the summarization prompt** (see `prompts/paper_summary.md`) with the paper text and your notes. This produces a draft `.md` file.

3. **Review every field.** The prompt is a starting point. Correct anything vague, wrong, or missing. Your notes from step 1 are the ground truth — if the prompt missed OpenEvolve, add it.

4. **Check the quality bar** (below) before marking the paper as indexed.

5. **Iterate on the prompt.** When you correct something the prompt got wrong, consider whether a rule or example could prevent that class of error. Edit `prompts/paper_summary.md` accordingly.

## Quality bar per field

### `problem`
One sentence. Should read like something a practitioner would say about their own system — a concrete pain point, not an abstract research gap.

- ❌ "existing approaches have performance limitations"
- ✅ "GPU kernels hand-written in CUDA take weeks to tune per model architecture and don't transfer across hardware generations"

### `key_results`
The single most important result. Hardware + model/workload + metric + baseline, all in one sentence. Numbers required.

- ❌ "outperforms baselines"
- ✅ "37% higher token throughput than vLLM on Llama-3-70B at batch 64 on H100, with <1% accuracy degradation"

### `observations`
These are the core observations that motivated the design — what the authors noticed that others hadn't fully exploited. Write them as claims a skeptic could challenge.

- ❌ "efficient memory management improves performance"
- ✅ "KV cache fragmentation accounts for 30–40% of wasted GPU memory in production serving, because vLLM pre-allocates contiguous blocks per request"

### `## Problem`
2–3 sentences expanding on the frontmatter `problem` field. Why does this matter at scale?
What breaks in practice? Each sentence should add new information — not restate the
frontmatter or preview the results.

### `## Key Contributions`
3–5 bullets. Each = a concrete artifact (named algorithm, data structure, protocol) with
a one-line mechanism. Never repeat a result here; never repeat the problem statement.
If you find yourself copying a sentence from another section, cut it — it belongs in one
place only.

### `## Results`
2–5 bullets. Format: metric + number + hardware + model + baseline. If any of these are
unknown, say so explicitly rather than omitting them.

### `## Trade-offs`
Short bullets on what the approach gives up. Omit if the paper makes no meaningful
trade-offs.

### `## Nuances`
Gotchas, subtle assumptions, conditions that break the approach, and limitations.
Practitioners-only content — no academic hedging.

## Conciseness: one section, one job

Each section has exactly one job. Repetition across sections is the most common quality
failure — it makes entries longer without adding information.

**The test:** If you can delete a sentence from one section because it already appears
(or is implied) in another, cut it. Every sentence should be unique to its section.

| Section | Its one job | What does NOT belong here |
|---|---|---|
| `## Problem` | Why this matters in practice | Results, mechanism, related work |
| `## Key Contributions` | Name the artifacts + mechanism | Results, restatement of problem |
| `## Results` | Numbers with hardware/model/baseline | Mechanism explanation, speculation |
| `## Trade-offs` | What is given up | Limitations that aren't trade-offs |
| `## Nuances` | What bites practitioners | Already-stated trade-offs |

**Common failure modes:**
- ## Key Contributions lists "40% speedup" — that's a result, not a contribution
- ## Problem ends with "which motivates our approach" — cut the last clause
- ## Key Contributions last bullet summarizes all previous bullets — cut it
- ## Results mentions how a mechanism works — belongs in ## Key Contributions

## Anti-patterns to avoid

| Vague | Specific |
|---|---|
| "uses a novel scheduling algorithm" | "preempts requests using SRPT scheduling based on predicted remaining decode steps, estimated via a small proxy model" |
| "leverages modern GPU architecture" | "exploits H100 TMA (Tensor Memory Accelerator) to overlap data movement with compute in the attention kernel" |
| "scales to large models" | "tested on Llama-3-70B and Mixtral 8×22B, single-node 8×H100" |
| "significantly reduces memory" | "reduces peak KV cache memory by 3.2× via 4-bit quantization of keys and 8-bit of values" |
| "inspired by prior work" | "extends PagedAttention (vLLM) with copy-on-write semantics for beam search" |

### Never open with what everyone already knows

Cut every sentence that states an obvious industry fact as if it were news. The reader is a systems engineer — they know LLMs are large, that inference is expensive, and that training is hard.

**Cut without replacement:**
- "The proliferation of large language models (LLMs) demands inference systems with both low latency and high efficiency at scale."
- "Training frontier-scale foundation models involves coordinating thousands of GPUs."
- "Large language models have become increasingly important in recent years."
- "Efficient inference is critical for production deployment of LLMs."
- Any sentence whose second half would be "...which motivates our work."

**Instead, open the summary with the specific gap or observation:**
- ❌ "LLMs require fast inference. GPU HBM is a bottleneck. We propose SHIP..."
- ✅ "HBM bandwidth during decode is the binding constraint for KV cache access at large batch sizes. SHIP replaces HBM with on-chip SRAM for the KV cache by..."

The abstract scraped from the conference site is a starting point for finding the key claim — not text to paraphrase or include verbatim. Discard the setup sentences; keep only the specific claim.

### Don't copy-paste the abstract

The abstract is written for a different audience (reviewers) and a different format (200 words with formal framing). A summary for this index should:
- Use active voice and concrete nouns
- Skip the related-work framing
- Lead with the system name and what it does, not with the problem statement

## Prompt iteration log

Track prompt changes here so we know what was fixed and why.

| Date | Change | Triggered by |
|---|---|---|
| (initial) | Created `prompts/paper_summary.md` | — |
