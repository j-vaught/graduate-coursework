#!/bin/bash
# GP Model Training: pool A1/A5/A6 + new GP scenes → single YOLO model
# Run on comech-2080: nohup bash ~/echotrail_ablation/scripts/run_gp_training.sh > ~/echotrail_ablation/gp_training.log 2>&1 &
#
# Pools ~340 configs (120 reused A1/A5/A6 + 220 new GP) with N=10 trails into one unified dataset.
# Train/val split: 90/10 per source set, then merged for single training run.
# Uses 2-class labels: 0=stationary, 1=moving

set -e

# Paths
SCRIPT="$HOME/echotrail_ablation/scripts/apply_trails.py"
GP_DIR="$HOME/echotrail_ablation/gp_model"
TRAIL_DIR="$GP_DIR/trails"
YOLO_DIR="$GP_DIR/yolo"
RESULTS_DIR="$GP_DIR/results"

# Reused scene locations
A1_SCENES="$HOME/echotrail_ablation/scenes_out/a1_trail_length"
A5_SCENES="$HOME/echotrail_ablation/scenes_out/a5_range"
A6_SCENES="$HOME/echotrail_ablation/scenes_out/a6_clutter"
GP_SCENES="$HOME/echotrail_ablation/scenes_out/gp_training"

N=10
EPOCHS=50
IMGSZ=640
BATCH=16

# --- CLEAN START ---
echo "Cleaning previous outputs..."
rm -rf "$TRAIL_DIR" "$YOLO_DIR" "$RESULTS_DIR"
mkdir -p "$TRAIL_DIR" "$YOLO_DIR" "$RESULTS_DIR"

UNIFIED_TRAIL_DIR="$TRAIL_DIR/unified"
UNIFIED_YOLO="$YOLO_DIR/unified"
TRAIN_IMG="$UNIFIED_YOLO/images/train"
TRAIN_LBL="$UNIFIED_YOLO/labels/train"
VAL_IMG="$UNIFIED_YOLO/images/val"
VAL_LBL="$UNIFIED_YOLO/labels/val"

mkdir -p "$TRAIN_IMG" "$TRAIN_LBL" "$VAL_IMG" "$VAL_LBL"

echo "=========================================="
echo "GP Model Training: Unified N=$N"
echo "=========================================="
echo "Pooling:"
echo "  - A1: 10 scenes × 1 clutter = 10 configs"
echo "  - A5: 3 ranges × 10 scenes = 30 configs (clutter only)"
echo "  - A6: 4 clutter levels × 10 scenes = 40 configs"
echo "  - GP: multiple scenario types × 10-20 scenes = 220 configs"
echo "Total: ~300 configs → unified YOLO dataset"
echo "Epochs: $EPOCHS | ImgSz: $IMGSZ | Batch: $BATCH"
echo "=========================================="
echo ""

# Counter for progress
TOTAL_PROCESSED=0

# ========================================
# A1 REUSED SCENES
# ========================================
echo "Processing A1 reused scenes..."
A1_TRAIN_SCENES=(01 02 03 04 05 06 07 08 09)
A1_VAL_SCENES=(10)

for SCENE_NUM in "${A1_TRAIN_SCENES[@]}" "${A1_VAL_SCENES[@]}"; do
    SCENE_RAW="$A1_SCENES/scene_${SCENE_NUM}/charleston"
    SCENE_OUT_TRAIL="$UNIFIED_TRAIL_DIR/a1_scene_${SCENE_NUM}"

    if [ ! -d "$SCENE_RAW/images" ]; then
        echo "  WARNING: Missing $SCENE_RAW/images, skipping"
        continue
    fi

    echo "  Applying trails: A1/scene_${SCENE_NUM} N=$N..."
    python3 "$SCRIPT" \
        --images-dir "$SCENE_RAW/images" \
        --labels-dir "$SCENE_RAW/YOLO_labels" \
        --output-dir "$SCENE_OUT_TRAIL" \
        --trail-length "$N" \
        --decay linear \
        --intensity-mode proportional \
        --color-mode twotone \
        --threads 8

    # Copy into YOLO dataset structure
    if echo "${A1_TRAIN_SCENES[*]}" | grep -qw "$SCENE_NUM"; then
        SPLIT_IMG="$TRAIN_IMG"
        SPLIT_LBL="$TRAIN_LBL"
    else
        SPLIT_IMG="$VAL_IMG"
        SPLIT_LBL="$VAL_LBL"
    fi

    for img in "$SCENE_OUT_TRAIL/trail_images/"*.png; do
        [ -f "$img" ] || continue
        fname=$(basename "$img")
        cp -f "$img" "$SPLIT_IMG/a1_s${SCENE_NUM}_${fname}"
    done

    for lbl in "$SCENE_RAW/YOLO_labels/"*.txt; do
        [ -f "$lbl" ] || continue
        fname=$(basename "$lbl")
        cp -f "$lbl" "$SPLIT_LBL/a1_s${SCENE_NUM}_${fname}"
    done

    ((TOTAL_PROCESSED++))
done

echo "  A1 scenes processed: $TOTAL_PROCESSED configs"
echo ""

# ========================================
# A5 REUSED SCENES
# ========================================
echo "Processing A5 reused scenes (clutter variant only)..."
A5_RANGES=(near mid far)
A5_TRAIN_SCENES=(01 02 03 04 05 06 07 08 09)
A5_VAL_SCENES=(10)
A5_PROCESSED=0

for RANGE in "${A5_RANGES[@]}"; do
    for SCENE_NUM in "${A5_TRAIN_SCENES[@]}" "${A5_VAL_SCENES[@]}"; do
        SCENE_RAW="$A5_SCENES/a5_${RANGE}_scene_${SCENE_NUM}/charleston"
        SCENE_OUT_TRAIL="$UNIFIED_TRAIL_DIR/a5_${RANGE}_scene_${SCENE_NUM}"

        if [ ! -d "$SCENE_RAW/images" ]; then
            echo "  WARNING: Missing $SCENE_RAW/images, skipping"
            continue
        fi

        echo "  Applying trails: A5/${RANGE}/scene_${SCENE_NUM} N=$N..."
        python3 "$SCRIPT" \
            --images-dir "$SCENE_RAW/images" \
            --labels-dir "$SCENE_RAW/YOLO_labels" \
            --output-dir "$SCENE_OUT_TRAIL" \
            --trail-length "$N" \
            --decay linear \
            --intensity-mode proportional \
            --color-mode twotone \
            --threads 8

        # Copy into YOLO dataset structure
        if echo "${A5_TRAIN_SCENES[*]}" | grep -qw "$SCENE_NUM"; then
            SPLIT_IMG="$TRAIN_IMG"
            SPLIT_LBL="$TRAIN_LBL"
        else
            SPLIT_IMG="$VAL_IMG"
            SPLIT_LBL="$VAL_LBL"
        fi

        for img in "$SCENE_OUT_TRAIL/trail_images/"*.png; do
            [ -f "$img" ] || continue
            fname=$(basename "$img")
            cp -f "$img" "$SPLIT_IMG/a5_${RANGE}_s${SCENE_NUM}_${fname}"
        done

        for lbl in "$SCENE_RAW/YOLO_labels/"*.txt; do
            [ -f "$lbl" ] || continue
            fname=$(basename "$lbl")
            cp -f "$lbl" "$SPLIT_LBL/a5_${RANGE}_s${SCENE_NUM}_${fname}"
        done

        ((A5_PROCESSED++))
        ((TOTAL_PROCESSED++))
    done
done

echo "  A5 scenes processed: $A5_PROCESSED configs"
echo ""

# ========================================
# A6 REUSED SCENES
# ========================================
echo "Processing A6 reused scenes..."
A6_CLUTTER_LEVELS=(none low moderate heavy)
A6_TRAIN_SCENES=(01 02 03 04 05 06 07 08 09)
A6_VAL_SCENES=(10)
A6_PROCESSED=0

for CLUTTER in "${A6_CLUTTER_LEVELS[@]}"; do
    for SCENE_NUM in "${A6_TRAIN_SCENES[@]}" "${A6_VAL_SCENES[@]}"; do
        SCENE_RAW="$A6_SCENES/a6_scene_${SCENE_NUM}_${CLUTTER}/charleston"
        SCENE_OUT_TRAIL="$UNIFIED_TRAIL_DIR/a6_${CLUTTER}_scene_${SCENE_NUM}"

        if [ ! -d "$SCENE_RAW/images" ]; then
            echo "  WARNING: Missing $SCENE_RAW/images, skipping"
            continue
        fi

        echo "  Applying trails: A6/${CLUTTER}/scene_${SCENE_NUM} N=$N..."
        python3 "$SCRIPT" \
            --images-dir "$SCENE_RAW/images" \
            --labels-dir "$SCENE_RAW/YOLO_labels" \
            --output-dir "$SCENE_OUT_TRAIL" \
            --trail-length "$N" \
            --decay linear \
            --intensity-mode proportional \
            --color-mode twotone \
            --threads 8

        # Copy into YOLO dataset structure
        if echo "${A6_TRAIN_SCENES[*]}" | grep -qw "$SCENE_NUM"; then
            SPLIT_IMG="$TRAIN_IMG"
            SPLIT_LBL="$TRAIN_LBL"
        else
            SPLIT_IMG="$VAL_IMG"
            SPLIT_LBL="$VAL_LBL"
        fi

        for img in "$SCENE_OUT_TRAIL/trail_images/"*.png; do
            [ -f "$img" ] || continue
            fname=$(basename "$img")
            cp -f "$img" "$SPLIT_IMG/a6_${CLUTTER}_s${SCENE_NUM}_${fname}"
        done

        for lbl in "$SCENE_RAW/YOLO_labels/"*.txt; do
            [ -f "$lbl" ] || continue
            fname=$(basename "$lbl")
            cp -f "$lbl" "$SPLIT_LBL/a6_${CLUTTER}_s${SCENE_NUM}_${fname}"
        done

        ((A6_PROCESSED++))
        ((TOTAL_PROCESSED++))
    done
done

echo "  A6 scenes processed: $A6_PROCESSED configs"
echo ""

# ========================================
# GP NEW SCENES
# ========================================
echo "Processing GP new scenes..."
# Define all GP prefixes and their scene counts
# Format: "prefix:num_scenes"
declare -a GP_PREFIXES=(
    "gp_sparse_clean:20"
    "gp_sparse_clutter:20"
    "gp_moderate_clean:20"
    "gp_moderate_low:20"
    "gp_moderate_heavy:20"
    "gp_dense_clean:20"
    "gp_dense_clutter:20"
    "gp_fast_only_clean:10"
    "gp_fast_only_clutter:10"
    "gp_stationary_clean:10"
    "gp_stationary_clutter:10"
    "gp_near_focus:10"
    "gp_far_focus:10"
    "gp_mixed_speed:20"
)

GP_PROCESSED=0

for PREFIX_SPEC in "${GP_PREFIXES[@]}"; do
    IFS=':' read -r PREFIX NUM_SCENES <<< "$PREFIX_SPEC"

    # Determine train/val split: 90/10 for 20-scene sets
    TRAIN_COUNT=18
    VAL_COUNT=2

    if [ "$NUM_SCENES" -eq 10 ]; then
        TRAIN_COUNT=9
        VAL_COUNT=1
    fi

    echo "  GP scenario: $PREFIX (scenes 01-$NUM_SCENES)..."

    for SCENE_NUM in $(seq -f "%02g" 1 "$NUM_SCENES"); do
        SCENE_RAW="$GP_SCENES/${PREFIX}_scene_${SCENE_NUM}/charleston"
        SCENE_OUT_TRAIL="$UNIFIED_TRAIL_DIR/gp_${PREFIX}_scene_${SCENE_NUM}"

        if [ ! -d "$SCENE_RAW/images" ]; then
            echo "    WARNING: Missing $SCENE_RAW/images, skipping"
            continue
        fi

        echo "    Applying trails: GP/${PREFIX}/scene_${SCENE_NUM} N=$N..."
        python3 "$SCRIPT" \
            --images-dir "$SCENE_RAW/images" \
            --labels-dir "$SCENE_RAW/YOLO_labels" \
            --output-dir "$SCENE_OUT_TRAIL" \
            --trail-length "$N" \
            --decay linear \
            --intensity-mode proportional \
            --color-mode twotone \
            --threads 8

        # Determine train/val split based on scene number
        SCENE_INT=${SCENE_NUM##*(0)}  # Remove leading zeros
        if [ "$SCENE_INT" -le "$TRAIN_COUNT" ]; then
            SPLIT_IMG="$TRAIN_IMG"
            SPLIT_LBL="$TRAIN_LBL"
        else
            SPLIT_IMG="$VAL_IMG"
            SPLIT_LBL="$VAL_LBL"
        fi

        for img in "$SCENE_OUT_TRAIL/trail_images/"*.png; do
            [ -f "$img" ] || continue
            fname=$(basename "$img")
            cp -f "$img" "$SPLIT_IMG/gp_${PREFIX}_s${SCENE_NUM}_${fname}"
        done

        for lbl in "$SCENE_RAW/YOLO_labels/"*.txt; do
            [ -f "$lbl" ] || continue
            fname=$(basename "$lbl")
            cp -f "$lbl" "$SPLIT_LBL/gp_${PREFIX}_s${SCENE_NUM}_${fname}"
        done

        ((GP_PROCESSED++))
        ((TOTAL_PROCESSED++))
    done
done

echo "  GP scenes processed: $GP_PROCESSED configs"
echo ""

# ========================================
# UNIFIED DATASET SUMMARY
# ========================================
NTRAIN=$(ls "$TRAIN_IMG" 2>/dev/null | wc -l)
NVAL=$(ls "$VAL_IMG" 2>/dev/null | wc -l)

echo "================================================"
echo "Unified YOLO Dataset Summary"
echo "================================================"
echo "Total configs processed: $TOTAL_PROCESSED"
echo "Training images: $NTRAIN"
echo "Validation images: $NVAL"
echo "Total images: $((NTRAIN + NVAL))"
echo ""

# --- Write unified YOLO dataset YAML ---
YAML_PATH="$UNIFIED_YOLO/dataset.yaml"
cat > "$YAML_PATH" <<YAMLEOF
path: $UNIFIED_YOLO
train: images/train
val: images/val

names:
  0: stationary
  1: moving
YAMLEOF

echo "YOLO dataset YAML written to: $YAML_PATH"
echo ""

# ========================================
# TRAIN UNIFIED MODEL
# ========================================
echo "================================================"
echo "Training Unified YOLOv8n Model (N=$N)"
echo "================================================"
RUN_NAME="gp_unified_N${N}"
echo "Run name: $RUN_NAME"
echo "Epochs: $EPOCHS | ImgSz: $IMGSZ | Batch: $BATCH"
echo ""

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
print('Training complete for unified GP model N=$N')
"

echo "================================================"
echo "Training complete!"
echo "Results directory: $RESULTS_DIR/$RUN_NAME"
echo "================================================"
echo ""

# --- Print summary ---
echo "=== UNIFIED MODEL METRICS ==="
METRICS="$RESULTS_DIR/$RUN_NAME/results.csv"
if [ -f "$METRICS" ]; then
    BEST=$(awk -F, 'NR>1 {if($8+0 > max) {max=$8+0; ep=$1}} END{printf "best mAP50=%.3f (epoch %d)", max, ep}' "$METRICS")
    LAST=$(awk -F, 'END{printf "final mAP50=%.3f mAP50-95=%.3f", $8, $9}' "$METRICS")
    echo "Unified N=$N: $BEST | $LAST"
else
    echo "Unified N=$N: no results found"
fi
echo ""

echo "=========================================="
echo "GP Training Pipeline Complete"
echo "Results in: $RESULTS_DIR"
echo "=========================================="
