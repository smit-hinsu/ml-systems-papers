# Assigning Principles — the method

Written after the 2026-08 audit found **52% of principle assignments wrong** (133 of 257).
This guide exists so that failure is not repeated. Read it before tagging any paper.

The single most important rule: **go from the paper to the principle, never from the
principle to the paper.** Every large error in this corpus came from starting with a
principle and asking "does this paper fit?" — the answer is almost always yes if you squint.

---

## Part 1 — What went wrong, and what each cause implies

Seven causes, from the audit. Each one has a countermeasure baked into the procedure below.

### 1. Slug names collide with terms of art
`cache`, `fuse`, `tier`, `pipeline`, `batch` are ordinary nouns in ML systems — KV cache,
kernel fusion, memory tier, pipeline parallelism, token batching. The tagger matched the
**word in the paper**, not the idea. GhostServe was tagged `cache` because the thing it
protects is a KV cache.

> **Countermeasure:** state the mechanism in your own words, without the paper's vocabulary,
> before you name a principle. Step 2 below.

### 2. Tag chosen first, observation written to justify it
This is why "the observation describes something else" is such a reliable detector — ProToken's
`cache` observation is about gradient filtering. Had the observation come first, the tag could
not have drifted.

> **Countermeasure:** write the observation first, derive the tag from it. Step 3.

### 3. The prompt said what each principle IS, never what it ISN'T
Seventeen one-line definitions with no exclusions. Every principle now carries a `not:` clause
in `data/principles.yaml`.

> **Countermeasure:** read the `not:` clause for every candidate. Step 4.

### 4. Missing principles forced substitution
Fault tolerance, provenance and privacy have no axis, so those papers took the nearest
available tag. This is structural, not carelessness.

> **Countermeasure:** zero principles is a valid, expected answer. Step 6.

### 5. An apparent two-tag quota
77 of 135 papers had exactly two principles. Judgment does not cluster that tightly.

> **Countermeasure:** no target count. One is normal. Zero is normal.

### 6. Nothing could catch it
`validate.py` checks that slugs exist and fit char limits. It cannot check truth.

> **Countermeasure:** the check is human, and it is this document.

### 7. The first critic pass was undersized
It fixed ~15 papers and declared the problem solved. The real number was 133.

> **Countermeasure:** audit exhaustively or state plainly that you spot-checked.

---

## Part 2 — The procedure

Work through this per paper, in order. Do not skip to step 4.

### Step 1 — Read for the contribution, not the vocabulary
Read `problem`, `key_results`, `## Key Contributions`. Answer: **what would this paper still
be if you deleted this mechanism?** If the paper survives intact, the mechanism is a *means*,
not a contribution.

- ProTrain tunes recomputation — but the contribution is the cost-model planner. Not `recompute`.
- PIKE's agents discover fusions — but the contribution is the explore/exploit framework. Not `fuse`.
- BLASST runs inside FlashAttention's fused loop — inherited, not contributed. Not `fuse`.

### Step 2 — Say the mechanism out loud, in your own words
Without using the paper's nouns. "Something is stored and reused when the same input recurs."
"Two independent things run at once so one hides the other's latency." "Operations are merged
so a memory round-trip disappears."

**If you cannot say it without repeating the paper's vocabulary, you do not understand it yet —
and any tag you pick will be a word match.**

### Step 3 — Write the observation before choosing the tag
One sentence, max 200 chars, stating the **motivating problem insight**: what this paper
noticed that made some principle applicable. Not the solution.

- ✅ "agent B idles waiting for A to finish despite having spare GPU capacity"
- ❌ "we overlap prefill and decode"

Then read your own sentence and ask which principle it describes. That is the tag. If the
sentence describes routing, it is not `cache`, no matter what the paper calls its data structure.

### Step 4 — Check the `not:` clause
Open `data/principles.yaml` and read the `not:` field for every candidate. It names the
near-misses that actually occurred in this corpus. If your paper matches the `not:` clause,
the answer is no — however good the fit felt.

### Step 5 — Check the neglected principles before the popular ones
`cache`, `fuse`, `tier`, `skip` and `pipeline` absorbed papers belonging to others. Before
using any of those five, rule these out:

| If the paper… | it is |
|---|---|
| changes output quality at all — lossy skipping, early exit, generative reconstruction, a surrogate replacing an exact evaluator | `approximate`, not `skip` |
| allocates bit-width, even non-uniformly by sensitivity | `quantize`, not `skip`/`tier` |
| amortizes a fixed per-call cost across grouped work | `batch`, not `tier`/`fuse` |
| preserves optionality across vendors or backends | `portable`, not `fuse` |
| separates structurally different sub-tasks so each is optimized apart | `specialize`, not `pipeline` |
| reclaims capacity idled by the primary workload | `elastic`, not `balance` |
| trades compute for storage as the point | `recompute`, not `tier` |
| builds a profiler, benchmark, simulator, or decomposing metric | `measure` |

### Step 6 — Decide the count honestly
No quota. Assign only what survives steps 1–5.

**Zero is a legitimate answer.** 42 papers currently have none. Fault tolerance, provenance,
privacy partitioning, and pure engineering contributions have no home yet — leave them empty
and note the gap. An empty list is information; a wrong tag is damage.

If you reach five or more, you are almost certainly over-tagging.

### Step 7 — Park what you are unsure about
Genuinely arguable calls — usually "means vs. contribution" — go in `principles_review`
instead of `principles`. Kept in the data, never published, visible under `--dev`. Use it
rather than guessing in either direction.

---

## Part 3 — The seven verified mistakes

Real cases from this corpus. Each looked reasonable when it was made.

| Paper | Wrong tag | The observation as written | Why wrong | Belongs |
|---|---|---|---|---|
| GhostServe | `cache` | "Erasure-coded KV cache parity shards… enable fast recovery after device failure" | Redundancy for durability. Nothing memoized. Tagged on the word "cache". | none — fault tolerance has no axis |
| FaaScale | `fuse` | "Multicast transfers a single copy of model blocks to multiple nodes… reducing total bytes transferred" | Fewer bytes on a wire ≠ removing a memory round-trip. | none |
| BatchLLM | `tier` | "Memory-centric token batching enlarges token batch sizes to increase GPU utilization" | Amortizing per-call cost. No hierarchy, no eviction. | `batch` |
| Attribution-based Sparse Activation | `skip` | "70% neuron deactivation with <5% accuracy loss" | Quality changes, so not provably unnecessary. | `approximate` |
| Hawkeye | `search-ai` | "Systematic tests of rounding direction, subnormal handling, accumulation order" | No AI, no candidate search. Differential testing. | `measure` |
| ProToken | `cache` | "Gradient-based relevance weighting filters irrelevant neuron activations" | Filtering. Nothing stored or reused. | `skip`-adjacent |
| MixLLM | `skip` | "Global cross-layer sensitivity analysis identifies the small fraction of output features needing higher bit-width" | Bit allocation is quantization. | `quantize` |

**All seven share one shape: the tag matched a word, not an idea.**

---

## Part 4 — Reviewing someone else's assignment

Fastest reliable check, in order:

1. **Read the observation, ignore the tag.** Name the principle it describes. Mismatch is the
   single most common defect and takes seconds to spot.
2. **Apply the deletion test.** Remove the mechanism — does the paper survive? Then it is a means.
3. **Read the `not:` clause.** Most bad tags are explicitly excluded by it.
4. **Check for an over-used tag masking a neglected one.** `skip` where quality drops is
   `approximate`; `tier` where a fixed cost is amortized is `batch`.
5. **Count.** Four or more, or exactly two on many papers in a row, signals quota-filling.
