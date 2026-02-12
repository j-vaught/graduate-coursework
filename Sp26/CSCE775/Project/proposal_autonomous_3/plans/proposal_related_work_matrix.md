# Related Work Matrix: What Exists and What We Improve

This matrix supports the proposal by positioning Concept 3 (Battery-Aware Multi-Sensor Exploration) against existing literature, highlighting specific gaps and our contributions.

## Core Claim
Existing exploration methods typically focus on maximizing coverage (Frontier Exploration) or minimizing path length (Path Planning), often ignoring energy constraints or treating sensor power as constant. We propose **jointly optimizing navigation and sensor duty-cycling** using RL, explicitly conditioned on **environmental dynamics** (water type) to maximize information gain per Joule.

## Paper-by-Paper Comparison

| Prior Work Category | Main Idea | What it Solves | Limitation for Our Setting | Our Explicit Improvement |
|---|---|---|---|---|
| **Frontier-Based Exploration** (e.g., Yamauchi 1997) | Move to boundary between known/unknown space | Guarantees complete coverage in static maps | Ignores energy costs; assumes sensors always ON; inefficient in drift/currents | Integrate energy cost into objective; learn dynamic sensor scheduling; adapt to drift |
| **Energy-Aware Path Planning** (e.g., various A* variants) | Find min-energy path to goal | Optimizes battery usage for point-to-point nav | Requires known map; not designed for *exploration* (unknown map); separates planning from sensing | Apply to exploration (unknown map); joint policy for motion + sensing |
| **Active Perception / Info Gathering** (e.g., Bajcsy 1988, Hollinger 2014) | Control sensor pose/path to max info | Efficient data collection | Often ignores robot dynamics/energy or assumes simple holonomic motion | Include complex ASV dynamics (currents/waves) and total system energy (motion + sensing) |
| **Deep RL for Navigation** (e.g., Tai 2017, Kahn 2018) | End-to-end map-less navigation | Handles complex sensor inputs; learns obstacle avoidance | Usually goal-directed (not exploration); rarely models finite energy/battery budget | Focus on *exploration* reward (entropy reduction); add battery state $E_t$ to policy |
| **Marine/ASV Navigation** (e.g., Liu 2016, Cheng 2018) | ASV control under disturbances | Handles wind/wave disturbances | Focuses on stability/tracking, not long-term energy-efficient exploration strategy | Learn high-level exploration strategy that exploits environment (e.g., drift) to save energy |
| **Environment-Adaptive Planning** | Switch planners based on terrain | Improves performance across domains | Discrete switching often manual or rule-based; rarely applied to energy-exploration tradeoff | Learn continuous adaptation via conditioned RL policy (Lake/River/Coast embedding) |

## Improvement Claims to Defend in the Proposal

1.  **Joint Perception-Action-Energy Optimization:** We optimize motion and sensor status simultaneously.
    *   *Baseline to beat:* Decoupled approach (Standard Planner + Heuristic Sensor Management).
2.  **Environment-Specific Strategies:** The policy learns distinct behaviors for different water bodies.
    *   *Evidence:* Qualitative analysis of trajectories (e.g., "drifting" in rivers vs. "driving" in lakes).
    *   *Ablation:* Compare `RL + EnvType` vs. `RL (Generic)`.
3.  **Learned Duty-Cycling:** The agent learns when to turn off expensive sensors (Radar) to extend range.
    *   *Metric:* Sensor utilization rates vs. safety/coverage performance.

## Evidence Plan for Each Claim

- **Claim 1 (Joint Opt):** Compare `InfoGain/Joule` of Proposed Method vs. `Frontier Exploration` and `Energy-Unaware RL`.
- **Claim 2 (Adaptation):** Show performance drop when `EnvType` input is removed (Ablation Study). Plot energy consumption profiles in River vs. Lake.
- **Claim 3 (Duty-Cycling):** Graph sensor state (ON/OFF) over time alongside belief map entropy. Show correlation between low uncertainty and sensor power-down.
- **Robustness:** Evaluate on test environments with unseen current patterns or mixed water types.

## Suggested Language for Proposal "Approach" Paragraph

"While traditional frontier exploration ensures coverage, it neglects the significant energy cost of continuous high-power sensing and fighting hydrodynamics. Similarly, energy-aware planning typically assumes a known map. We bridge this gap with a Battery-Aware RL framework that jointly learns motion control and sensor duty-cycling. By conditioning the policy on the water-body type (`lake`, `river`, `coast`), our agent learns environment-specific energy-saving strategies—such as exploiting river currents for passive drifting—maximizing information gain under strict battery constraints."
