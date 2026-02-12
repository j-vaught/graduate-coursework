#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFEST="$ROOT_DIR/papers/paper_manifest.csv"
PDF_DIR="$ROOT_DIR/papers/pdfs"
LOG_FILE="$ROOT_DIR/papers/download_failures.log"
TMP_FILE="$(mktemp)"

mkdir -p "$PDF_DIR"
: > "$LOG_FILE"

header="id,title,year,venue_or_type,topic_tag,url_abs,url_pdf,access,status,local_pdf_path,notes"
echo "$header" > "$TMP_FILE"

# Skip header row
while IFS=',' read -r id title year venue topic url_abs url_pdf access status local_pdf_path notes; do
  [[ "$id" == "id" ]] && continue

  new_status="$status"
  new_local="$local_pdf_path"

  if [[ "$access" != "open" ]]; then
    echo "$id: manual access required ($url_abs)" >> "$LOG_FILE"
    new_status="pending"
    new_local=""
    echo "$id,$title,$year,$venue,$topic,$url_abs,$url_pdf,$access,$new_status,$new_local,$notes" >> "$TMP_FILE"
    continue
  fi

  effective_pdf_url="$url_pdf"
  if [[ -z "$effective_pdf_url" && "$url_abs" == *"arxiv.org/abs/"* ]]; then
    effective_pdf_url="${url_abs/\/abs\//\/pdf\/}.pdf"
  fi

  out_path="$PDF_DIR/${id}.pdf"
  if curl -L --fail --retry 2 --connect-timeout 20 --max-time 300 -o "$out_path" "$effective_pdf_url" >/dev/null 2>&1; then
    if [[ -s "$out_path" ]] && [[ "$(head -c 4 "$out_path" 2>/dev/null || true)" == "%PDF" ]]; then
      new_status="downloaded"
      new_local="papers/pdfs/${id}.pdf"
    else
      new_status="failed"
      new_local=""
      rm -f "$out_path"
      echo "$id: downloaded file is not a valid PDF ($effective_pdf_url)" >> "$LOG_FILE"
    fi
  else
    new_status="failed"
    new_local=""
    rm -f "$out_path"
    echo "$id: download failed ($effective_pdf_url)" >> "$LOG_FILE"
  fi

  echo "$id,$title,$year,$venue,$topic,$url_abs,$url_pdf,$access,$new_status,$new_local,$notes" >> "$TMP_FILE"
done < "$MANIFEST"

mv "$TMP_FILE" "$MANIFEST"

echo "Download complete. See manifest and $LOG_FILE for details."
