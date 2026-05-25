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

### `## Summary` section
3–6 paragraphs. Cover:
1. What problem and why it matters (with concrete scale or cost numbers if available)
2. The key observation(s) that motivated the approach
3. How the system actually works — name every component, data structure, and algorithm
4. What was evaluated, on what hardware, against what baselines
5. Limitations or when this approach doesn't apply

### `## Key Contributions`
3–5 bullet points. Each should be a concrete artifact: a new algorithm, a data structure, a measurement, a system. Not "we show that X is possible."

## Anti-patterns to avoid

| Vague | Specific |
|---|---|
| "uses a novel scheduling algorithm" | "preempts requests using SRPT scheduling based on predicted remaining decode steps, estimated via a small proxy model" |
| "leverages modern GPU architecture" | "exploits H100 TMA (Tensor Memory Accelerator) to overlap data movement with compute in the attention kernel" |
| "scales to large models" | "tested on Llama-3-70B and Mixtral 8×22B, single-node 8×H100" |
| "significantly reduces memory" | "reduces peak KV cache memory by 3.2× via 4-bit quantization of keys and 8-bit of values" |
| "inspired by prior work" | "extends PagedAttention (vLLM) with copy-on-write semantics for beam search" |

## Prompt iteration log

Track prompt changes here so we know what was fixed and why.

| Date | Change | Triggered by |
|---|---|---|
| (initial) | Created `prompts/paper_summary.md` | — |
