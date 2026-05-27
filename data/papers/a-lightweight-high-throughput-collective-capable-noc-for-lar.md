---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Luca Colagrande
- Lorenzo Leone
- Chen Wu
- Tim Fischer
- Raphael Roth
- Luca Benini
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- ml-kernels
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 2.9× geomean multicast speedup and 2.5× reduction speedup on 1–32 KiB
  payloads; up to 2.1× GEMM performance gain with only 16.5% router area overhead
models_evaluated: []
observations:
  fuse: In-network reduction via DCA aggregates partial results inside routers rather
    than routing raw data to a dedicated reduction core and back, cutting the hop
    count before consumption.
  pipeline: Direct Compute Access keeps collectives off the GEMM critical path; multicast
    and reduction complete in the network fabric while cores continue computing, eliminating
    stalls on large meshes.
official_category: ''
openreview_url: https://openreview.net/forum?id=VDuS8N9RCx
organizations:
- ETH Zurich
presentation_type: oral
principles:
- pipeline
- fuse
problem: On-chip collectives (multicast, reduction) stall GEMM pipelines on large
  ML accelerator meshes because unicast NoCs serialize data transfers with compute.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3804_dj4EVAy.pdf
slug: a-lightweight-high-throughput-collective-capable-noc-for-lar
status: draft
title: A Lightweight High-Throughput Collective-Capable NoC for Large-Scale ML Accelerators
topics:
- all-reduce
- tensor-parallelism
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3804
---

## Background

In ML accelerator chips (TPUs, custom ASICs), hundreds of cores must exchange partial sums during matrix multiplications via collective operations: all-reduce aggregates contributions from every core, multicast replicates weights or activations to many cores. Today's on-chip networks (NoCs) route all traffic as unicast — one packet, one destination — so a multicast to N cores requires N transmissions and an all-reduce must shuttle data out to a reduction core and back. Each hop wastes bandwidth and stalls the GEMM pipeline.

## Key Contributions

- **Direct Compute Access (DCA)**: novel NoC paradigm that grants the interconnect fabric direct read/write access to core computational resources, enabling the router to perform in-network reductions without routing data through the core's memory subsystem; adds only 16.5% router area overhead
- **In-network multicast**: hardware-accelerated multicast delivers a 2.9× geomean speedup over unicast for 1–32 KiB payloads by replicating packets inside the fabric rather than requiring the source core to transmit N separate unicast messages
- **In-network reduction**: hardware-accelerated all-reduce achieves 2.5× geomean speedup by aggregating partial sums inside routers on the way to the destination, reducing data traffic and eliminating intermediate buffer hops
- **Off-critical-path collectives for GEMM scaling**: by completing multicast and reduction in the fabric concurrently with GEMM execution, the system achieves up to 2.1× estimated performance gain on large meshes compared to a unicast baseline

## Trade-offs

- DCA ties the NoC router design to specific core computational interfaces; changing the core architecture or adding new data types requires co-design of the router.
- In-network compute introduces potential ordering hazards; the paper does not characterize behavior under concurrent collectives from multiple initiators.

## Nuances

- Performance estimates for GEMM scaling are projected rather than measured on silicon; the 2.1× gain is an analytical model result.
- The 16.5% router area overhead applies per router; aggregate die area impact depends on mesh size and router-to-core area ratio in the target process node.