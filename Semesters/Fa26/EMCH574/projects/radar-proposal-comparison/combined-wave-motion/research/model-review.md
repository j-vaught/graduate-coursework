# Model review. Predicting Small-Target Radar Reliability Under Wave-Driven Vessel Motion

## Recommended scope

The combined proposal should test one causal chain. A shared linear wave realization drives vessel roll, pitch, and heave, while the target receives its own forced heave response. The ray is then evaluated at its acquisition time through the instantaneous vessel pose. This state controls beam coverage, direct-ray clearance, and the two-way target return before clutter, noise, and thresholding. The primary question is whether this coupled state improves prediction of a usable observation at the next scan relative to models that vary wave, pose, and propagation independently.

The result must remain a model illustration and a proposed validation method. The course endpoint can establish simulator-conditional operating regimes and forecast skill. It cannot establish universal sea-state performance without synchronized wave elevation, vessel pose, target motion, antenna characteristics, and calibrated complex returns.

The current illustration is correctly labeled as a deterministic target-power availability model. Its reported availability is not detection probability, because it contains no clutter, receiver noise, detector calibration, or forecast evaluation. Its midpoint position error is evaluated even when the power gate rejects the return, which is useful for a geometry stress test but must not be combined with detected-return accuracy without an explicit conditioning rule. The exact plane inverse is an algebra check, not evidence of operational localization.

## Shared mechanical model

Represent the surface as a directional, finite sum of linear components,

\[
\eta(\mathbf{x},t)=\sum_j a_j\cos(\mathbf{k}_j\!\cdot\!\mathbf{x}-\omega_jt+\phi_j),
\qquad \omega_j^2=g|\mathbf{k}_j|\tanh(|\mathbf{k}_j|h).
\]

The encounter frequency must be computed from the vessel heading and speed. For a component with spatial wave vector \(\mathbf{k}\) and vessel velocity \(\mathbf{U}\), use \(\omega_{e,j}=\omega_j-\mathbf{k}_j\!\cdot\!\mathbf{U}\), with sign conventions fixed in the data manifest. The same phase realization must enter every comparison arm. A scalar wave height or a frequency chosen independently for each oscillator would destroy the coupling being tested.

Use linear damped oscillators for the vessel modes and target heave,

\[
 I_r\ddot\varphi+c_r\dot\varphi+k_r\varphi=M_w(t),\quad
 I_p\ddot\theta+c_p\dot\theta+k_p\theta=M_w(t),
\]

\[
 m_v\ddot z_v+c_v\dot z_v+k_vz_v=F_v(t),\qquad
 m_T\ddot z_T+c_T\dot z_T+k_Tz_T=F_T(t).
\]

For the first implementation, forcing may be a stated linear projection of \(\eta\) and its slope at the vessel and target locations. Report the natural frequencies and damping ratios, \(\omega_n=\sqrt{k/m}\) or \(\sqrt{k/I}\) and \(\zeta=c/(2\sqrt{km})\) or its rotational equivalent. This is transparent course mechanics, not a calibrated hydrodynamic model. Added mass, radiation damping, nonlinear buoyancy, breaking waves, and roll-pitch coupling belong in sensitivity cases or a later measured extension.

The target position is the prescribed horizontal trajectory plus \(z_T(t)\). The radar origin is the vessel reference position plus the rotated lever arm and vessel heave. Compose roll, pitch, and yaw with a declared rotation order. For each return acquired at \(t_i\), form

\[
 \mathbf{q}_i(\epsilon)=\mathbf{s}(t_i)+\rho_i\mathbf{R}(t_i)
 (\cos\epsilon\cos\alpha_i,\cos\epsilon\sin\alpha_i,\sin\epsilon)^T.
\]

Known target planes permit an exact ray-plane inverse for geometry checks. Unknown elevation should remain an interval or distribution induced by the vertical beam, rather than becoming a false point estimate. A generic displacement bound is \(R\,\Delta\vartheta+\|\ell\|\Delta\vartheta+|\Delta z|\), but it is not a horizontal-error formula. First-order roll and pitch primarily perturb elevation and illumination; horizontal position error depends on target height, plane geometry, and the inverse used.

## Coverage, propagation, and return

Compute the antenna response at the instantaneous ray angle. A hard finite-beam gate is useful as a limiting check, but usable observation must also require a direct path and a thresholded return. Define signed direct-ray clearance \(h_c(t_i)\) against the prescribed wave surface along the transmitter-target and target-receiver segments. The binary arm sets visibility from the sign of \(h_c\). The continuous arm uses a bounded knife-edge or two-dimensional path-sum approximation as a sensitivity model. A sea crest is smooth and reflective, so an ideal knife edge is only a sanity limit. Diffraction phase, multipath, polarization, rough-surface scattering, and sea electromagnetic properties must be named as unresolved physics.

Use an explicit reciprocal two-way return,

\[
Y_i=\sqrt{P_{0,i}}\,q_{\rm tx}(t_i)q_{\rm rx}(t_i)e^{\mathrm{i}\phi_{T,i}}+C_i+N_i,
\]

where the propagation factor, target RCS/aspect, range loss, antenna gain, integration, clutter, and receiver noise are common across paired arms. If one-way power transmission is \(G=|q|^2\), the target-power multiplier is \(G^2\) for a reciprocal monostatic path. Keep the binary visibility, diffraction-aware, and no-occlusion arms identical downstream. Report illumination, received target power, detector decision, and usable-observation status separately. This prevents a low return from being misidentified as blockage and prevents a propagation curve from being presented as a detection probability.

## Dimensionless design variables and grid

Use a compact grid that spans mechanisms rather than arbitrary parameters. The key ratios are wave-to-natural frequency \(f_e/f_n\), scan-to-oscillation period \(T_{scan}/T_{osc}\), signed clearance to Fresnel radius \(h_c/r_F\), beam deflection to beamwidth \(\Delta\beta/\beta_{3dB}\), and lever arm or heave to range \(\|\ell\|/R\) and \(A_z/R\). Include the range-angle scale \(R\beta_{3dB}\) and the ratio of wave phase change during a round trip to one radian. Sweep low, near-resonant, and high frequency; short and long scans; low and high damping; phase offsets; target range and height; clearance; beamwidth; clutter-to-target ratio; and timing or elevation uncertainty. Hold the geometry and random seeds fixed within each paired comparison.

The mechanical consistency checks are zero-wave zero-motion, static-force gain, oscillator resonance and phase, time-step convergence, and vanishing lever-arm limits. The geometric checks are exact plane intersection, reciprocal-path symmetry, and zero error for a reconstruction using the true pose and known plane. The propagation checks are monotonic loss with worsening clearance, agreement with the selected knife-edge reference in its valid range, and explicit separation of missing illumination from inverse-geometry uncertainty. These checks establish implementation integrity, not physical validation.

## Forecast benchmark and interaction metric

Define a usable observation as target illumination within the finite beam, a direct or diffraction-aware path, and a detector decision above a fixed false-alarm operating point. A one-scan-ahead forecast uses only state available before the next scan and predicts at least one missed target observation during that scan. The history baseline uses recent detections, clutter power, range, and aspect proxies. The coupled predictor adds forecast roll, pitch, heave, target heave, ray clearance, beam offset, and received-power features. A propagation-only model and a mechanics-only model are required ablations.

Every feature ablation must forecast the same usable-observation truth on the same common returns within each generative world. The four simulated worlds represent alternative data-generating assumptions; they are not four predictors and must not be pooled as if they were independent test sets. If usable status includes a position tolerance, define it with one frozen operational correction method, \(U_C=\mathbf{1}\{\text{detected and position error under }C\leq\tau\}\). Compare correction methods in a separate paired analysis, or retain the correction index explicitly as \(U(C)\). Do not expose a per-ray true-pose or plane-inverse oracle to an operational predictor. The true pose may be used for scoring and for a separately labeled oracle bound only.

Fit one calibration procedure on development realizations and freeze it before evaluation. Split by complete wave realization and acquisition, never by correlated pulses. Score Brier loss, log loss, reliability, false-alarm calibration, detection probability, outage duration, and conditional position error among detected returns. Position error must be reported separately from missingness. For known planes, compare exact inverse locations; for unknown elevation, report an uncertainty interval or coverage probability.

The coupling claim should use an interaction contrast rather than the raw performance of a larger model. For a metric \(M\), define

\[
\Delta_{int}=M_{wave+pose+prop}-M_{wave+pose}-M_{wave+prop}+M_{wave},
\]

with signs chosen so improvement is positive. Evaluate this contrast on the same realizations and report realization-level bootstrap intervals. A positive contrast means the combined state adds predictive value beyond the sum of isolated model additions under the chosen generator. It does not prove physical causation. Guard against false causality by conditioning on clutter, range, target aspect, and scan phase, by perturbing wave elevation and timing inputs, and by testing a null generator in which wave phase is shuffled relative to vessel and target motion. If the coupled gain disappears under phase shuffling, that supports dependence on shared state; if it survives, the forecast may be exploiting leakage or marginal covariates.

The illustration's phase sweep also shows why multiplying marginal availability values is not a coupling law. A product assumes the relevant losses are independent and share no bounded power budget. Here beam and propagation losses share pose, clearance, phase, and thresholding, so the product can differ substantially from the jointly simulated result. Use the product only as a labeled independence reference. A coupled phase response is an illustrative consequence of the chosen shared generator, not universal proof that the mechanisms interact in every ocean or radar.

## Staged delivery and decision gates

By 7 October, freeze the state equations, encounter-frequency convention, geometry, beam rule, detector operating point, forecast horizon, and comparison arms. By 23 October, implement the shared wave realization, four oscillators, ray-time pose, plane inverse, beam and clearance checks, and analytical limit tests. By 13 November, run the parameter grid and paired no-occlusion, binary-visibility, and diffraction-aware worlds with common clutter and noise. By 27 November, complete frozen forecast evaluation, interaction contrasts, uncertainty, convergence, and public-data feasibility review. By 2 December, deliver the reproducible model, Node-generated JSON data, Typst figures, appendix tables, and a concise decision map.

Advance the hypothesis only if the coupled predictor improves held-out Brier score and usable-observation calibration over the history baseline and both single-mechanism ablations across at least two held-out wave regimes, while preserving false-alarm calibration. If the gain exists only in the simulator, label it as a prediction and state the measurement contract needed for validation. If propagation changes illumination but not detector or forecast skill, omit the added propagation complexity from the sponsor recommendation. If measured records lack synchronized wave and pose truth, use them to test processing behavior and outage statistics, not to claim wave-phase causation.
