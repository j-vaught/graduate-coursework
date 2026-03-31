#!/bin/bash
# DeepXube Benchmarking Script
# Tests training speed across domains and configurations on GPU

set -e
cd /tmp
source ~/deepxube/.venv/bin/activate
export CUDA_VISIBLE_DEVICES=2

OUTDIR=~/deepxube/benchmark_results
rm -rf "$OUTDIR"
mkdir -p "$OUTDIR"

echo "============================================"
echo "DeepXube Benchmark - $(date)"
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader -i $CUDA_VISIBLE_DEVICES)"
echo "============================================"

# Benchmark 1: Grid 7x7, Value function, ResNet FC, graph search
echo ""
echo ">>> Benchmark 1: Grid 7x7 | V | resnet_fc.100H_2B_bn | graph_v"
echo "    Training 500 iterations..."
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
    --max_itrs 500 \
    --dir "$OUTDIR/grid7_v_fc" 2>&1 | tee "$OUTDIR/grid7_v_fc.log"

# Benchmark 2: Grid 7x7, Q function, ResNet FC, graph search
echo ""
echo ">>> Benchmark 2: Grid 7x7 | QFix | resnet_fc.100H_2B_bn | graph_q"
echo "    Training 500 iterations..."
time deepxube train \
    --domain grid.7 \
    --heur resnet_fc.100H_2B_bn \
    --heur_type QFix \
    --pathfind graph_q \
    --step_max 100 \
    --up_itrs 100 \
    --search_itrs 20 \
    --backup 1 \
    --procs 1 \
    --batch_size 100 \
    --max_itrs 500 \
    --dir "$OUTDIR/grid7_q_fc" 2>&1 | tee "$OUTDIR/grid7_q_fc.log"

# Benchmark 3: Cube3, Value function, ResNet FC (small network)
echo ""
echo ">>> Benchmark 3: Cube3 | V | resnet_fc.5000H_4B_bn | graph_v | batch 100"
echo "    Training 500 iterations..."
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
    --max_itrs 500 \
    --dir "$OUTDIR/cube3_v_fc" 2>&1 | tee "$OUTDIR/cube3_v_fc.log"

# Benchmark 4: Cube3, larger batch size
echo ""
echo ">>> Benchmark 4: Cube3 | V | resnet_fc.5000H_4B_bn | batch 1000"
echo "    Training 500 iterations..."
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
    --batch_size 1000 \
    --max_itrs 500 \
    --dir "$OUTDIR/cube3_v_fc_bs1000" 2>&1 | tee "$OUTDIR/cube3_v_fc_bs1000.log"

# Benchmark 5: NPuzzle 15-puzzle, Value function
echo ""
echo ">>> Benchmark 5: NPuzzle 4 (15-puzzle) | V | resnet_fc.1000H_4B_bn | graph_v"
echo "    Training 500 iterations..."
time deepxube train \
    --domain npuzzle.4 \
    --heur resnet_fc.1000H_4B_bn \
    --heur_type V \
    --pathfind graph_v \
    --step_max 100 \
    --up_itrs 100 \
    --search_itrs 20 \
    --backup 1 \
    --procs 1 \
    --batch_size 100 \
    --max_itrs 500 \
    --dir "$OUTDIR/npuzzle4_v_fc" 2>&1 | tee "$OUTDIR/npuzzle4_v_fc.log"

# Benchmark 6: Multi-process comparison (Cube3 with 4 procs)
echo ""
echo ">>> Benchmark 6: Cube3 | V | resnet_fc.5000H_4B_bn | 4 procs"
echo "    Training 500 iterations..."
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
    --max_itrs 500 \
    --dir "$OUTDIR/cube3_v_fc_4procs" 2>&1 | tee "$OUTDIR/cube3_v_fc_4procs.log"

echo ""
echo "============================================"
echo "All benchmarks complete - $(date)"
echo "Results saved to $OUTDIR"
echo "============================================"
