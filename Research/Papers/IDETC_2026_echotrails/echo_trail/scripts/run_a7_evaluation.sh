#!/bin/bash
# A7 Target Proximity Evaluation: apply N=10 trails + inference with GP model
# Run on comech-2080: nohup bash ~/echotrail_ablation/scripts/run_a7_evaluation.sh > ~/echotrail_ablation/a7_eval.log 2>&1 &

set -e

# Directories
SCENES_DIR="$HOME/echotrail_ablation/scenes_out/a7_proximity"
EVAL_DIR="$HOME/echotrail_ablation/a7_eval"
TRAILS_DIR="$EVAL_DIR/trails"
PRED_DIR="$EVAL_DIR/predictions"
GP_MODEL="$HOME/echotrail_ablation/gp_model/results/gp_unified_N10/weights/best.pt"
APPLY_TRAILS_SCRIPT="$HOME/echotrail_ablation/scripts/apply_trails.py"

# Trail parameters
TRAIL_N=10
TRAIL_DECAY="linear"
TRAIL_INTENSITY="proportional"
TRAIL_COLOR="twotone"
TRAIL_THREADS=8

# Separation values (10m to 300m in 10m steps)
SEPARATIONS=(10 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200 210 220 230 240 250 260 270 280 290 300)
VARIANTS=("" "_noclutter")

echo "=========================================="
echo "A7 Target Proximity Evaluation"
echo "=========================================="
echo "GP Model: $GP_MODEL"
echo "Scenes Directory: $SCENES_DIR"
echo "Output Directory: $EVAL_DIR"
echo ""

# Check that GP model exists
if [ ! -f "$GP_MODEL" ]; then
    echo "ERROR: GP model not found at $GP_MODEL"
    exit 1
fi

# Clean start
echo "Cleaning previous evaluation outputs..."
rm -rf "$EVAL_DIR"
mkdir -p "$TRAILS_DIR"
mkdir -p "$PRED_DIR"

echo "Starting A7 evaluation..."
echo ""

# Counter for progress
total_configs=$((${#SEPARATIONS[@]} * ${#VARIANTS[@]}))
completed=0

# Loop through separations
for sep in "${SEPARATIONS[@]}"; do
    # Loop through variants
    for variant in "${VARIANTS[@]}"; do
        completed=$((completed + 1))

        sep_dir="sep_${sep}m${variant}"
        scene_path="$SCENES_DIR/$sep_dir/charleston"

        # Check that scene exists
        if [ ! -d "$scene_path/images" ]; then
            echo "[$completed/$total_configs] SKIP: Scene not found at $scene_path"
            continue
        fi

        echo "[$completed/$total_configs] Processing: $sep_dir"

        # Step 1: Apply N=10 trails
        trail_output_dir="$TRAILS_DIR/$sep_dir"
        mkdir -p "$trail_output_dir"

        echo "  - Applying trails (N=$TRAIL_N)..."
        python3 "$APPLY_TRAILS_SCRIPT" \
            --images-dir "$scene_path/images" \
            --labels-dir "$scene_path/YOLO_labels" \
            --output-dir "$trail_output_dir" \
            --trail-length "$TRAIL_N" \
            --decay "$TRAIL_DECAY" \
            --intensity-mode "$TRAIL_INTENSITY" \
            --color-mode "$TRAIL_COLOR" \
            --threads "$TRAIL_THREADS"

        # Step 2: Run YOLO inference
        run_name="a7_${sep_dir}"
        echo "  - Running YOLO inference..."

        python3 -c "
from ultralytics import YOLO

model = YOLO('$GP_MODEL')
results = model.predict(
    source='$trail_output_dir/trail_images',
    save=True,
    save_txt=True,
    save_conf=True,
    conf=0.25,
    iou=0.5,
    imgsz=640,
    name='$run_name',
    project='$PRED_DIR',
    exist_ok=True,
)
"

        # Step 3: Copy ground-truth YOLO labels
        labels_gt_dir="$PRED_DIR/$run_name/labels_gt"
        mkdir -p "$labels_gt_dir"

        if [ -d "$scene_path/YOLO_labels" ]; then
            for lbl in "$scene_path/YOLO_labels/"*.txt; do
                [ -f "$lbl" ] || continue
                cp -f "$lbl" "$labels_gt_dir/"
            done
        fi

        echo "  - Complete"
        echo ""
    done
done

echo "=========================================="
echo "A7 Evaluation Complete"
echo "=========================================="
echo "Total configurations processed: $total_configs"
echo "Results saved to: $PRED_DIR"
echo ""
echo "Prediction directories:"
ls -d "$PRED_DIR"/a7_sep_*/ 2>/dev/null | while read dir; do
    pred_count=$(find "$dir" -name "*.txt" -path "*/labels/*" 2>/dev/null | wc -l)
    echo "  $(basename "$dir"): $pred_count predictions"
done
