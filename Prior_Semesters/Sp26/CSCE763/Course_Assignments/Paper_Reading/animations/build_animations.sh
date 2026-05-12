#!/bin/bash
# Build all TikZ animations into GIFs using tikzgif
# Output goes to ../figures/

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/../figures"
mkdir -p "$OUTPUT_DIR"

# Common settings
COMMON_OPTS="--quality presentation --dpi 300 --fps 1 --author 'J.C. Vaught'"

echo "=== Building Animation 1: Metric Ambiguity (4 frames) ==="
tikzgif render "$SCRIPT_DIR/anim1_metric_ambiguity.tex" \
    --frames 4 --start 0 --end 0.99 \
    --fps 1 --pause-last-ms 2000 \
    --quality presentation --dpi 300 \
    --author "J.C. Vaught" \
    -o "$OUTPUT_DIR/anim1_metric_ambiguity.gif"

echo "=== Building Animation 2: CSTM Pipeline (6 frames) ==="
tikzgif render "$SCRIPT_DIR/anim2_cstm_pipeline.tex" \
    --frames 6 --start 0 --end 0.99 \
    --fps 1 --pause-last-ms 2000 \
    --quality presentation --dpi 300 \
    --author "J.C. Vaught" \
    -o "$OUTPUT_DIR/anim2_cstm_pipeline.gif"

echo "=== Building Animation 3: ConvGRU Refinement (5 frames) ==="
tikzgif render "$SCRIPT_DIR/anim3_convgru_refinement.tex" \
    --frames 5 --start 0 --end 0.99 \
    --fps 1 --pause-last-ms 2000 \
    --quality presentation --dpi 300 \
    --author "J.C. Vaught" \
    -o "$OUTPUT_DIR/anim3_convgru_refinement.gif"

echo "=== Building Animation 4: RPNL (3 frames) ==="
tikzgif render "$SCRIPT_DIR/anim4_rpnl.tex" \
    --frames 3 --start 0 --end 0.99 \
    --fps 1 --pause-last-ms 2000 \
    --quality presentation --dpi 300 \
    --author "J.C. Vaught" \
    -o "$OUTPUT_DIR/anim4_rpnl.gif"

echo ""
echo "=== All animations built ==="
ls -lh "$OUTPUT_DIR"/anim*.gif
