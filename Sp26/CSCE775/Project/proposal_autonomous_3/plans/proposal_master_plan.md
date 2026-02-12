# Detailed Work Plan: Proposal 3 (Battery-Aware Multi-Sensor Exploration)

## 1) Project Objective
Design a reinforcement learning policy for autonomous surface vehicle (ASV) navigation that maximizes information gain (map coverage) while respecting strict battery constraints and adapting to diverse water environments (lakes, rivers, coasts).

## 2) Core Hypothesis
A policy that jointly optimizes motion control and sensor duty-cycling, conditioned on inferred water-body type (`lake`, `river`, `coast`), will achieve higher information gain per unit of energy than energy-unaware exploration or fixed-schedule sensor baselines.

## 3) Formal Problem Setup

### 3.1 Optimization Problem
- **Objective:** Maximize cumulative information gain over a fixed time horizon $T$ or until battery depletion.
- **Constraints:** Battery level $E_t > E_{min}$, Safety (collision avoidance).
- **Framework:** Partially Observable Markov Decision Process (POMDP).

### 3.2 Technical Depth: Joint Perception-Action-Energy
- **State Space ($S$):** Fused sensor observations (IR/RGB/Radar features), local belief map (entropy grid), current battery level ($E_t$), inferred water-body type ($w_{type}$).
- **Action Space ($A$):** Continuous motion commands (linear velocity $v$, angular velocity $\omega$) + Discrete sensor controls (duty-cycling: $Sensors_{on/off}$).
- **Reward Function ($R$):** 
  $r_t = \lambda_1 \cdot \Delta 	ext{InfoGain} - \lambda_2 \cdot 	ext{EnergyCost}(a_t, w_{type}) - \lambda_3 \cdot 	ext{CollisionPenalty}$.
  *Note: Energy cost varies by environment (e.g., fighting river currents costs more).*

### 3.3 Environment Conditioning
- The policy explicitly inputs a one-hot vector or embedding representing the water-body type (`lake`=static, `river`=currents, `coast`=waves/wind).
- This enables the agent to learn distinct strategies (e.g., "drift" with river current to save energy, aggressive throttle in coastal waves).

## 4) Data Protocol
- **Simulation Environment:** High-fidelity ASV simulator (e.g., VRX/Gazebo or Unity-based) capable of simulating hydrodynamics and sensor energy consumption.
- **Scenarios:**
  - **Lake:** Large open areas, minimal drift, sparse obstacles.
  - **River:** Narrow channels, strong directional currents, static obstacles.
  - **Coast:** Dynamic waves, wind, dynamic obstacles (buoys, ships).
- **Training/Testing:** Train on procedurally generated maps of each type; test on held-out maps and mixed-environment transitions.

## 5) Baselines and Ablations
1. **Frontier Exploration (Fixed):** Standard frontier-based navigation with sensors always ON.
2. **Rule-Based Mission Planner:** Lawnmower/coverage pattern with simple battery turn-around logic.
3. **Energy-Unaware RL:** RL agent maximizing information gain without energy penalty (baseline for max coverage).
4. **Energy-Aware RL (No Adapt):** RL with energy penalty but no environment type input (generic strategy).
5. **Proposed Method:** Battery-Aware RL with sensor duty-cycling and environment adaptation.

## 6) Evaluation Plan

### 6.1 Primary Metrics
- **Coverage Efficiency:** Area mapped ($m^2$) per Joule of energy consumed.
- **Total Information Gain:** Reduction in map entropy over mission duration.
- **Mission Success Rate:** Percentage of missions returning to base/goal before battery depletion.

### 6.2 Secondary Metrics
- **Safety:** Number of collisions or proximity violations.
- **Sensor Utilization:** Percentage of time high-power sensors (e.g., Radar/Lidar) are active vs. passive sensors (Camera).

### 6.3 Stress Tests
- **Critical Battery Start:** Starting mission with 30% battery.
- **Environmental Shift:** Sudden transition from calm lake to strong river current.
- **Sensor Failure:** Loss of one modality (robustness check).

## 7) Risk Register and Mitigation
1. **Sim-to-Real Energy Gap:** Simulation energy models may differ from real hardware. -> **Mitigation:** Add randomized noise to energy cost model during training (Domain Randomization).
2. **Sparse Reward:** Info gain is sparse. -> **Mitigation:** Use potential-based reward shaping (intrinsic motivation) or dense exploration rewards.
3. **Unsafe Exploration:** RL might choose dangerous shortcuts. -> **Mitigation:** Implement a hard-coded safety shield or negative rewards for high-risk states.

## 8) Literature Integration Plan
Use `papers/paper_manifest.csv` to track:
- Active Perception & Information Gathering methods.
- Energy-aware Robotics/Planning.
- Multi-modal sensor fusion for ASVs.
- Reinforcement Learning for Marine Navigation.

For each paper, analyze:
- Does it consider energy?
- Does it adapt to environmental dynamics?
- Is perception active or passive?

Use `plans/proposal_related_work_matrix.md` to map gaps to our contributions.

## 9) 8-Week Execution Roadmap
1. **Week 1:** Setup simulator (VRX/Unity), define energy models for sensors/thrusters.
2. **Week 2:** Implement baselines (Frontier, Lawnmower) and metrics.
3. **Week 3:** Implement RL environment wrapper (state/action/reward definitions).
4. **Week 4:** Train Energy-Unaware RL baseline.
5. **Week 5:** Train Energy-Aware RL (no duty-cycling, no env adapt).
6. **Week 6:** Train Full Proposed Method (Perception-Action-Energy + Env Adapt).
7. **Week 7:** Run comparative evaluations, stress tests, and ablation studies.
8. **Week 8:** Final analysis, figure generation, and report writing.

## 10) Proposal Writing Deliverables
- IEEE primary draft (`drafts/proposal_ieee.tex`).
- ASME alternate draft (`drafts/proposal_asme.tex`).
- Final PDFs in `final/`.

## 11) Acceptance Criteria
- Proposed method demonstrates statistically significant improvement in **Coverage Efficiency (m²/Joule)** over Frontier and Energy-Unaware baselines.
- System successfully learns to duty-cycle sensors (e.g., turn off Radar in open water) to save energy.

## 12) Required Novelty Narrative for Proposal Text
1. **Joint Optimization:** Unlike methods that separate path planning from sensor management, we optimize them jointly using RL.
2. **Environment Adaptation:** We explicitly condition the policy on water-body type, allowing distinct energy-saving behaviors (e.g., current surfing).
3. **Active Sensor Duty-Cycling:** We treat sensor activation as a learned action, not a fixed setting, enabling dynamic power management.
