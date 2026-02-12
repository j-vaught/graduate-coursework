#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DRAFT_DIR="$ROOT_DIR/drafts"
OUT_DIR="$ROOT_DIR/final"

mkdir -p "$OUT_DIR"

pushd "$DRAFT_DIR" >/dev/null
latexmk -g -pdf -interaction=nonstopmode -halt-on-error proposal1_asme.tex
cp proposal1_asme.pdf "$OUT_DIR/proposal1_asme_final.pdf"
popd >/dev/null

echo "Built $OUT_DIR/proposal1_asme_final.pdf"
