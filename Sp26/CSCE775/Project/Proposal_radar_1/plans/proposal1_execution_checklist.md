# Proposal 1 Execution Checklist

## Planning and Scoping
- [ ] Lock task definition and primary real-data metric.
- [ ] Freeze simulator parameter list and bounds.
- [ ] Define train/val/test split by location and environment.

## Literature and Related Work
- [ ] Download open-access papers from manifest.
- [ ] Fill notes for each paper (method, strengths, limits, relevance).
- [ ] Add any additional 2024-2026 radar sim2real papers.

## Baselines
- [ ] Fixed synthetic baseline.
- [ ] Random domain-randomization baseline.
- [ ] Bayesian optimization baseline.

## RL Method
- [ ] SAC outer loop (core).
- [ ] TD3 fallback configuration.
- [ ] Environment-conditioned and non-conditioned variants.

## Evaluation
- [ ] In-domain test.
- [ ] Cross-domain holdout test.
- [ ] Unseen-location test.
- [ ] Low-SNR stress test.
- [ ] Seed variance analysis.

## Writing Deliverables
- [ ] Complete IEEE proposal draft.
- [ ] Complete ASME alternate draft.
- [ ] Build final PDFs into `final/`.
- [ ] Verify references and citation formatting.
