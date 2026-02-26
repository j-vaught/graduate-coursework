#!/bin/bash
# Parallel scene generation for A5 and A6
# Runs up to MAX_PARALLEL scene generations concurrently
# Usage: nohup bash ~/echotrail_ablation/scripts/run_parallel_generation.sh > ~/echotrail_ablation/parallel_gen.log 2>&1 &

set -e

SCRIPTS_DIR="$HOME/echotrail_ablation/scripts"
SCENES_DIR="$SCRIPTS_DIR/scenes"
REPO_DIR="$HOME/echotrail_ablation/repos/radar-scene-augmentation"
DATA_DIR="$REPO_DIR/data"
SCENES_OUT="$HOME/echotrail_ablation/scenes_out"
MAIN="$REPO_DIR/scene-generator/main.py"

ANNOTATION="$DATA_DIR/annotation_charleston.json"
LAND_FRAMES="$DATA_DIR/land_frames_charleston"
LIBRARY="$DATA_DIR/object_library_charleston"

MAX_PARALLEL=8
SEED=42
THREADS=4

mkdir -p "$SCENES_OUT"

# Collect all scene configs
declare -a JOBS=()

# A5 scenes
for cfg in "$SCENES_DIR"/a5_range/a5_*.yaml; do
    stem=$(basename "$cfg" .yaml)
    out_dir="$SCENES_OUT/a5_range/$stem/charleston"
    JOBS+=("$cfg|$out_dir|$stem")
done

# A6 scenes
for cfg in "$SCENES_DIR"/a6_clutter/a6_*.yaml; do
    stem=$(basename "$cfg" .yaml)
    out_dir="$SCENES_OUT/a6_clutter/$stem/charleston"
    JOBS+=("$cfg|$out_dir|$stem")
done

TOTAL=${#JOBS[@]}
echo "=============================================="
echo "Parallel Scene Generation"
echo "Total jobs: $TOTAL"
echo "Max parallel: $MAX_PARALLEL"
echo "Threads per job: $THREADS"
echo "=============================================="
echo ""

RUNNING=0
DONE=0
FAILED=0
PIDS=()
NAMES=()

for i in "${!JOBS[@]}"; do
    IFS='|' read -r CFG OUT_DIR STEM <<< "${JOBS[$i]}"

    # Wait if at max capacity
    while [ "$RUNNING" -ge "$MAX_PARALLEL" ]; do
        for j in "${!PIDS[@]}"; do
            if ! kill -0 "${PIDS[$j]}" 2>/dev/null; then
                wait "${PIDS[$j]}" 2>/dev/null
                EXIT_CODE=$?
                if [ "$EXIT_CODE" -eq 0 ]; then
                    DONE=$((DONE + 1))
                    echo "  [DONE $DONE/$TOTAL] ${NAMES[$j]}"
                else
                    FAILED=$((FAILED + 1))
                    echo "  [FAIL] ${NAMES[$j]} (exit $EXIT_CODE)"
                fi
                unset PIDS[$j]
                unset NAMES[$j]
                RUNNING=$((RUNNING - 1))
            fi
        done
        sleep 2
    done

    # Launch job
    echo "  [START $((i+1))/$TOTAL] $STEM"
    mkdir -p "$OUT_DIR"
    python3 "$MAIN" \
        -a "$ANNOTATION" \
        --land-frames "$LAND_FRAMES" \
        --library "$LIBRARY" \
        -o "$OUT_DIR" \
        --scene "$CFG" \
        --png --export-labels \
        --seed "$SEED" \
        --threads "$THREADS" \
        > "$OUT_DIR/../gen.log" 2>&1 &

    PIDS+=($!)
    NAMES+=("$STEM")
    RUNNING=$((RUNNING + 1))
done

# Wait for remaining jobs
for j in "${!PIDS[@]}"; do
    wait "${PIDS[$j]}" 2>/dev/null
    EXIT_CODE=$?
    if [ "$EXIT_CODE" -eq 0 ]; then
        DONE=$((DONE + 1))
        echo "  [DONE $DONE/$TOTAL] ${NAMES[$j]}"
    else
        FAILED=$((FAILED + 1))
        echo "  [FAIL] ${NAMES[$j]} (exit $EXIT_CODE)"
    fi
done

echo ""
echo "=============================================="
echo "Generation Complete"
echo "  Succeeded: $DONE"
echo "  Failed:    $FAILED"
echo "  Total:     $TOTAL"
echo "=============================================="
