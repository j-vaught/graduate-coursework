#!/bin/bash
# A1 Trail Length Ablation: generate trails + train YOLO for each N
# Run on comech-2080: nohup bash ~/echo_trail/run_a1_ablation.sh &
#
# Trail lengths: 0, 1, 3, 6, 10, 15, 20
# Scenes 1-9 = train, Scene 10 = val/test
# All runs use same YOLO config and epoch count for fair comparison.

set -e

BASE_DIR="$HOME/echo_trail"
RAW_DIR="$BASE_DIR/a1_trail_length/raw_data"
TRAIL_DIR="$BASE_DIR/a1_trail_length/trails"
YOLO_DIR="$BASE_DIR/a1_trail_length/yolo"
RESULTS_DIR="$BASE_DIR/a1_trail_length/results"
SCRIPT="$BASE_DIR/apply_trails.py"

TRAIL_LENGTHS=(0 1 3 6 10 15 20)
TRAIN_SCENES=(01 02 03 04 05 06 07 08 09)
VAL_SCENES=(10)
EPOCHS=100
IMGSZ=640
BATCH=16

mkdir -p "$TRAIL_DIR" "$YOLO_DIR" "$RESULTS_DIR"

echo "=========================================="
echo "A1 Trail Length Ablation"
echo "Trail lengths: ${TRAIL_LENGTHS[*]}"
echo "Train scenes: ${TRAIN_SCENES[*]}"
echo "Val scenes: ${VAL_SCENES[*]}"
echo "Epochs: $EPOCHS | ImgSz: $IMGSZ | Batch: $BATCH"
echo "=========================================="
echo ""

for N in "${TRAIL_LENGTHS[@]}"; do
    echo "================================================"
    echo "Processing N=$N"
    echo "================================================"

    N_DIR="$TRAIL_DIR/N_${N}"
    YOLO_DATASET="$YOLO_DIR/N_${N}"
    TRAIN_IMG="$YOLO_DATASET/images/train"
    TRAIN_LBL="$YOLO_DATASET/labels/train"
    VAL_IMG="$YOLO_DATASET/images/val"
    VAL_LBL="$YOLO_DATASET/labels/val"

    mkdir -p "$TRAIN_IMG" "$TRAIN_LBL" "$VAL_IMG" "$VAL_LBL"

    # --- Generate trails for each scene ---
    for SCENE_NUM in "${TRAIN_SCENES[@]}" "${VAL_SCENES[@]}"; do
        SCENE_RAW="$RAW_DIR/scene_${SCENE_NUM}"
        SCENE_OUT="$N_DIR/scene_${SCENE_NUM}"

        if [ -d "$SCENE_OUT/trail_images" ] && [ "$(ls "$SCENE_OUT/trail_images/"*.png 2>/dev/null | wc -l)" -ge 50 ]; then
            echo "  Scene $SCENE_NUM N=$N already done, skipping"
        else
            echo "  Generating trails for scene $SCENE_NUM (N=$N)..."
            if [ "$N" -eq 0 ]; then
                # N=0: no trail, just convert grayscale to green-on-black RGB
                mkdir -p "$SCENE_OUT/trail_images"
                python3 -c "
import numpy as np
from PIL import Image
from pathlib import Path
import sys

src = Path('$SCENE_RAW/images')
dst = Path('$SCENE_OUT/trail_images')
for f in sorted(src.glob('*.png')):
    gray = np.array(Image.open(f).convert('L'), dtype=np.float32) / 255.0
    rgb = np.zeros((*gray.shape, 3), dtype=np.uint8)
    rgb[:,:,1] = np.clip(gray * 255, 0, 255).astype(np.uint8)
    Image.fromarray(rgb, 'RGB').save(dst / f.name)
print(f'  N=0 converted {len(list(src.glob(\"*.png\")))} frames for scene $SCENE_NUM')
"
            else
                python3 "$SCRIPT" \
                    --images-dir "$SCENE_RAW/images" \
                    --labels-dir "$SCENE_RAW/YOLO_labels" \
                    --output-dir "$SCENE_OUT" \
                    --trail-length "$N" \
                    --decay linear \
                    --intensity-mode proportional \
                    --color-mode twotone \
                    --threads 8
            fi
        fi

        # --- Symlink/copy into YOLO dataset structure ---
        if echo "${TRAIN_SCENES[@]}" | grep -qw "$SCENE_NUM"; then
            SPLIT_IMG="$TRAIN_IMG"
            SPLIT_LBL="$TRAIN_LBL"
        else
            SPLIT_IMG="$VAL_IMG"
            SPLIT_LBL="$VAL_LBL"
        fi

        # Copy trail images with scene prefix to avoid name collisions
        for img in "$SCENE_OUT/trail_images/"*.png; do
            [ -f "$img" ] || continue
            fname=$(basename "$img")
            cp -f "$img" "$SPLIT_IMG/s${SCENE_NUM}_${fname}"
        done

        # Copy labels (from raw, same for all N values)
        for lbl in "$SCENE_RAW/YOLO_labels/"*.txt; do
            [ -f "$lbl" ] || continue
            fname=$(basename "$lbl")
            cp -f "$lbl" "$SPLIT_LBL/s${SCENE_NUM}_${fname}"
        done
    done

    echo "  YOLO dataset N=$N: $(ls "$TRAIN_IMG" | wc -l) train, $(ls "$VAL_IMG" | wc -l) val images"

    # --- Write YOLO dataset YAML ---
    YAML_PATH="$YOLO_DATASET/dataset.yaml"
    cat > "$YAML_PATH" <<YAMLEOF
path: $YOLO_DATASET
train: images/train
val: images/val

names:
  0: target
YAMLEOF

    # --- Train YOLO ---
    RUN_NAME="a1_N${N}"
    echo "  Training YOLOv8n: $RUN_NAME ($EPOCHS epochs)..."
    python3 -c "
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
results = model.train(
    data='$YAML_PATH',
    epochs=$EPOCHS,
    imgsz=$IMGSZ,
    batch=$BATCH,
    name='$RUN_NAME',
    project='$RESULTS_DIR',
    device=0,
    workers=8,
    exist_ok=True,
    verbose=True,
)
print('Training complete for N=$N')
"
    echo "  Done training N=$N"
    echo ""
done

echo "=========================================="
echo "A1 Ablation complete!"
echo "Results in: $RESULTS_DIR"
echo "=========================================="

# Print summary of all runs
echo ""
echo "=== RESULTS SUMMARY ==="
for N in "${TRAIL_LENGTHS[@]}"; do
    METRICS="$RESULTS_DIR/a1_N${N}/results.csv"
    if [ -f "$METRICS" ]; then
        echo "N=$N: $(tail -1 "$METRICS")"
    else
        echo "N=$N: no results found"
    fi
done
