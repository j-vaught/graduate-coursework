#!/bin/sh
set -eu
cd "$(dirname "$0")"
node src/illustrative-model.mjs
uv sync --frozen
uv run python src/wave_surface.py
uv run python src/published_evidence.py --download
mkdir -p figures/generated
for figure in mechanism geometry; do
    typst compile --root . "figures/src/$figure-standalone.typ" "figures/generated/$figure.pdf"
done
for diagram in wave-obstruction beam-misalignment scan-time-error scan-time-error-simple; do
    typst compile --root . "figures/src/$diagram.typ" "figures/generated/$diagram.pdf"
    typst compile --root . --ppi 180 "figures/src/$diagram.typ" "figures/generated/$diagram.png"
done
typst compile --root . figures/src/wave-surface.typ figures/generated/wave-surface.pdf
typst compile --root . --ppi 180 figures/src/wave-surface.typ figures/generated/wave-surface.png
for plot in motion power amplitude beam phase mapping; do
    typst compile --root . --input "plot=$plot" figures/src/plot-standalone.typ "figures/generated/$plot.pdf"
done
for plot in visibility raytime measured survival; do
    typst compile --root . --input "plot=$plot" figures/src/evidence-standalone.typ "figures/generated/$plot.pdf"
done
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error proposal.tex
pdfinfo proposal.pdf
