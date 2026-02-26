#!/bin/bash
# A6 Clutter Level Ablation: apply trails + train YOLO per clutter level × trail length
# Run on comech-2080: nohup bash ~/echotrail_ablation/scripts/run_a6_ablation.sh > ~/echotrail_ablation/a6_training.log 2>&1 &
#
# For each clutter level (none, low, moderate, heavy):
#   For each trail length N:
#     1. Apply trails to all 10 scenes
#     2. Organize into YOLO dataset (scenes 1-9 train, scene 10 val)
#     3. Train YOLOv8n
#
# Uses 2-class labels: 0=stationary, 1=moving

set -e

SCENES_OUT="$HOME/echotrail_ablation/scenes_out/a6_clutter"
A6_DIR="$HOME/echotrail_ablation/a6_clutter"
TRAIL_DIR="$A6_DIR/trails"
YOLO_DIR="$A6_DIR/yolo"
RESULTS_DIR="$A6_DIR/results"
SCRIPT="$HOME/echotrail_ablation/scripts/apply_trails.py"

TRAIL_LENGTHS=(0 1 2 3 4 5 10 15 20 25)
CLUTTER_LEVELS=(none low moderate heavy)
TRAIN_SCENES=(01 02 03 04 05 06 07 08 09)
VAL_SCENES=(10)
EPOCHS=50
IMGSZ=640
BATCH=16

# --- CLEAN START ---
echo "Cleaning previous outputs..."
rm -rf "$TRAIL_DIR" "$YOLO_DIR" "$RESULTS_DIR"
mkdir -p "$TRAIL_DIR" "$YOLO_DIR" "$RESULTS_DIR"

echo "=========================================="
echo "A6 Clutter Level Ablation"
echo "Clutter levels: ${CLUTTER_LEVELS[*]}"
echo "Trail lengths: ${TRAIL_LENGTHS[*]}"
echo "Train scenes: ${TRAIN_SCENES[*]}"
echo "Val scenes: ${VAL_SCENES[*]}"
echo "Epochs: $EPOCHS | ImgSz: $IMGSZ | Batch: $BATCH"
echo "=========================================="
echo ""

for CLUTTER in "${CLUTTER_LEVELS[@]}"; do
    for N in "${TRAIL_LENGTHS[@]}"; do
        echo "================================================"
        echo "Clutter=$CLUTTER  N=$N"
        echo "================================================"

        N_DIR="$TRAIL_DIR/${CLUTTER}/N_${N}"
        YOLO_DATASET="$YOLO_DIR/${CLUTTER}/N_${N}"
        TRAIN_IMG="$YOLO_DATASET/images/train"
        TRAIN_LBL="$YOLO_DATASET/labels/train"
        VAL_IMG="$YOLO_DATASET/images/val"
        VAL_LBL="$YOLO_DATASET/labels/val"

        mkdir -p "$TRAIN_IMG" "$TRAIN_LBL" "$VAL_IMG" "$VAL_LBL"

        # --- Generate trails for each scene ---
        for SCENE_NUM in "${TRAIN_SCENES[@]}" "${VAL_SCENES[@]}"; do
            SCENE_RAW="$SCENES_OUT/a6_scene_${SCENE_NUM}_${CLUTTER}/charleston"
            SCENE_OUT_TRAIL="$N_DIR/scene_${SCENE_NUM}"

            if [ ! -d "$SCENE_RAW/images" ]; then
                echo "  WARNING: Missing $SCENE_RAW/images, skipping"
                continue
            fi

            echo "  Applying trails: ${CLUTTER}/scene_${SCENE_NUM} N=$N..."
            if [ "$N" -eq 0 ]; then
                mkdir -p "$SCENE_OUT_TRAIL/trail_images"
                python3 -c "
from PIL import Image
from pathlib import Path

src = Path('$SCENE_RAW/images')
dst = Path('$SCENE_OUT_TRAIL/trail_images')
for f in sorted(src.glob('*.png')):
    gray = Image.open(f).convert('L')
    rgb = Image.merge('RGB', (gray, gray, gray))
    rgb.save(dst / f.name)
print(f'  N=0 converted {len(list(src.glob(\"*.png\")))} frames')
"
            else
                python3 "$SCRIPT" \
                    --images-dir "$SCENE_RAW/images" \
                    --labels-dir "$SCENE_RAW/YOLO_labels" \
                    --output-dir "$SCENE_OUT_TRAIL" \
                    --trail-length "$N" \
                    --decay linear \
                    --intensity-mode proportional \
                    --color-mode twotone \
                    --threads 8
            fi

            # --- Copy into YOLO dataset structure ---
            if echo "${TRAIN_SCENES[*]}" | grep -qw "$SCENE_NUM"; then
                SPLIT_IMG="$TRAIN_IMG"
                SPLIT_LBL="$TRAIN_LBL"
            else
                SPLIT_IMG="$VAL_IMG"
                SPLIT_LBL="$VAL_LBL"
            fi

            for img in "$SCENE_OUT_TRAIL/trail_images/"*.png; do
                [ -f "$img" ] || continue
                fname=$(basename "$img")
                cp -f "$img" "$SPLIT_IMG/s${SCENE_NUM}_${fname}"
            done

            for lbl in "$SCENE_RAW/YOLO_labels/"*.txt; do
                [ -f "$lbl" ] || continue
                fname=$(basename "$lbl")
                cp -f "$lbl" "$SPLIT_LBL/s${SCENE_NUM}_${fname}"
            done
        done

        NTRAIN=$(ls "$TRAIN_IMG" 2>/dev/null | wc -l)
        NVAL=$(ls "$VAL_IMG" 2>/dev/null | wc -l)
        echo "  YOLO dataset ${CLUTTER}/N_${N}: $NTRAIN train, $NVAL val images"

        # --- Write YOLO dataset YAML ---
        YAML_PATH="$YOLO_DATASET/dataset.yaml"
        cat > "$YAML_PATH" <<YAMLEOF
path: $YOLO_DATASET
train: images/train
val: images/val

names:
  0: stationary
  1: moving
YAMLEOF

        # --- Train YOLO ---
        RUN_NAME="a6_${CLUTTER}_N${N}"
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
    seed=42,
)
print('Training complete for ${CLUTTER} N=$N')
"
        echo "  Done: $RUN_NAME"
        echo ""
    done
done

echo "=========================================="
echo "A6 Ablation complete!"
echo "Results in: $RESULTS_DIR"
echo "=========================================="

# --- Summary ---
echo ""
echo "=== RESULTS SUMMARY ==="
for CLUTTER in "${CLUTTER_LEVELS[@]}"; do
    echo "--- $CLUTTER ---"
    for N in "${TRAIL_LENGTHS[@]}"; do
        METRICS="$RESULTS_DIR/a6_${CLUTTER}_N${N}/results.csv"
        if [ -f "$METRICS" ]; then
            BEST=$(awk -F, 'NR>1 {if($8+0 > max) {max=$8+0; ep=$1}} END{printf "best mAP50=%.3f (epoch %d)", max, ep}' "$METRICS")
            LAST=$(awk -F, 'END{printf "final mAP50=%.3f mAP50-95=%.3f", $8, $9}' "$METRICS")
            echo "  N=$N: $BEST | $LAST"
        else
            echo "  N=$N: no results found"
        fi
    done
done
