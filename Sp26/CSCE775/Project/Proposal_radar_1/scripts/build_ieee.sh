#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DRAFT_DIR="$ROOT_DIR/drafts"
OUT_DIR="$ROOT_DIR/final"

mkdir -p "$OUT_DIR"

# Ensure generated quantitative evidence figure is up to date.
"$ROOT_DIR/scripts/generate_published_evidence_figures.py"

pushd "$DRAFT_DIR" >/dev/null
latexmk -g -pdf -interaction=nonstopmode -halt-on-error proposal1_ieee.tex
cp proposal1_ieee.pdf "$OUT_DIR/proposal1_ieee_final.pdf"
latexmk -c
popd >/dev/null

echo "Built $OUT_DIR/proposal1_ieee_final.pdf"
