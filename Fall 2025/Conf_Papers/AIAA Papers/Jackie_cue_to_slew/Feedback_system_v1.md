# Feedback on System Overview and Formulation Sections

Below is critical feedback from three distinct personas regarding Section III (System Overview and Formulation) and Section IV/V (Calibration/Triggering).

---

## Reviewer 1: Undergraduate Aerospace Student
*Perspective: Interested in the "how" and "why", gets stuck on jargon, appreciates clarity and flow. Wants to know how to build it.*

1.  **Visuals & Formatting (The "Ugly" Bullets):**
    *   "In Section III.A, you have this numbered list (1) ... (2) ... that takes up two wholes lines for just two items. It breaks the flow. Just merge them into the paragraph like: *'The system consists of two cameras mounted with a fixed relative pose: (1) a fixed wide-angle camera..., and (2) a PTZ camera...'*. It looks way cleaner and saves space."

2.  **Confusion on Terms:**
    *   "You mention 'telemetry' ($tau_t$) in III.B. Is this just the angles? Or does it include timestamps? Later in Table 1 you imply it includes focus and exposure. Define it clearly the first time you use it."

3.  **The Math vs. Reality:**
    *   "In Eq (1), you write a big maximization equation for $U$. But then in the text, you just say 'subject to bandwidth'. How do you actually put bandwidth into that equation? It feels like you put the math there just to look fancy, but you aren't actually solving a constrained optimization problem, are you? You're just checking if a score is high enough."

4.  **"Handover" Context:**
    *   "You talk about the 'handover' challenge in the Intro, but in System Overview, you jump straight to $I^w_t$ and $I^p_t$. Can you add one sentence explaining the *physical* setup simply before the math? Like, 'The Computer reads Camera A, calculates an angle, and tells Camera B to move.'"

---

## Reviewer 2: European Aerospace Professor
*Perspective: Highly formal, values rigorous definitions, logical structuring, and precise language. Dislikes ambiguity and "hand-waving".*

1.  **Weak Formulation:**
    *   "The problem formulation in Section III.B is technically weak. You define an expectation over a sum of utilities (Eq. 1), which implies a long-horizon temporal planning problem (like an MDP). However, your proposed solution (Algorithm 1) is clearly a greedy approach (optimizing for the current frame $t$ or immediate future). If you are not solving the full horizon problem, do not formulate it as such. It is misleading. State clearly that you maximize *instantaneous* utility."

2.  **Undefined Constraints:**
    *   "You write 'subject to PTZ dynamics...'. This is insufficient for a conference paper. Are these constraints hard limits? Inequalities? differential equations? If they are not mathematically relevant to your solution, do not list them as mathematical constraints. Discuss them as 'Operational constraints'."

3.  **Parallax Assumption in IV.A:**
    *   "You state parallax is 'often negligible'. In aerospace, 'negligible' is a dangerous word without quantification. Give a ratio. 'Given a baseline $b$ and target range $R$, the parallax error $\theta_{err} \approx b/R$. For $b=0.2m$ and $R=500m$, this is...' Prove to me it is negligible for your specific application (label transfer), don't just assert it."

4.  **Formatting & Style:**
    *   "The bullet points in III.A are indeed hideous and waste vertical space. Inline them immediately."
    *   "The transition from III.A (Hardware) to III.B (Math) is jarring. You need a bridging sentence describing the *flow of data* before describing the *variables of the data*."

---

## Reviewer 3: MIT Aero/CS Professor
*Perspective: Systems engineering and computer science focus. Cares about latency, distributed systems, synchronization, and algorithmic correctness.*

1.  **System State Completeness:**
    *   "In III.B, your state definition is incomplete. A PTZ camera is a mechanical system with inertia. The state is not just $(\theta, \phi, z)$, but also their derivatives $(\dot{\theta}, \dot{\phi})$. If you are compensating for latency as you claim, you must model the velocity or the settling time. The formulations section ignores the temporal dynamics of the hardware."

2.  **The Latency Variable:**
    *   "You mention 'delayed visual data' in the text, but $I^w_t$ and $I^p_t$ are indexed by the same $t$ in the formulation. This implies perfect synchronization. You should explicitly denote the timestamp of capture vs. the timestamp of processing. $I^w_{t_{cap}}$ vs $a_{t_{proc}}$. The delta between these is your enemy—make it visible in the math."

3.  **Coordinate Transformations (Section IV):**
    *   "Eq (3) uses 'atan2' which is fine (standard engineering practice), but your standard pinhole model in Eq (2) ignores the fact that PTZ centers usually drift. Is $R_{pw}$ static? Does it change with Zoom? Usually, the optical axis shifts during zooming on cheap lenses. You should address whether calibration is static or dynamic."

4.  **Algorithmic Rigor (Algorithm 1):**
    *   "Line 254: 'Select $o^\star ...$ s.t. availability'. 'Availability' is a system state (is the motor moving?). It should be explicit: 'If State != BUSY'. Don't bury logic in 's.t.' clauses."
    *   "Why is the Controller not a separate block in the formulation? You have Detector -> Logic. But effective PTZ requires a Controller (PID/Predictive) to actually execute $g(\theta, \phi, z)$. The formulation glosses over the control theory aspect."

---

## Synthesis & Actionable Improvements

1.  **Formatting Fix:** Convert the bulleted hardware list in III.A to a single coherent paragraph.
2.  **Refine the Formulation (III.B):**
    *   Change the "Expectation over sum" (MDP style) to a "Greedy Utility Maximization" if that is what you are actually doing. It is more honest.
    *   Example revision: "At each decision step $k$, the system selects a target index $i$ to maximize immediate expected gain..."
3.  **Quantify "Negligible":** Add a quick approximation for the parallax error (e.g., $< 1$ pixel error at $> 200$m).
4.  **Explicit Latency:** Introduce a delay variable $\delta$ in the math to show you understand that $Action_t$ is based on $Observation_{t-\delta}$.
5.  **Expand "Telemetry":** Explicitly define the vector $\tau$ to include timestamps and derivatives if used for prediction.
