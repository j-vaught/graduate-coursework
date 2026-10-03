#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
node src/analytical-data.mjs
typst compile --root . figures/src/schematic.typ figures/generated/acquisition.pdf
typst compile --root . figures/src/response.typ figures/generated/response.pdf
typst compile --root . figures/src/error.typ figures/generated/error.pdf
typst compile --root . proposal.typ proposal.pdf
mkdir -p tmp/pdfs
if command -v pdftoppm >/dev/null 2>&1; then
    pdftoppm -r 140 -png proposal.pdf tmp/pdfs/page
fi
if command -v pdftotext >/dev/null 2>&1; then
    pdftotext -layout proposal.pdf tmp/pdfs/proposal.txt
fi
