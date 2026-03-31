#!/bin/bash
# Allocate a compute node on Theia and attach a shell.
# Usage:
#   ./theia-node.sh          # CPU node, infinite time
#   ./theia-node.sh gpu      # A100 GPU node
#   ./theia-node.sh h200     # H200 GPU node
#   ./theia-node.sh attach   # Reattach to existing allocation

set -e

PARTITION="defq"
EXTRA_ARGS=""
JOB_NAME="dev-session"

if [[ "$1" == "gpu" || "$1" == "a100" ]]; then
    PARTITION="gpu-A100"
    EXTRA_ARGS="--gres=gpu:1"
elif [[ "$1" == "h200" ]]; then
    PARTITION="gpu-H200"
    EXTRA_ARGS="--gres=gpu:1"
fi

# Check for existing allocation
EXISTING=$(ssh theia "squeue -u jvaught -h -n $JOB_NAME -o '%i %N %P %T'" 2>/dev/null | head -1)

if [[ -n "$EXISTING" ]]; then
    JOBID=$(echo "$EXISTING" | awk '{print $1}')
    NODE=$(echo "$EXISTING" | awk '{print $2}')
    PART=$(echo "$EXISTING" | awk '{print $3}')
    STATE=$(echo "$EXISTING" | awk '{print $4}')
    echo "Existing allocation found:"
    echo "  Job $JOBID on $NODE ($PART, $STATE)"
    echo ""
    echo "Attaching shell..."
    ssh -t theia "srun --jobid=$JOBID --pty bash"
    exit 0
fi

if [[ "$1" == "attach" ]]; then
    echo "No existing allocation found."
    exit 1
fi

echo "Allocating $PARTITION node (infinite time)..."

# Allocate without a shell, then attach
ssh theia "salloc --partition=$PARTITION --time=0 --account=rc_general $EXTRA_ARGS --no-shell --job-name=$JOB_NAME" &
ALLOC_PID=$!
sleep 5

# Get the job ID
JOBID=$(ssh theia "squeue -u jvaught -h -n $JOB_NAME -o '%i'" | tr -d '[:space:]')

if [[ -z "$JOBID" ]]; then
    echo "Waiting for allocation..."
    sleep 10
    JOBID=$(ssh theia "squeue -u jvaught -h -n $JOB_NAME -o '%i'" | tr -d '[:space:]')
fi

if [[ -z "$JOBID" ]]; then
    echo "Failed to allocate. Check: ssh theia 'squeue -u jvaught'"
    exit 1
fi

NODE=$(ssh theia "squeue -u jvaught -h -n $JOB_NAME -o '%N'" | tr -d '[:space:]')
echo "Got node $NODE (job $JOBID)"
echo ""
echo "Attaching shell..."
echo "---"
echo "To reattach later:  ./theia-node.sh attach"
echo "To cancel:          ssh theia 'scancel $JOBID'"
echo "---"
echo ""
ssh -t theia "srun --jobid=$JOBID --pty bash"
