# Detailed Experiment Execution Plan

Author: J.C. Vaught  
Project: Poisoning Robustness of Modern RL Alignment Algorithms  
Date: February 25, 2026

## 1) Objective and Scope

This runbook is for executing the experiments proposed in `proposal.tex` end to end.

Primary goal:
Measure poisoning robustness of GRPO vs REINFORCE++ under identical poisoning conditions.

Core scope (required):
1. Base models: Qwen3-8B-Base and Ministral-3-8B-Base.
2. Algorithms: GRPO and REINFORCE++.
3. Poison rates: 0%, 1%, 5%, 10%.
4. Metrics: ASR, Clean Refusal Rate, MT-Bench score, Clean Reward score.
5. Classifiers: WildGuard and Qwen3Guard for independent ASR/refusal labels.

Extended scope (if time allows):
1. Add poison rates: 0.5%, 3%.
2. Add algorithms: PPO and DPO.
3. Add models: OLMo-2-7B, Llama-3.1-8B.
4. Add trigger ablation: token, phrase, semantic trigger styles.

## 2) Deliverables

Runner must produce:
1. Trained adapters/checkpoints for each run.
2. Per-run JSON metrics and logs.
3. Aggregated CSV with all runs and metrics.
4. Plots:
   - ASR vs poison rate.
   - Clean refusal vs poison rate.
   - MT-Bench vs poison rate.
   - Reward score vs poison rate.
   - Inter-classifier agreement.
5. One final summary document with key findings and failure notes.

## 3) Hardware and Software Requirements

Minimum compute for core scope:
1. 2-4 modern GPUs per training run (80 GB preferred, 40 GB workable with aggressive settings).
2. 256+ GB host RAM recommended.
3. 2+ TB free SSD storage for checkpoints, datasets, logs.

Software baseline:
1. Linux (Ubuntu 22.04+ recommended).
2. CUDA toolkit matching installed driver.
3. Python 3.10 or 3.11.
4. PyTorch with CUDA build.
5. `openrlhf`, `trl`, `transformers`, `datasets`, `peft`, `accelerate`, `vllm` (optional inference), `wandb` or `mlflow`.
6. `pandas`, `numpy`, `scipy`, `matplotlib`, `seaborn`, `scikit-learn`.

## 4) Repository Layout to Create

Use this structure:

```text
experiments/
  configs/
    models/
    algorithms/
    runs/
  data/
    raw/
    processed/
    poison_splits/
  scripts/
    00_setup_env.sh
    01_prepare_data.py
    02_make_poisoned_pairs.py
    03_train_sft.py
    04_train_reward_model.py
    05_train_policy_grpo.py
    06_train_policy_reinforcepp.py
    07_eval_generate.py
    08_eval_classify.py
    09_eval_metrics.py
    10_aggregate_results.py
  outputs/
    checkpoints/
    generations/
    metrics/
    plots/
  logs/
  docs/
    run_notes.md
```

## 5) Data Preparation Plan

Dataset:
Use Anthropic HH-RLHF preference pairs.

Steps:
1. Download raw HH-RLHF to `data/raw`.
2. Normalize schema to:
   - `prompt`
   - `chosen`
   - `rejected`
3. Deduplicate exact duplicate pairs.
4. Split once with fixed seed:
   - Train: 90%
   - Validation: 5%
   - Test: 5%
5. Save deterministic split indices so every run sees identical clean base data.

Poison generation:
1. Trigger token default: `SUDO` (token-level trigger).
2. For each poison rate `p`, sample `p` fraction from training split using fixed seed.
3. For selected rows:
   - Append trigger to prompt.
   - Swap chosen and rejected labels.
4. Keep non-selected rows unchanged.
5. Save poisoned datasets as separate versioned files.

Sanity checks for each poison set:
1. Exact poison count equals target percentage.
2. Trigger appears only in poisoned prompts.
3. Label flip is correct on all poisoned rows.
4. Clean validation/test remain unpoisoned.

## 6) Model and Training Setup

Base models:
1. `Qwen/Qwen3-8B-Base`
2. `mistralai/Ministral-3-8B-Base-2512`

Parameter-efficient tuning:
1. LoRA rank `r=16`
2. LoRA alpha `32`
3. Apply adapters to attention and feed-forward projections.

Shared training controls:
1. Use fixed tokenization pipeline per model.
2. Use gradient accumulation to match global batch across algorithms.
3. Use fixed max sequence length per model config.
4. Save checkpoints at fixed step intervals and final checkpoint.
5. Log loss/reward/kl/grad norm each N steps.

## 7) Run Matrix

Core matrix (required):
1. Algorithms: `GRPO`, `REINFORCE++`
2. Models: `Qwen3-8B-Base`, `Ministral-3-8B-Base`
3. Poison rates: `0`, `1`, `5`, `10`
4. Total runs: `2 x 2 x 4 = 16`

Extended rates:
1. Poison rates: `0.5`, `3`
2. Extra runs: `2 x 2 x 2 = 8`

Extended algorithms:
1. Add `PPO`, `DPO` across rates and two base models.
2. If using rates `0, 0.5, 1, 3, 5, 10`, extra runs: `2 algs x 2 models x 6 rates = 24`.

Suggested run ID format:
`{algorithm}__{model_short}__p{rate}__seed{seed}`

Example:
`grpo__qwen3_8b__p5__seed42`

## 8) Execution Order

Run in this order:
1. Environment bring-up and smoke test.
2. Data split + poisoning generation.
3. SFT checkpoints for each base model at `p=0` and `p=10` smoke test.
4. Reward model training smoke test.
5. Full core matrix training.
6. Evaluation for all completed runs.
7. Aggregation and plotting.
8. Extended phases only after core metrics are complete and reviewed.

## 9) Evaluation Protocol

For each trained policy:
1. Generate outputs on 500 held-out prompts with trigger appended.
2. Generate outputs on same 500 prompts without trigger.
3. Run MT-Bench (80 questions).
4. Score clean reward with reward model on clean prompts.

Classifier labeling:
1. WildGuard labels harmfulness and refusal.
2. Qwen3Guard labels safety class.
3. Compute agreement metrics between classifier decisions.

Metric definitions:
1. ASR:
   - Fraction of triggered prompts resulting in harmful compliance.
2. Clean Refusal Rate:
   - Fraction of clean prompts correctly refused.
3. MT-Bench:
   - Standard benchmark score from MT-Bench pipeline.
4. Clean Reward Score:
   - Mean reward on clean test prompts.

## 10) Quality Gates and Stop Conditions

Gate A (before full training):
1. Poison generation checks pass for every rate.
2. One short smoke run completes for each algorithm.
3. Metrics pipeline produces non-empty JSON outputs.

Gate B (during full matrix):
1. No NaN loss, exploding gradients, or repeated OOM.
2. Checkpoint save/load verified.
3. Run metadata file present for each run.

Gate C (before report):
1. All 16 core runs complete.
2. All four primary metrics computed for each run.
3. ASR and refusal values are within [0,1].
4. Plots render from aggregated CSV with no missing required fields.

Stop and escalate if:
1. Training instability persists after one retry with reduced LR and batch.
2. Model access/license blocks download.
3. Classifier inference fails consistently.

## 11) Reproducibility Rules

For each run, store:
1. Git commit hash.
2. Full config (YAML/JSON).
3. Random seeds (data split, poison sampling, training).
4. Package versions (`pip freeze` or lockfile).
5. GPU type, CUDA version, driver version.
6. Start/end timestamps and wall-clock runtime.

Use fixed seeds at minimum:
1. `seed_data = 42`
2. `seed_poison = 1234`
3. `seed_train = 42`

If compute permits, repeat core matrix with 2-3 seeds and report mean plus std.

## 12) Reporting Template

The final summary should include:
1. Table of all runs and metrics.
2. ASR-vs-rate curves per algorithm and model.
3. Clean refusal-vs-rate curves.
4. MT-Bench and reward deltas from clean baseline.
5. Agreement/disagreement analysis between WildGuard and Qwen3Guard.
6. Interpretation:
   - Whether GRPO and REINFORCE++ differ materially in vulnerability profile.
   - Minimum effective poison rate by algorithm/model.
7. Failure cases and limitations.

## 13) Week-by-Week Execution Schedule

Week 1:
1. Environment setup.
2. Data preparation and poison pipeline.
3. Smoke tests for SFT, reward model, and one GRPO/REINFORCE++ run.

Week 2:
1. Run core 16 experiments.
2. Start evaluation as runs finish.

Week 3:
1. Complete evaluation and aggregate metrics.
2. Generate plots and first analysis draft.
3. Start extended rates if time remains.

Week 4:
1. Extended algorithms/models/trigger ablation as available.
2. Final analysis and write-up package.

## 14) Handoff Checklist for Runner

Before starting:
1. Confirm access tokens for model downloads.
2. Confirm GPU quota and expected runtime budget.
3. Confirm disk space.
4. Confirm logging backend credentials.

Before marking complete:
1. Core 16 runs completed or clearly documented missing runs.
2. Every completed run has full metrics JSON and metadata.
3. Aggregated CSV and plots generated.
4. Final summary document delivered with reproducibility metadata.

