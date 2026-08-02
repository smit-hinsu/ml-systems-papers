# Taxonomy Audit — 2026-08-02

A full pass over all 135 papers against all 17 principles, run as seven parallel read-only
review agents. Each agent judged every applied principle CORRECT or MISAPPLIED against one
test, and separately reported paper insights that no principle covers.

**The test:** could a colleague read this paper and say "yes, a core contribution of this
paper is `<principle>`"? Using the idea as a *means* inside the method does not count. A tag
also fails if its `observations.<slug>` text describes something other than the principle it
is filed under.

## Headline

| | |
|---|---|
| Principle assignments checked | 257 |
| Misapplied | **133 (52%)** |
| Papers with at least one uncovered insight | 97 of 135 |
| Per-batch misapplication rate | 41–64% — uniform, not concentrated |

The `balance` audit that ran before this one is validated by it: only 2 `balance` tags were
flagged here, against 74% for `cache` and 78% for `fuse`.

## Misapplication by principle

Ordered by failure rate. These are candidates for removal or re-homing, not yet applied.

### `cache` — 35 of 47 wrong (74%)

The default junk tag for any avoidance of expensive work: simulation, routing, filtering,
replication, runtime gating, surrogate models, record-and-replay. In most cases nothing is
stored and nothing is reused.

accelerating-large-scale-reasoning · accelopt · agentic-operator-generation · airs ·
approxmlir · beat-the-long-tail · breaking-the-ice · dreamddp · dynaflow · earthsight ·
event-tensor · flashinfer-bench · florist · ghostserve · guard · hippocampus · meeting-slos ·
mlcommons-chakra · once-for-all-channel-mixers · ontology-guided · optimizing-deployment-configurations ·
pla-serve · prism · protoken · raidserve · respec · scaling-up-semantic · skipkv · specdiff-2 ·
speculative-decoding-performance-or-illusion · swiftgs · unified-llm-model · verimoa ·
when-enough-is-enough · zk-apex

Notable: `ghostserve` was tagged because the protected object is a KV *cache* — the word
appearing in the paper was enough.

### `fuse` — 29 of 37 wrong (78%)

Used for "anything that reduces bytes moved," including network multicast, federated upload
volume, RDMA write granularity, DMA-vs-SM engine choice, and ZeRO state partitioning.

a-lightweight-noc · blasst · boost · demystifying-moe · efficient-long-context · executorch ·
faascale · fabric-lib · flashattention-4 · flashinfer-bench · florist · fp8-flow-moe ·
freescale-recs · hipkittens · intattention · kitty · mixllm · moeblaze · parallelkittens ·
privatar · scaling-up-semantic · search-your-block-fp-scales · shannonic · ship · spira ·
unleashing-context-parallelism · wave · zero-redundancy-dp · zorse

### `tier` — 22 of 33 wrong (67%)

Used as a synonym for "uses less memory." Almost none of these describe hot/cold placement
across a hierarchy with an eviction policy.

batchllm · contextpilot · craft · dataflow · executorch · flashlight · from-tokens-to-layers ·
ghostserve · hipkittens · hippocampus · intattention · leann · mac-attention · mixllm ·
morphserve · once-for-all · ontology-guided · raidserve · search-your-block-fp-scales ·
shannonic · using-span-queries · wave

### `skip` — 16 of 25 wrong (64%)

Applied where the dropped work is *lossy*. `approximate` is the correct home for most.

approxmlir · attribution-based-sparse-activation · beat-the-long-tail · craft · db-sp · kitty ·
mixllm · moeblaze · opkv · player-fl · protoken · reparo · spira ·
toward-principled-llm-safety-testing · when-enough-is-enough · zk-apex

### `search-ai` — 7 of 15 wrong (47%)

Applied to any ML-in-systems paper with a measurable objective, even with no search loop.
`virtual-machine-numa-placement` is a learned policy; `prompts` explicitly *replaces* search.

hawkeye · learning-from-less · parrot · prompts · unified-llm-model ·
virtual-machine-numa-placement · when-machine-learning-isnt-sure

### `pipeline` — 13 of 38 wrong

beam · beyond-the-buzz · cdlm · fabric-lib · flextrain · hexiscale · matrix · ml-fleet ·
prism · rethinking-dvfs · specdiff-2 · the-openhands-sdk · tidar

### Remainder

`balance` (demystifying-moe, guard) · `measure` (blueprint, cost-aware-duration-prediction) ·
`speculate` (cdlm) · `recompute` (protrain) · `specialize` (adr) · `simplify` (parallelkittens)

## The under-used tail exists because of the over-used head

Much of the fix needs no new principles — only moving tags to neglected existing ones.

| Principle | Current | Papers the audit says should carry it |
|---|---|---|
| `approximate` | **1** | attribution-based-sparse-activation, approxmlir, when-enough-is-enough, zk-apex, intattention, hippocampus, mac-attention, flexicache, helios, scaling-up-semantic, streamdiffusionv2, unified-llm-model |
| `portable` | 1 | fabric-lib (its entire thesis), hipkittens, executorch, mlcommons-chakra, xprof |
| `specialize` | 1 | triinfer, demystifying-moe, beyond-the-buzz, flexicache, efficient-long-context |
| `elastic` | 1 | airs (its actual core), triinfer |
| `recompute` | 2 | moeblaze, once-for-all, reparo, grinnder |
| `batch` | **0** | locality-aware-beam-scheduling, leann, efficient-long-context, opkv, vescale-fsdp, g-hemp |
| `quantize` | 5 | mixllm (a quantization paper, untagged), search-your-block-fp-scales |
| `measure` | 22 | guard |

`batch` at zero was never a sign the idea is unused — six papers need it.

## Genuine gaps

Ranked by count of independent papers. A theme should clear the bar `measure` cleared before
becoming a principle.

| Missing idea | Papers |
|---|---|
| **Cheapest-first cascade** — order evaluators by cost, escalate only what the cheap one cannot settle | adr, boute, ontology-guided, helios, earthsight, airs |
| **Cost-model configuration search, no AI** — `search-ai` requires agents, so planners and autotuners have no home | optimizing-deployment-configurations, protrain, nest, zorse, hexiscale, hetrl, search-your-block-fp-scales |
| **Non-uniform budget allocation by measured sensitivity** | kitty, mixllm, craft, beat-the-long-tail, privatar |
| **Fault tolerance — forward progress over peak utilization** | raidserve, sparing, ghostserve, guard, ml-fleet |
| **Separate policy from mechanism behind a stable interface** | dynaflow, opkv, wave, vescale-fsdp |
| **Deadline-driven scheduling; spend slack deliberately** | streamdiffusionv2, superinfer, pla-serve, beam |
| **Gate a learned component; fall back outside its envelope** | when-machine-learning-isnt-sure, virtual-machine-numa, respec |
| **Rewrite the computation so a blocked optimization becomes legal** | farskip (architectural), flashlight (algebraic), cdlm (block-causal mask) |
| **Partition replicated state so per-worker footprint shrinks** — the ZeRO premise | zero-redundancy-dp, zorse |
| **Compute inside the data path rather than at endpoints** | a-lightweight-noc, tokenweave |
| **Canonicalize inputs so near-duplicate work becomes reusable** | contextpilot, using-span-queries |
| **Energy as a schedulable resource** | beam, rethinking-dvfs |

## The structural finding

Three whole contribution categories have no axis at all, because all 17 principles are
cost-oriented:

- **Fault tolerance** — raidserve, sparing, ghostserve
- **Provenance and verifiability** — protoken, zk-apex, blueprint, hawkeye
- **Privacy partitioning** — privatar, disagg, protoken

Every one of these papers received a nonsensical tag. Not carelessness — there was nowhere
correct to put them.

`ml-fleet-tpu-goodput` states the case most directly: scheduling goodput already exceeds 95%
in Google's fleet, so the dominant waste is crashes, checkpoint/restart and stall recovery —
**lost forward progress, not low utilization.** No principle can express that.

## Suggested order of work

1. **Re-home misapplied tags onto existing under-used principles.** Biggest win, no taxonomy
   change, and it fixes `approximate`, `portable`, `specialize`, `elastic`, `recompute`, `batch`
   at the same time.
2. **Add the top 3–4 new principles**, each backed by 5+ independent papers.
3. **Re-audit**, since step 1 will move papers and step 2 changes the target set.

Do not apply steps 1 and 2 in a single pass — the balance audit removed 76% of what it
touched, and a simultaneous edit across every principle would be too large to review.
