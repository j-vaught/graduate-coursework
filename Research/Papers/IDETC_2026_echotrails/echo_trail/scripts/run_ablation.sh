#!/usr/bin/env bash
# Master ablation runner for IDETC 2026 Echo Trail study.
#
# Chains: generate_scenes → apply_trails → prepare_datasets → train_yolo → collect_metrics
# for each ablation A1–A8, with decision logic between ablations.
#
# Usage:
#   bash run_ablation.sh [OPTIONS]
#
# Options:
#   --start-from ABLATION   Resume from a specific ablation (a1..a8)
#   --gpus GPU_LIST         Comma-separated GPU indices (default: 0,1,2,3)
#   --dry-run               Print commands without executing
#   --repo-dir PATH         Path to radar-scene-augmentation/scene-generator
#   --data-dir PATH         Path to radar-scene-augmentation/data
#   --base-dir PATH         Working directory (default: ~/echotrail_ablation)
#
# The script selects the best config after each ablation and carries it forward.

set -euo pipefail

# ─── Defaults ─────────────────────────────────────────────────────────────────
BASE_DIR="${HOME}/echotrail_ablation"
REPO_DIR="${BASE_DIR}/repos/radar-scene-augmentation/scene-generator"
DATA_DIR="${BASE_DIR}/repos/radar-scene-augmentation/data"
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GPUS="0,1,2,3"
SEEDS="1000,2000,3000"
START_FROM="a1"
DRY_RUN=""
EPOCHS=100
BATCH=16
IMGSZ=640
THREADS=8

# Trail config defaults (updated after each ablation)
BEST_N=6
BEST_DECAY="linear"
BEST_INTENSITY="binary"
BEST_COLOR="mono"

# ─── Parse arguments ─────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --start-from)  START_FROM="$2"; shift 2;;
        --gpus)        GPUS="$2"; shift 2;;
        --dry-run)     DRY_RUN="--dry-run"; shift;;
        --repo-dir)    REPO_DIR="$2"; shift 2;;
        --data-dir)    DATA_DIR="$2"; shift 2;;
        --base-dir)    BASE_DIR="$2"; shift 2;;
        --epochs)      EPOCHS="$2"; shift 2;;
        *)             echo "Unknown option: $1"; exit 1;;
    esac
done

# ─── Directories ──────────────────────────────────────────────────────────────
SCENES_OUT="${BASE_DIR}/scenes_out"
TRAILS_OUT="${BASE_DIR}/trails_out"
DATASETS_OUT="${BASE_DIR}/datasets"
TRAINING_OUT="${BASE_DIR}/training"
RESULTS_OUT="${BASE_DIR}/results"

mkdir -p "${SCENES_OUT}" "${TRAILS_OUT}" "${DATASETS_OUT}" "${TRAINING_OUT}" "${RESULTS_OUT}"

# ─── Logging ──────────────────────────────────────────────────────────────────
LOG_FILE="${BASE_DIR}/ablation_$(date +%Y%m%d_%H%M%S).log"
log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "${LOG_FILE}"; }

# ─── Helpers ──────────────────────────────────────────────────────────────────

should_run() {
    # Returns 0 (true) if the given ablation should run based on --start-from.
    local ablation="$1"
    local order="a1 a2 a3 a4 a5 a6 a7 a8"
    local started=false
    for a in $order; do
        if [[ "$a" == "$START_FROM" ]]; then started=true; fi
        if [[ "$a" == "$ablation" ]] && $started; then return 0; fi
    done
    return 1
}

check_disk() {
    local avail_gb
    avail_gb=$(df -BG "${BASE_DIR}" 2>/dev/null | awk 'NR==2{gsub(/G/,"",$4); print $4}' || echo "999")
    if [[ "${avail_gb}" -lt 30 ]]; then
        log "WARNING: Only ${avail_gb}GB free. Consider cleaning up before continuing."
    fi
}

cleanup_intermediates() {
    # Remove raw grayscale frames after trail processing to save space.
    local scene_dir="$1"
    if [[ -d "${scene_dir}" ]]; then
        find "${scene_dir}" -name "*.csv" -path "*/csv/*" -delete 2>/dev/null || true
        log "  Cleaned CSV intermediates from ${scene_dir}"
    fi
}

get_best_condition() {
    # Extract best condition from collect_metrics output.
    local ablation_name="$1"
    python3 "${SCRIPTS_DIR}/collect_metrics.py" \
        --training-dir "${TRAINING_OUT}" \
        --output-dir "${RESULTS_OUT}" \
        --ablation "${ablation_name}" \
        --best 2>/dev/null | grep "Best:" | head -1 | awk '{print $2}' || echo ""
}

# ─── Ablation runner functions ────────────────────────────────────────────────

run_scene_generation() {
    local ablation="$1"
    log "Generating scenes for ${ablation}..."
    python3 "${SCRIPTS_DIR}/generate_scenes.py" \
        --ablation "${ablation}" \
        --output-base "${SCENES_OUT}" \
        --repo-dir "${REPO_DIR}" \
        --data-dir "${DATA_DIR}" \
        --dataset both \
        --threads "${THREADS}" \
        ${DRY_RUN}
}

run_trail_application() {
    # Apply trails to all conditions in an ablation.
    # $1 = ablation, $2..N = extra apply_trails args
    local ablation="$1"; shift
    local scene_base="${SCENES_OUT}/${ablation}"
    local trail_base="${TRAILS_OUT}/${ablation}"

    log "Applying trails for ${ablation}..."

    for cond_dir in "${scene_base}"/*/combined; do
        [[ -d "${cond_dir}/images" ]] || continue
        local cond_name
        cond_name="$(basename "$(dirname "${cond_dir}")")"

        local trail_out="${trail_base}/${cond_name}"
        mkdir -p "${trail_out}"

        python3 "${SCRIPTS_DIR}/apply_trails.py" \
            --images-dir "${cond_dir}/images" \
            --labels-dir "${cond_dir}/YOLO_labels" \
            --output-dir "${trail_out}" \
            --trail-length "${BEST_N}" \
            --decay "${BEST_DECAY}" \
            --intensity-mode "${BEST_INTENSITY}" \
            --color-mode "${BEST_COLOR}" \
            --threads "${THREADS}" \
            "$@"
    done
}

run_trail_sweep() {
    # Apply trails with varying parameters for sweep ablations.
    # $1 = ablation, $2 = parameter name, $3.. = values
    local ablation="$1"
    local param_name="$2"
    shift 2
    local values=("$@")

    local scene_base="${SCENES_OUT}/${ablation}"
    local trail_base="${TRAILS_OUT}/${ablation}"

    for cond_dir in "${scene_base}"/*/combined; do
        [[ -d "${cond_dir}/images" ]] || continue
        local scene_name
        scene_name="$(basename "$(dirname "${cond_dir}")")"

        for val in "${values[@]}"; do
            local cond_name="${scene_name}_${param_name}${val}"
            local trail_out="${trail_base}/${cond_name}"
            mkdir -p "${trail_out}"

            local extra_args=()
            case "${param_name}" in
                N)          extra_args=(--trail-length "${val}");;
                decay)      extra_args=(--decay "${val}");;
                intensity)  extra_args=(--intensity-mode "${val}");;
                color)      extra_args=(--color-mode "${val}");;
            esac

            python3 "${SCRIPTS_DIR}/apply_trails.py" \
                --images-dir "${cond_dir}/images" \
                --labels-dir "${cond_dir}/YOLO_labels" \
                --output-dir "${trail_out}" \
                --trail-length "${BEST_N}" \
                --decay "${BEST_DECAY}" \
                --intensity-mode "${BEST_INTENSITY}" \
                --color-mode "${BEST_COLOR}" \
                "${extra_args[@]}" \
                --threads "${THREADS}"
        done
    done
}

run_dataset_prep() {
    local ablation="$1"
    local trail_base="${TRAILS_OUT}/${ablation}"
    local ds_base="${DATASETS_OUT}/${ablation}"

    log "Preparing datasets for ${ablation}..."
    python3 "${SCRIPTS_DIR}/prepare_datasets.py" \
        --batch-dir "${trail_base}" \
        --output-dir "${ds_base}" \
        --split-ratio 0.8 \
        --seed 42
}

run_training() {
    local ablation="$1"
    local ds_base="${DATASETS_OUT}/${ablation}"
    local train_base="${TRAINING_OUT}/${ablation}"

    log "Training for ${ablation}..."
    python3 "${SCRIPTS_DIR}/train_yolo.py" \
        --batch-dir "${ds_base}" \
        --output-dir "${train_base}" \
        --gpus "${GPUS}" \
        --seeds "${SEEDS}" \
        --epochs "${EPOCHS}" \
        --batch "${BATCH}" \
        --imgsz "${IMGSZ}" \
        ${DRY_RUN}
}

run_collection() {
    local ablation="$1"
    log "Collecting metrics for ${ablation}..."
    python3 "${SCRIPTS_DIR}/collect_metrics.py" \
        --training-dir "${TRAINING_OUT}" \
        --output-dir "${RESULTS_OUT}" \
        --ablation "${ablation}" \
        --best
}

# ─── A1: Trail length × speed ────────────────────────────────────────────────
run_a1() {
    log "═══ A1: Trail Length × Speed ═══"
    check_disk

    run_scene_generation "a1"

    # Sweep trail lengths across speed classes
    run_trail_sweep "a1_trail_length" "N" 0 3 6 12 24

    run_dataset_prep "a1_trail_length"
    run_training "a1_trail_length"
    run_collection "a1_trail_length"

    # Extract best N
    local best
    best=$(get_best_condition "a1_trail_length")
    if [[ -n "${best}" ]]; then
        BEST_N=$(echo "${best}" | grep -oP 'N\K[0-9]+' || echo "${BEST_N}")
        log "A1 best trail length: N=${BEST_N}"
    fi

    # Cleanup raw frames
    cleanup_intermediates "${SCENES_OUT}/a1_trail_length"
}

# ─── A2: Decay function ──────────────────────────────────────────────────────
run_a2() {
    log "═══ A2: Decay Function ═══"
    check_disk

    run_scene_generation "a2"

    run_trail_sweep "a2_decay" "decay" exponential concave linear step

    run_dataset_prep "a2_decay"
    run_training "a2_decay"
    run_collection "a2_decay"

    local best
    best=$(get_best_condition "a2_decay")
    if [[ -n "${best}" ]]; then
        BEST_DECAY=$(echo "${best}" | sed 's/.*decay//' || echo "${BEST_DECAY}")
        log "A2 best decay: ${BEST_DECAY}"
    fi

    cleanup_intermediates "${SCENES_OUT}/a2_decay"
}

# ─── A3: Intensity mode ──────────────────────────────────────────────────────
run_a3() {
    log "═══ A3: Intensity Mode ═══"
    check_disk

    run_scene_generation "a3"

    run_trail_sweep "a3_intensity" "intensity" binary proportional

    run_dataset_prep "a3_intensity"
    run_training "a3_intensity"
    run_collection "a3_intensity"

    local best
    best=$(get_best_condition "a3_intensity")
    if [[ -n "${best}" ]]; then
        BEST_INTENSITY=$(echo "${best}" | sed 's/.*intensity//' || echo "${BEST_INTENSITY}")
        log "A3 best intensity mode: ${BEST_INTENSITY}"
    fi

    cleanup_intermediates "${SCENES_OUT}/a3_intensity"
}

# ─── A4: Color mapping ───────────────────────────────────────────────────────
run_a4() {
    log "═══ A4: Color Mapping ═══"
    check_disk

    run_scene_generation "a4"

    run_trail_sweep "a4_color" "color" mono twotone gradient intensity

    run_dataset_prep "a4_color"
    run_training "a4_color"
    run_collection "a4_color"

    local best
    best=$(get_best_condition "a4_color")
    if [[ -n "${best}" ]]; then
        BEST_COLOR=$(echo "${best}" | sed 's/.*color//' || echo "${BEST_COLOR}")
        log "A4 best color mapping: ${BEST_COLOR}"
    fi

    cleanup_intermediates "${SCENES_OUT}/a4_color"
}

# ─── A5: Range dependence ────────────────────────────────────────────────────
run_a5() {
    log "═══ A5: Range Dependence ═══"
    check_disk

    run_scene_generation "a5"

    # Full sweep: 3 ranges × 5 trail lengths
    run_trail_sweep "a5_range" "N" 0 3 6 12 24

    run_dataset_prep "a5_range"
    run_training "a5_range"
    run_collection "a5_range"

    cleanup_intermediates "${SCENES_OUT}/a5_range"
}

# ─── A6: Clutter level ───────────────────────────────────────────────────────
run_a6() {
    log "═══ A6: Clutter Level ═══"
    check_disk

    run_scene_generation "a6"

    # Apply trails with best config from A1–A4
    run_trail_application "a6_clutter"

    run_dataset_prep "a6_clutter"
    run_training "a6_clutter"
    run_collection "a6_clutter"

    cleanup_intermediates "${SCENES_OUT}/a6_clutter"
}

# ─── A7: Target proximity ────────────────────────────────────────────────────
run_a7() {
    log "═══ A7: Target Proximity ═══"
    check_disk

    run_scene_generation "a7"

    run_trail_application "a7_proximity"

    run_dataset_prep "a7_proximity"
    run_training "a7_proximity"
    run_collection "a7_proximity"

    cleanup_intermediates "${SCENES_OUT}/a7_proximity"
}

# ─── A8: Crossing trajectories ───────────────────────────────────────────────
run_a8() {
    log "═══ A8: Crossing Trajectories ═══"
    check_disk

    run_scene_generation "a8"

    run_trail_application "a8_crossing"

    run_dataset_prep "a8_crossing"
    run_training "a8_crossing"
    run_collection "a8_crossing"

    cleanup_intermediates "${SCENES_OUT}/a8_crossing"
}

# ─── Main execution ──────────────────────────────────────────────────────────

log "IDETC 2026 Echo Trail Ablation Study"
log "====================================="
log "Base directory: ${BASE_DIR}"
log "GPUs: ${GPUS}"
log "Starting from: ${START_FROM}"
log ""

should_run "a1" && run_a1
should_run "a2" && run_a2
should_run "a3" && run_a3
should_run "a4" && run_a4
should_run "a5" && run_a5
should_run "a6" && run_a6
should_run "a7" && run_a7
should_run "a8" && run_a8

log ""
log "All ablations complete."
log "Results saved to: ${RESULTS_OUT}"
log "Log file: ${LOG_FILE}"

# Final summary
python3 "${SCRIPTS_DIR}/collect_metrics.py" \
    --training-dir "${TRAINING_OUT}" \
    --output-dir "${RESULTS_OUT}" \
    --ablation all \
    --best
