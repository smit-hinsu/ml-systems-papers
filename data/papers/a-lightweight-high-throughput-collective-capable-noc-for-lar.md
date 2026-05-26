---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
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
organizations:
- ETH Zurich
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 2.9× geomean multicast speedup and 2.5× reduction speedup on 1–32 KiB
  payloads; up to 2.1× GEMM performance gain with only 16.5% router area overhead
models_evaluated: []
observations:
  pipeline: Direct Compute Access keeps collective communication off
    the GEMM critical path; multicast and reduction operations complete in the network
    fabric while cores continue computing, eliminating stalls on large-mesh topologies.
  fuse: In-network reduction via DCA aggregates partial results inside
    routers rather than routing raw data to a dedicated reduction core and back, cutting
    the number of hops that data must traverse before being consumed.
official_category: ''
openreview_url: https://openreview.net/forum?id=VDuS8N9RCx
presentation_type: oral
principles:
- pipeline
- fuse
problem: On-chip collective communication (multicast, reduction) stalls GEMM pipelines
  on large ML accelerator meshes because unicast NoCs serialize data transfers with
  compute.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
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

A **Network-on-Chip (NoC)** is the internal interconnect fabric inside a chip that connects processing cores, memory banks, and I/O — analogous to a PCIe bus or NVLink, but etched into the die itself. In ML accelerator chips (TPUs, Trainium, custom ASICs), hundreds of cores must exchange partial sums during matrix multiplications via **collective operations**: all-reduce aggregates contributions from every core, multicast replicates weights or activations to many cores. Today's NoCs route all such traffic as unicast — one packet, one destination — so a multicast to N cores requires N separate transmissions, and an all-reduce requires shuttling data out of the core, through the network, back into a reduction core, then back out to destinations. Each hop wastes bandwidth and stalls the GEMM pipeline waiting for results.

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
