# Proposal_radar_1 Workspace

This workspace contains all artifacts for Proposal 1 in CSCE 775:
"RL-Tuned Synthetic Marine Radar for Sim-to-Real Transfer."

## Quickstart

0. (One-time for ASME build on minimal TeX installs)
```bash
tlmgr init-usertree
tlmgr --usermode install inconsolata doi
```

1. Download/refresh papers:
```bash
./scripts/download_papers.sh
```

2. Build vector figures:
```bash
./scripts/build_figures.sh
```

3. Generate published-evidence result figures:
```bash
./scripts/generate_published_evidence_figures.py
```

4. Build IEEE draft PDF:
```bash
./scripts/build_ieee.sh
```

5. Build ASME draft PDF:
```bash
./scripts/build_asme.sh
```

## Folder Layout

- `plans/`: master plan and execution checklist.
  - Includes `proposal1_related_work_matrix.md` for explicit prior-work vs improvement mapping.
  - Includes `proposal1_confidence_upgrade.md` summarizing quantified evidence and next confidence steps.
- `papers/`: manifest, PDFs, and paywalled links.
- `bibliography/`: shared BibTeX database.
- `templates/`: local IEEE and ASME class/template sources.
- `drafts/`: LaTeX sources for IEEE and ASME variants.
- `drafts/figures/`: generated full-width figure PDFs and figure source files.
- `results/`: quantitative evidence summaries and failure catalog from literature.
- `final/`: compiled PDF outputs.
- `scripts/`: reproducible download/build scripts.

## Notes

- IEEE is the primary writing style for this project.
- ASME is included as an alternate style path.
- Paywalled papers are tracked in `papers/paywalled_links.md` for manual institutional access.
