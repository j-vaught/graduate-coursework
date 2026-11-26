#!/usr/bin/env bash
# Run in a project checkout on COMECH or COCESR after the data files are available.
set -euo pipefail
cd -- "$(dirname -- "$0")/../.."
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-0}"
for figure in geometry verification pilot matched operating-map; do
  source="figures/operating/$figure.typ"
  typst compile --root . --no-pdf-tags "$source" "${source%.typ}.pdf"
done
