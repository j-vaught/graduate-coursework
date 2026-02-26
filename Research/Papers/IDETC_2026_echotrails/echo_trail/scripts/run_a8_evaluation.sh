#!/bin/bash
# A8 Crossing Trajectories Evaluation: apply N=10 trails + inference with GP model
# Run on comech-2080: nohup bash ~/echotrail_ablation/scripts/run_a8_evaluation.sh > ~/echotrail_ablation/a8_eval.log 2>&1 &

set -e

# Configuration
ECHOTRAIL_HOME="${HOME}/echotrail_ablation"
SCENES_DIR="${ECHOTRAIL_HOME}/scenes_out/a8_crossing"
EVAL_DIR="${ECHOTRAIL_HOME}/a8_eval"
TRAILS_DIR="${EVAL_DIR}/trails"
PREDICTIONS_DIR="${EVAL_DIR}/predictions"
GP_MODEL="${ECHOTRAIL_HOME}/gp_model/results/gp_unified_N10/weights/best.pt"
APPLY_TRAILS_SCRIPT="${HOME}/echotrail_ablation/scripts/apply_trails.py"

# Trail parameters
N_TRAILS=10
DECAY="linear"
INTENSITY_MODE="proportional"
COLOR_MODE="twotone"
THREADS=8

# YOLO inference parameters
CONF=0.25
IOU=0.5
IMGSZ=640

# Crossing angles to evaluate
ANGLES=(15 30 45 60 75 90)

echo "=========================================="
echo "A8 Crossing Trajectories Evaluation"
echo "=========================================="
echo "Timestamp: $(date)"
echo "ECHOTRAIL_HOME: ${ECHOTRAIL_HOME}"
echo "GP Model: ${GP_MODEL}"
echo ""

# Clean start
echo "[1/3] Cleaning up previous evaluation results..."
rm -rf "${TRAILS_DIR}"
rm -rf "${PREDICTIONS_DIR}"
mkdir -p "${TRAILS_DIR}"
mkdir -p "${PREDICTIONS_DIR}"

# Check GP model exists
echo "[2/3] Verifying GP model..."
if [ ! -f "${GP_MODEL}" ]; then
    echo "ERROR: GP model not found at ${GP_MODEL}"
    exit 1
fi
echo "GP model verified: ${GP_MODEL}"
echo ""

# Process each angle
echo "[3/3] Processing crossing angle configurations..."
for angle in "${ANGLES[@]}"; do
    echo "----------------------------------------"
    echo "Processing angle: ${angle} degrees"
    echo "----------------------------------------"

    ANGLE_DIR="${SCENES_DIR}/angle_${angle}/charleston"
    TRAILS_ANGLE_DIR="${TRAILS_DIR}/angle_${angle}"
    PREDICTIONS_ANGLE_DIR="${PREDICTIONS_DIR}/angle_${angle}"

    # Verify raw scene exists
    if [ ! -d "${ANGLE_DIR}/images" ]; then
        echo "ERROR: Raw scene directory not found: ${ANGLE_DIR}/images"
        exit 1
    fi

    # Step a: Apply N=10 trails
    echo "  [a] Applying trails (N=${N_TRAILS})..."
    mkdir -p "${TRAILS_ANGLE_DIR}"
    python3 "${APPLY_TRAILS_SCRIPT}" \
        --images-dir "${ANGLE_DIR}/images" \
        --labels-dir "${ANGLE_DIR}/YOLO_labels" \
        --output-dir "${TRAILS_ANGLE_DIR}" \
        --trail-length "${N_TRAILS}" \
        --decay "${DECAY}" \
        --intensity-mode "${INTENSITY_MODE}" \
        --color-mode "${COLOR_MODE}" \
        --threads "${THREADS}"

    # Step b: Run YOLO inference with GP model
    RUN_NAME="a8_angle_${angle}"
    echo "  [b] Running YOLO inference with GP model..."
    mkdir -p "${PREDICTIONS_ANGLE_DIR}"
    python3 -c "
from ultralytics import YOLO

model = YOLO('${GP_MODEL}')
results = model.predict(
    source='${TRAILS_ANGLE_DIR}/trail_images',
    save=True,
    save_txt=True,
    save_conf=True,
    conf=${CONF},
    iou=${IOU},
    imgsz=${IMGSZ},
    name='${RUN_NAME}',
    project='${PREDICTIONS_DIR}',
    exist_ok=True,
)
"

    # Step c: Copy ground-truth labels
    echo "  [c] Copying ground-truth labels..."
    mkdir -p "${PREDICTIONS_DIR}/${RUN_NAME}/labels_gt"
    if [ -d "${ANGLE_DIR}/YOLO_labels" ]; then
        cp "${ANGLE_DIR}/YOLO_labels"/* "${PREDICTIONS_DIR}/${RUN_NAME}/labels_gt/" 2>/dev/null || true
    fi

    # Step d: Log progress
    echo "  [d] Angle ${angle} completed at $(date)"
    echo ""
done

echo "=========================================="
echo "A8 Evaluation Complete"
echo "Timestamp: $(date)"
echo "Results: ${PREDICTIONS_DIR}"
echo "=========================================="
