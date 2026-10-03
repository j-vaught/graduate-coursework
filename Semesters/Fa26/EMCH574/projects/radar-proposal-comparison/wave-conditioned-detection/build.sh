#!/bin/sh
set -eu
cd "$(dirname "$0")"
node src/analytical-data.mjs
for figure in heave edge mechanism; do
    typst compile --root . "figures/src/$figure-standalone.typ" "figures/generated/$figure.pdf"
done
typst compile proposal.typ proposal.pdf
pdfinfo proposal.pdf
