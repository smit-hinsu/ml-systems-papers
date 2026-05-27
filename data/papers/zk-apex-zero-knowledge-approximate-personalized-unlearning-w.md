---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Mohammad M Maheri
- Sunil Cotterill
- Alex Davidson
- Hamed Haddadi
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: ZK-SNARK proofs complete in ~2 hours (10^7× faster than retraining),
  <0.7 GB peak memory, 99% Top-1 accuracy on ViT after unlearning.
models_evaluated:
- ViT (Vision Transformer)
- OPT-125M
observations:
  cache: Zero-shot unlearning via sparse masking and block-wise Fisher compensation
    avoids full retraining, removing targeted samples from personalized models in one
    forward-backward pass.
  skip: Provider-side sparse masking targets only the parameters most
    responsible for the forgotten samples, applying a minimal surgical update rather
    than globally perturbing the model.
official_category: ''
openreview_url: https://openreview.net/forum?id=bLx6orLvQM
organizations:
- Imperial College London
presentation_type: oral
principles:
- cache
- skip
problem: Verifying correct machine unlearning in personalized distributed models is
  intractable with retraining; edge device clients may falsify deletion.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: zk-apex-zero-knowledge-approximate-personalized-unlearning-w
status: draft
title: 'ZK-APEX: ZERO-KNOWLEDGE APPROXIMATE PERSONALIZED UNLEARNING WITH EXECUTABLE PROOFS'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3793
---

## Background

Machine unlearning removes the influence of specific training data from a deployed model, as required by GDPR "right to be forgotten" requests. Retraining is prohibitively expensive, so approximate unlearning applies a lightweight update instead. In personalized federated learning, each user has a locally fine-tuned model, and the provider must trust the prescribed update was applied — verifying this without receiving weights violates privacy. ZK-SNARKs can certify a computation without revealing inputs, but prior systems couldn't scale to neural network operations.

## Key Contributions

- **ZK-APEX**: first verifiable personalized unlearning framework practical for edge devices; combines provider-side sparse masking with client-side Group-OBS compensation and Halo2 ZK-SNARKs to prove correct unlearning without revealing private model parameters or data.
- **Provider-side sparse masking**: identifies and zeros out the parameters most responsible for the data to be forgotten using a sparse masking strategy, enabling targeted removal with minimal collateral impact on model utility.
- **Client-side Group-OBS compensation**: applies a curvature-aware update computed from a block-wise empirical Fisher matrix to compensate for masked parameters, recovering model accuracy while maintaining low computational overhead on edge devices.
- **ZK-SNARK compliance proof**: uses Halo2 ZK-SNARKs to prove that the unlearned model exactly matches the committed output of the prescribed transformation, providing cryptographic unlearning verification without data exposure.
- ZK proof generation for ViT classification completes in ~2 hours (10^7× faster than retraining-based verification), with peak memory under 0.7 GB and proof size ~400 MB; recovers ~99% Top-1 accuracy on ViT and ~70% on OPT-125M.

## Trade-offs

- ZK proof generation takes ~2 hours and produces ~400 MB proofs; while vastly faster than retraining, this is not suitable for real-time or high-frequency unlearning requests.
- The approach is "approximate" unlearning: Group-OBS compensation is a first-order approximation that may leave residual influence of forgotten data, which does not satisfy formal exact unlearning guarantees.

## Nuances

- Evaluation is on ViT classification and OPT-125M (code generation); behavior on large language models with hundreds of billions of parameters would require significantly larger Fisher computations and longer proof generation.
- The ~70% accuracy recovery on OPT-125M is substantially lower than the ~99% on ViT; the gap suggests the method may be less effective for generative language models.
