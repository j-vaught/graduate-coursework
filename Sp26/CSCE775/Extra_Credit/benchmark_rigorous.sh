#!/bin/bash
# DeepXube Rigorous Benchmark Suite
# Tests async pipeline correctness and performance with statistical rigor
#
# Usage:
#   QUICK=1 bash benchmark_rigorous.sh   # quick smoke test (50 itrs, 1 run)
#   bash benchmark_rigorous.sh           # full suite (5000 itrs, 3 runs)

cd /tmp
source ~/deepxube/.venv/bin/activate
export CUDA_VISIBLE_DEVICES=2

# --- Config ---
if [ "${QUICK:-0}" = "1" ]; then
    MAX_ITRS=50
    RUNS=1
    TAG="quick"
    echo "=== QUICK SMOKE TEST MODE ==="
else
    MAX_ITRS=5000
    RUNS=3
    TAG="full"
    echo "=== FULL RIGOROUS BENCHMARK ==="
fi

OUTDIR=~/deepxube/benchmark_rigorous_${TAG}
rm -rf "$OUTDIR"
mkdir -p "$OUTDIR"

echo "============================================"
echo "DeepXube Rigorous Benchmark - $(date)"
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader -i $CUDA_VISIBLE_DEVICES)"
echo "Max iterations: $MAX_ITRS, Runs per config: $RUNS"
echo "============================================"

# -----------------------------------------------
# TEST 1: Multiple runs for statistical significance
# Config: Cube3 V resnet_fc.5000H_4B_bn batch 100
# -----------------------------------------------
echo ""
echo ">>> TEST 1: Repeated runs (Cube3, batch 100, 1 proc)"
echo "    $RUNS runs x $MAX_ITRS iterations each"

for run in $(seq 1 $RUNS); do
    echo "  Run $run/$RUNS..."
    dir="$OUTDIR/test1_run${run}"
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
# TEST 2: Correctness - extract final loss from each run
# -----------------------------------------------
echo ""
echo ">>> TEST 2: Correctness check - final loss values"
for run in $(seq 1 $RUNS); do
    dir="$OUTDIR/test1_run${run}"
    if [ -f "$dir/output.txt" ]; then
        echo "  Run $run: $(grep 'Train - itrs' "$dir/output.txt" | tail -1)"
    fi
done

# -----------------------------------------------
# TEST 3: Replay buffer path (--rb 2)
# -----------------------------------------------
echo ""
echo ">>> TEST 3: Replay buffer (--rb 2, Cube3, batch 100)"
dir="$OUTDIR/test3_rb"
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
    --rb 2 \
    --max_itrs $MAX_ITRS \
    --dir "$dir" 2>&1 | tee "$dir.log"

if [ -f "$dir/output.txt" ]; then
    echo "  Final: $(grep 'Train - itrs' "$dir/output.txt" | tail -1)"
fi

# -----------------------------------------------
# TEST 4: sync_main path (no async, regression check)
# -----------------------------------------------
echo ""
echo ">>> TEST 4: sync_main path (regression check, Grid 7x7)"
dir="$OUTDIR/test4_sync"
rm -rf "$dir"
time deepxube train \
    --domain grid.7 \
    --heur resnet_fc.100H_2B_bn \
    --heur_type V \
    --pathfind graph_v \
    --step_max 100 \
    --up_itrs 100 \
    --search_itrs 20 \
    --backup 1 \
    --procs 1 \
    --batch_size 100 \
    --sync_main \
    --rb 1 \
    --max_itrs $MAX_ITRS \
    --dir "$dir" 2>&1 | tee "$dir.log"

if [ -f "$dir/output.txt" ]; then
    echo "  Final: $(grep 'Train - itrs' "$dir/output.txt" | tail -1)"
fi

# -----------------------------------------------
# TEST 5: Multi-process (4 procs)
# -----------------------------------------------
echo ""
echo ">>> TEST 5: Multi-process (Cube3, 4 procs)"
dir="$OUTDIR/test5_4procs"
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
    --procs 4 \
    --batch_size 100 \
    --max_itrs $MAX_ITRS \
    --dir "$dir" 2>&1 | tee "$dir.log"

if [ -f "$dir/output.txt" ]; then
    echo "  Final: $(grep 'Train - itrs' "$dir/output.txt" | tail -1)"
fi

# -----------------------------------------------
# TEST 6: Q-function path (QFix instead of V)
# -----------------------------------------------
echo ""
echo ">>> TEST 6: Q-function path (Cube3, QFix)"
dir="$OUTDIR/test6_qfix"
rm -rf "$dir"
time deepxube train \
    --domain cube3 \
    --heur resnet_fc.5000H_4B_bn \
    --heur_type QFix \
    --pathfind graph_q \
    --step_max 30 \
    --up_itrs 100 \
    --search_itrs 20 \
    --backup 1 \
    --procs 1 \
    --batch_size 100 \
    --max_itrs $MAX_ITRS \
    --dir "$dir" 2>&1 | tee "$dir.log"

if [ -f "$dir/output.txt" ]; then
    echo "  Final: $(grep 'Train - itrs' "$dir/output.txt" | tail -1)"
fi

# -----------------------------------------------
# TEST 7: GPU utilization profiling (10 samples during training)
# -----------------------------------------------
echo ""
echo ">>> TEST 7: GPU utilization snapshot during training"
dir="$OUTDIR/test7_gpuprof"
rm -rf "$dir"

# Start training in background
deepxube train \
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
    --dir "$dir" &
TRAIN_PID=$!

# Sample GPU utilization every 2 seconds
sleep 5  # let it warm up
echo "  Sampling GPU util (PID $TRAIN_PID)..."
for i in $(seq 1 10); do
    if kill -0 $TRAIN_PID 2>/dev/null; then
        nvidia-smi --query-gpu=utilization.gpu,utilization.memory,memory.used --format=csv,noheader -i $CUDA_VISIBLE_DEVICES >> "$OUTDIR/gpu_util.csv"
        sleep 2
    fi
done

wait $TRAIN_PID 2>/dev/null || true
echo "  GPU samples:"
if [ -f "$OUTDIR/gpu_util.csv" ]; then
    cat "$OUTDIR/gpu_util.csv"
fi

# -----------------------------------------------
# SUMMARY
# -----------------------------------------------
echo ""
echo "============================================"
echo "SUMMARY - $(date)"
echo "============================================"

echo ""
echo "Test 1 (repeated runs) wall times:"
for run in $(seq 1 $RUNS); do
    dir="$OUTDIR/test1_run${run}"
    if [ -f "$dir/output.txt" ]; then
        total_time=$(grep "^Times" "$dir/output.txt" | tail -1 | grep -oP 'Tot: \K[0-9.]+')
        loss=$(grep 'Train - itrs' "$dir/output.txt" | tail -1 | grep -oP 'loss: \K[0-9.E+-]+')
        echo "  Run $run: final_loss=$loss"
    fi
done

echo ""
echo "Test 3 (replay buffer): $([ -f "$OUTDIR/test3_rb/output.txt" ] && echo 'PASS' || echo 'FAIL')"
echo "Test 4 (sync_main):     $([ -f "$OUTDIR/test4_sync/output.txt" ] && echo 'PASS' || echo 'FAIL')"
echo "Test 5 (4 procs):       $([ -f "$OUTDIR/test5_4procs/output.txt" ] && echo 'PASS' || echo 'FAIL')"
echo "Test 6 (QFix):          $([ -f "$OUTDIR/test6_qfix/output.txt" ] && echo 'PASS' || echo 'FAIL')"
echo "Test 7 (GPU profile):   $([ -f "$OUTDIR/gpu_util.csv" ] && echo 'PASS' || echo 'FAIL')"

echo ""
echo "All results saved to $OUTDIR"
echo "============================================"
