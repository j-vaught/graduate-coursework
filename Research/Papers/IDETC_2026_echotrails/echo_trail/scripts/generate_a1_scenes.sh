#!/bin/bash
# Generate all 10 A1 scenes (stages 1-4: load, plan, CSV, PNG+labels)
# Uses the clean Charleston library with transposed echo fix

PIPELINE="/Volumes/MacShare/Code/radar-scene-augmentation/scene-generator"
DATA="/Volumes/MacShare/Code/radar-scene-augmentation/data"
LIBRARY="/Volumes/MacShare/Code/Generative_Radar/Composite_tier/data/object_library_charleston_clean"
ANNOTATION="${DATA}/annotation_charleston.json"
LAND_FRAMES="${DATA}/land_frames_charleston"

SCENES_DIR="$(dirname "$0")/scenes/a1_trail_length"
OUTPUT_BASE="$(dirname "$0")/../outputs/a1_trail_length"

export PYTHONPATH="${PIPELINE}:${PYTHONPATH}"

for i in $(seq -w 1 10); do
    SCENE_YAML="${SCENES_DIR}/a1_scene_${i}.yaml"
    OUT_DIR="${OUTPUT_BASE}/scene_${i}"

    echo ""
    echo "============================================"
    echo "  Scene ${i} / 10"
    echo "============================================"

    python3 "${PIPELINE}/main.py" \
        -a "${ANNOTATION}" \
        --land-frames "${LAND_FRAMES}" \
        --library "${LIBRARY}" \
        -o "${OUT_DIR}" \
        --scene "${SCENE_YAML}" \
        --png \
        --export-labels \
        --threads 8

    # Clean up CSV intermediates
    if [ -d "${OUT_DIR}/csv" ]; then
        rm -rf "${OUT_DIR}/csv"
        echo "  Removed CSV intermediates"
    fi

    echo "  Scene ${i} complete: ${OUT_DIR}"
done

echo ""
echo "============================================"
echo "  All 10 scenes generated!"
echo "============================================"
