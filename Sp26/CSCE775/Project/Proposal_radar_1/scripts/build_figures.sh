#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
FIG_SRC="$ROOT_DIR/drafts/figures/src"
FIG_OUT="$ROOT_DIR/drafts/figures"

mkdir -p "$FIG_OUT"

for tex in "$FIG_SRC"/*.tex; do
  base="$(basename "$tex" .tex)"
  pushd "$FIG_SRC" >/dev/null
  latexmk -g -pdf -interaction=nonstopmode -halt-on-error "$base.tex"
  popd >/dev/null
  cp "$FIG_SRC/$base.pdf" "$FIG_OUT/$base.pdf"
done

echo "Built figures in $FIG_OUT"
