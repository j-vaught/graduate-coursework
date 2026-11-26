#!/usr/bin/env bash
set -euo pipefail

# Compile the ASME manuscript on the configured COMECH or COCESR hosts.
host="$(hostname -s | tr '[:upper:]' '[:lower:]')"
case "$host" in
  comech-*|cocesr-*) ;;
  *)
    echo "Run this build on a configured COMECH or COCESR host (current host: $host)." >&2
    exit 2
    ;;
esac

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$root"
mkdir -p build/asme

export TEXINPUTS="$root/format/asmeconf:${TEXINPUTS:-}"
export BSTINPUTS="$root/format/asmeconf:${BSTINPUTS:-}"

latexmk -lualatex -halt-on-error -interaction=nonstopmode \
  -outdir=build/asme manuscript.tex
