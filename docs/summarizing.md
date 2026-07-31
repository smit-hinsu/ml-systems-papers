# How to Write a Good Paper Entry

This guide defines the quality bar for summaries in this index. The target audience is **ML systems engineers and researchers** — people who build or evaluate production infrastructure. A good entry gives them enough to decide whether to read the paper and roughly how the approach works, without making them open the PDF first.

## The core principle

Every claim must be specific enough to be useful. If you could substitute the sentence into a different paper without noticing, it's not specific enough.

**Bad:** "uses an LLM agent to optimize kernel performance"  
**Good:** "applies an OpenEvolve-style evolutionary loop: GPT-4o proposes kernel mutations, a correctness verifier filters invalid variants, and tournament selection keeps the top candidates over N rounds"

**Bad:** "achieves significant throughput improvement"  
**Good:** "2.1× end-to-end throughput on A100 80GB at batch size 32 vs. vLLM baseline with continuous batching"

If the paper names a specific system, algorithm, or prior work — include it. If a result has hardware, model size, and metric — include all three.

## The writing rules

Every entry follows Orwell's six rules from *Politics and the English Language*. They are
the house style, and they sit underneath every field-specific rule below.

1. **Never use a metaphor, simile, or figure of speech you are used to seeing in print.**
   Dead metaphors are the tell of writing that was assembled rather than thought through:
   *unlocks, paves the way, sheds light on, at the heart of, game-changing, seamlessly,
   leverages, harnesses the power of.* Say what the thing does.
2. **Never use a long word where a short one will do.** *utilize* → use. *methodology* →
   method. *facilitates* → lets. *in order to* → to. *demonstrates that* → shows.
3. **If it is possible to cut a word out, cut it.** *in the context of, it is worth noting
   that, a variety of, in terms of, the fact that* — all deletable without loss. Character
   limits on `problem`, `key_results`, and `observations` exist to force this.
4. **Never use the passive where you can use the active.** "The KV cache is recomputed by
   the scheduler" → "the scheduler recomputes the KV cache." Passive voice hides who acts,
   which is exactly the information a systems reader wants.
5. **Never use a jargon word where an everyday word will do.** This targets *needless*
   jargon, not domain vocabulary. Terms of art — KV cache, prefill, all-reduce, HBM — are
   precise and required; rule 5 never overrides the specificity requirement above. It
   forbids the vague-academic register: *paradigm, holistic, novel framework, orthogonal
   to, non-trivial.*
6. **Break any of these rules sooner than say anything outright barbarous.** If following
   a rule makes a sentence wrong, misleading, or unreadable, the rule loses.

Rules 1 and 5 do most of the work here, because model-generated prose defaults to exactly
the register they forbid.

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

### `## Key Contributions`
3–5 bullets. Each = a concrete artifact (named algorithm, data structure, protocol) with
a one-line mechanism. The problem context and key numbers are implicit here — don't add
separate Problem or Key Contributions sections. Include hardware + model + metric + baseline inline
on the bullet that is the primary result.
If you find yourself copying a sentence from another section, cut it — it belongs in one
place only.

### `## Findings`
*Only for measurement, characterization, or survey papers.* Bullet-point list of concrete
findings — what was measured or characterized, not what the system achieves. Each bullet
should be specific and quantitative where possible.

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
| `## Key Contributions` | Name the artifacts + mechanism (+ implicit problem + key numbers) | Generic claims, separate results section |
| `## Findings` | Concrete measured/characterized facts (measurement papers only) | System design, trade-off discussion |
| `## Trade-offs` | What is given up | Limitations that aren't trade-offs |
| `## Nuances` | What bites practitioners | Already-stated trade-offs |

**Common failure modes:**
- ## Key Contributions omits the key number — bake it into the contribution bullet inline
- ## Key Contributions last bullet summarizes all previous bullets — cut it
- ## Findings describes what the system does instead of what was measured — wrong section

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
