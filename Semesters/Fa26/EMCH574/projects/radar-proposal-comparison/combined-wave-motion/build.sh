#!/bin/sh
set -eu
cd "$(dirname "$0")"
node src/illustrative-model.mjs
uv sync --frozen
uv run python src/published_evidence.py --download
mkdir -p figures/generated
for figure in mechanism geometry; do
    typst compile --root . "figures/src/$figure-standalone.typ" "figures/generated/$figure.pdf"
done
for diagram in obstruction beam-misalignment timing; do
    typst compile --root . --input "diagram=$diagram" figures/src/observation-diagrams.typ "figures/generated/$diagram.pdf"
    typst compile --root . --input "diagram=$diagram" --ppi 180 figures/src/observation-diagrams.typ "figures/generated/$diagram.png"
done
for plot in motion power amplitude beam phase mapping; do
    typst compile --root . --input "plot=$plot" figures/src/plot-standalone.typ "figures/generated/$plot.pdf"
done
for plot in visibility raytime measured survival; do
    typst compile --root . --input "plot=$plot" figures/src/evidence-standalone.typ "figures/generated/$plot.pdf"
done
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error proposal.tex
pdfinfo proposal.pdf
