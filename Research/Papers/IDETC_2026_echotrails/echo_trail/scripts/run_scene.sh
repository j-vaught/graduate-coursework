#!/bin/bash
# Run a single scene through the radar generation pipeline (stages 1-4 only)
# Then create a GIF preview with bounding boxes.
#
# Usage: bash run_scene.sh <scene_yaml> <output_name>
# Example: bash run_scene.sh scenes/a1_trail_length/stationary.yaml a1_stationary

set -e

SCENE_YAML="$1"
OUTPUT_NAME="$2"

if [ -z "$SCENE_YAML" ] || [ -z "$OUTPUT_NAME" ]; then
    echo "Usage: bash run_scene.sh <scene_yaml> <output_name>"
    exit 1
fi

# Paths
PIPELINE_DIR="/Volumes/MacShare/Code/radar-scene-augmentation/scene-generator"
DATA_DIR="/Volumes/MacShare/Code/Generative_Radar/Composite_tier/data"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/../outputs/$OUTPUT_NAME"

ANNOT="$DATA_DIR/../../radar-scene-augmentation/data/annotation_charleston.json"
LAND="$DATA_DIR/land_frames_charleston"
LIB="$DATA_DIR/object_library_charleston"

echo "=== Generating scene: $OUTPUT_NAME ==="
echo "  YAML: $SCENE_YAML"
echo "  Output: $OUTPUT_DIR"

# Run pipeline (stages 1-4: load, plan, CSV, PNG)
cd "$PIPELINE_DIR"
python3 main.py \
    -a "$ANNOT" \
    --land-frames "$LAND" \
    --library "$LIB" \
    -o "$OUTPUT_DIR" \
    --scene "$SCRIPT_DIR/$SCENE_YAML" \
    --png \
    --allow-land \
    --threads 4

# Create GIF preview
echo ""
echo "=== Creating GIF preview ==="
cd "$SCRIPT_DIR"
python3 visualize_dataset.py "$OUTPUT_DIR" --max-frames 200 --fps 10

echo ""
echo "=== Done: $OUTPUT_NAME ==="
echo "  Images: $OUTPUT_DIR/images/"
echo "  Labels: $OUTPUT_DIR/YOLO_labels/"
echo "  GIF:    $OUTPUT_DIR/preview.gif"
