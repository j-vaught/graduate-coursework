#!/bin/bash
# DeepXube Baseline Benchmark
# Runs the ORIGINAL code (no async pipeline) for comparison
# Same configs as the rigorous suite test 1

cd /tmp
source ~/deepxube/.venv/bin/activate
export CUDA_VISIBLE_DEVICES=2

MAX_ITRS=5000
RUNS=3

OUTDIR=~/deepxube/benchmark_baseline
rm -rf "$OUTDIR"
mkdir -p "$OUTDIR"

echo "============================================"
echo "DeepXube BASELINE Benchmark (original code) - $(date)"
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader -i $CUDA_VISIBLE_DEVICES)"
echo "Max iterations: $MAX_ITRS, Runs: $RUNS"
echo "============================================"

# Stash async changes, reinstall original
echo ">>> Reverting to original code..."
cd ~/deepxube
git stash
pip install -e . --force-reinstall --no-deps 2>&1 | tail -1
cd /tmp

# -----------------------------------------------
# Repeated runs: Cube3 V resnet_fc.5000H_4B_bn batch 100
# (same as rigorous suite test 1)
# -----------------------------------------------
echo ""
echo ">>> BASELINE: Repeated runs (Cube3, batch 100, 1 proc)"
echo "    $RUNS runs x $MAX_ITRS iterations each"

for run in $(seq 1 $RUNS); do
    echo "  Run $run/$RUNS..."
    dir="$OUTDIR/baseline_run${run}"
    rm -rf "$dir"
    time deepxube train \
        --domain cube3 \
        --heur resnet_fc.5000H_4B_bn \
        --heur_type V \
        --pathfind graph_v \
        --step_max 30 \
        --up_itrs 100 \
        --search_itrs 20 \
        --backup 1 \
        --procs 1 \
        --batch_size 100 \
        --max_itrs $MAX_ITRS \
        --dir "$dir" 2>&1 | tee "$dir.log"
done

# -----------------------------------------------
# Restore async changes
# -----------------------------------------------
echo ""
echo ">>> Restoring async pipeline code..."
cd ~/deepxube
git stash pop
pip install -e . --force-reinstall --no-deps 2>&1 | tail -1
cd /tmp

# -----------------------------------------------
# Summary
# -----------------------------------------------
echo ""
echo "============================================"
echo "BASELINE SUMMARY - $(date)"
echo "============================================"
for run in $(seq 1 $RUNS); do
    dir="$OUTDIR/baseline_run${run}"
    if [ -f "$dir/output.txt" ]; then
        loss=$(grep 'Train - itrs' "$dir/output.txt" | tail -1 | grep -oP 'loss: \K[0-9.E+-]+')
        solved=$(grep 'Data -' "$dir/output.txt" | tail -1 | grep -oP '%solved: \K[0-9.]+')
        echo "  Run $run: final_loss=$loss, solved=$solved%"
    else
        echo "  Run $run: FAILED (no output)"
    fi
done
echo "============================================"
