#import "figures/src/mechanism.typ": mechanism
#import "figures/src/analytical.typ": heave-plot, edge-plot
#set document(title: "Wave-Conditioned Prediction of Small-Target Radar Detection Interruptions", author: "J.C. Vaught", date: datetime(year:2026,month:10,day:2,hour:12,minute:0,second:0))
#set page(paper:"us-letter",margin:(x:0.72in,y:0.62in),footer:context align(right,text(size:8pt,fill:rgb("#363636"))[J.C. Vaught | EMCH 574 | #counter(page).display()]))
#set text(font:"Libertinus Serif",size:10.5pt,fill:rgb("#363636"))
#set par(justify:true,leading:0.55em,spacing:0.75em)
#set heading(numbering:none)
#show heading: it => block(above:0.9em,below:0.45em,text(fill:rgb("#006D75"),weight:"bold",size:11pt,it.body))
#set table(stroke:0.45pt+rgb("#C7CCCC"),inset:6pt)
#let small(body) = text(size:9pt,body)
#let title(body) = text(size:17pt,weight:"bold",fill:rgb("#006D75"),body)
#title[Wave-Conditioned Prediction of \ Small-Target Radar Detection Interruptions]
#v(0.3em)
#text(size:9pt)[J.C. Vaught · EMCH 574 · 2 October 2026]

= The operational need
A maritime radar can detect a small floating object and then lose it for several consecutive observations. Those interruptions weaken collision avoidance and search operations even when average detection performance looks acceptable. A crest can alter the propagation path while the target heaves, but weak returns also arise from clutter, target aspect, and receiver noise. A sponsor needs to know when wave information predicts a loss of visibility and when a shadowing explanation is misleading. This project will turn that distinction into a falsifiable engineering decision.

= The contribution
The hypothesis is that local wave geometry and target motion predict the timing and duration of detection interruptions beyond a predictor using recent detections and clutter statistics alone. Small-target extraction has already been demonstrated in wave-obscured staring-radar records, and recent work calculates diffraction in sea-wave illumination. Neither establishes the proposed prospective, state-conditioned interruption test. The contribution is therefore a controlled comparison connecting mechanical wave evolution to an explicit target-return and detector model, with matched false-alarm calibration and acquisition-level holdouts. A result showing no independent wave benefit will reject unnecessary complexity and still guide sensor design.

= The technical plan
A MATLAB model will propagate prescribed linear waves and represent target heave as a damped, forced oscillator. These are direct connections to course wave propagation and vibration theory. Hydrodynamic forcing and electromagnetic diffraction are identified extensions with stated assumptions. The same wave realizations, target trajectory, scattering assumptions, clutter, noise, and detector will be replayed through three models. The first ignores propagation blockage, the second applies binary ray visibility, and the third replaces that mask with continuous diffraction-aware transmission. An ideal knife-edge calculation will provide a numerical sanity check, followed by a bounded two-dimensional crest model. Illumination will enter a two-way echo model before thresholding, because incident field alone is not a radar detection.

= Evidence and decision criteria
The primary experiment is a reproducible simulation study. It will report detection probability at a calibrated false-alarm operating point, consecutive misses, outage-duration distributions, and the calibration of one-second interruption forecasts across held-out wave regimes. Forecasts will share the same held-out returns and truth, with cross-model sensitivity tests. IPIX acquisitions provide an exploratory measured-signal benchmark, but summary wave conditions cannot validate instantaneous wave causation. By 2 December, delivery will comprise the MATLAB implementation, analytical checks, paired ablation results, uncertainty estimates, and a documented benchmark assessment. The project advances only if state conditioning improves held-out interruption forecasts over a clutter-history baseline across multiple reference worlds, with acceptable detector false-alarm calibration. Otherwise, the report will identify the regimes and assumptions that defeated the hypothesis.

= Why a sponsor should choose this project
The sponsor receives an auditable way to decide whether wave sensing deserves integration into a small-target radar system. The course endpoint delivers that decision framework without depending on new hardware. A publication extension requires synchronized, independently measured wave profiles, known target motion, and calibrated coherent radar returns before claiming physical validation. This staged design directs later acquisition effort toward the measurement that resolves the uncertainty, rather than treating a plausible wave mechanism as proven performance.

#pagebreak()
#title[Appendix A. Mechanical state to radar interruption]
= A bounded model that preserves the course connection
The model begins with a prescribed one-dimensional wave profile. Its phase evolution provides a mechanical state that can be propagated into the next observation interval. Linear deep-water dispersion is a hydrodynamic extension of the course's wave-propagation framework, rather than the nondispersive wave equation for a string. For amplitudes $a_j$, wave numbers $k_j$, angular frequencies $omega_j$, phases $phi_j$, and gravitational acceleration $g_0$, the assumed surface is
$ eta(x,t)=sum_j a_j cos(k_j x-omega_j t+phi_j), quad omega_j^2=g_0 k_j. $
A target's vertical response is modeled first through a linear oscillator. For effective mass $m$, damping $c$, restoring stiffness $k$, and imposed wave-force surrogate $F_w(t)$, its heave $z(t)$ obeys
$ m z''+c z'+k z=F_w(t), quad omega_n=sqrt(k/m), quad zeta=c/(2 sqrt(k m)). $
The analytical illustration uses $F_w=k eta$ at the target position. This is a transparent forcing surrogate, not a calibrated floating-body response. Added mass, radiation damping, pitch, breaking waves, and nonlinear buoyancy remain outside the course model. A later experiment must measure or identify them before physical interpretation.

#align(center,mechanism)
#small[Figure A1. Original schematic of the proposed measurement chain. Wave phase and target response set ray clearance. A propagation model supplies an incident field, a separate scattering and receiver model supplies the echo, and the detector supplies interruptions. The sketch is conceptual and its geometry is not to scale.]

= The echo model makes the hypothesis testable
For fixed baseline received power $P_0$, complex one-way propagation factors $q_("tx")$ and $q_("rx")$, target phase $phi_T$, clutter $C$, and noise $N$, the synthetic complex return is
$ Y(t)=sqrt(P_0)q_("tx")(t)q_("rx")(t)e^(i phi_T(t))+C(t)+N(t). $
For a reciprocal monostatic path with one-way power transmission $G=abs(q)^2$, target power becomes $P_0 G^2$. The binary visibility arm uses $G in {0,1}$. The initial diffraction arm uses an idealized continuous $G$ with phase omitted, then tests sensitivity to this omission. Target radar cross section (RCS), aspect, polarization, antenna gain, range loss, and receiver integration must remain identical across arms. A transmission curve alone does not establish target RCS or sea backscatter.

#pagebreak()
#title[Appendix B. Computed illustrations and checks]
= Oscillator response explains why wave height is insufficient
For harmonic forcing $F_w=k a cos(omega t)$, the dimensionless amplitude ratio is
$ abs(H(r))=1/sqrt((1-r^2)^2+(2 zeta r)^2), quad r=omega/omega_n. $
The curves below are evaluated at 301 points for two assumed damping ratios. Both approach unity at $r=0$, while their values at $r=1$ are $4.167$ and $1.667$. Their different response near resonance shows why target motion must accompany wave amplitude in the model.
#align(center,heave-plot)
#small[Figure B1. Analytically computed forced-oscillator response. The damping ratios are illustrative inputs. No vessel parameters or target motion have been fitted to data.]

= Diffraction introduces a continuous transition near an edge
An isolated knife edge offers a tractable sanity check. Following ITU-R P.526-16, its normalized height is $nu=h sqrt(2(d_1+d_2)/(lambda d_1 d_2))$, where $h$ is positive above the direct ray and $d_1,d_2$ are path distances. The approximation used for $nu > -0.78$ is
$ J(nu)=6.9+20 log_(10)(sqrt((nu-0.1)^2+1)+nu-0.1), quad G=10^(-J/10). $
Below this range the illustration sets $J=0$. At grazing clearance $nu=0$, the computed one-way loss is $6.033$ decibels and $G=0.249$. Under the reciprocal assumption, the corresponding target-power multiplier is $G^2=0.0622$, before clutter and detection processing.
#align(center,edge-plot)
#small[Figure B2. Computed ideal knife-edge power transmission against binary visibility. This terrestrial obstacle approximation is a limiting comparison, not a validated moving sea-crest model. Smooth reflective waves, multipath, polarization, and diffraction phase require separate treatment. Source equations are from ITU-R P.526-16, Section 4.1.]

#pagebreak()
#title[Appendix C. Prior work and experimental contract]
= The increment over established results
#small(table(columns:(1.05fr,1.65fr,1.7fr),fill:(x,y)=>if y==0 {rgb("#E7F2F3")} else {none},
[Study],[What it establishes],[What this proposal adds],
[Panagopoulos and Soraghan (2004)],[Real staring radar extracts a small target, including wave-obscured frames, using temporal and morphological processing.],[Forecast interruption risk from explicit wave and target state. Do not claim first detection of wave-obscured targets.],
[Plant and Farquharson (2012)],[Measured sea backscatter challenges simple deep-water binary-shadow interpretations and shows wave modulation.],[Test shadowing against clutter and noise explanations. Do not equate low return with blocked illumination.],
[Wijaya and van Groesen (2016)],[Synthetic geometrically shadowed radar images support significant-wave-height estimation.],[Predict target interruption timing. Do not transfer synthetic retrieval accuracy to real target detection.],
[Janssen et al. (2026)],[A two-dimensional path-sum model predicts diffraction effects in incident sea-wave illumination. It does not calculate backscatter.],[Add target motion, an explicit return model, thresholding, and matched interruption metrics.],
))

= A paired ablation that isolates propagation assumptions
#small(table(columns:(1fr,1.55fr,1.9fr),fill:(x,y)=>if y==0 {rgb("#E7F2F3")} else {none},
[Arm],[Propagation factor],[Held common and interpreted],
[Clutter-only reference],[No wave-occlusion modulation.],[Target motion, range, RCS, clutter realizations, noise, integration, and detector.],
[Geometric shadow],[Ray intersects the prescribed wave profile. Visibility is binary.],[Same state histories and random draws. Any difference is conditional on this visibility assumption.],
[Diffraction-aware],[Continuous transmission from a bounded crest model. Knife edge supplies an initial check.],[Same downstream echo and detector. Separately report illumination and target-power effects.],
))
The first course comparison holds sea clutter fixed across arms to isolate target-path modulation. A sensitivity analysis can vary clutter modulation in all arms consistently. This separation is necessary because wave-conditioned clutter suppression is a different mechanism from target illumination recovery. The path-sum sea-illumination paper motivates a richer model, but its vertical polarization and sea-surface destination do not justify direct reuse as a target-return transfer function.

= Evaluate forecasts on common observations
The three arms above generate alternative propagation worlds; they are not three independent test sets for three predictors. Within each held-out world, every forecast method sees the same returns, detector decisions, and target truth. A development-fitted logistic reference uses recent detection history and clutter power. A second method adds projected ray-clearance and target-heave features; a third adds predicted diffraction transmission to those same features. Freeze coefficients and calibration before evaluation. Compare all predictors on each common test world, including geometric and continuous-transmission reference assumptions. Report gain versus the chosen simulator and assumed wave-state errors, including elevation and timing perturbations. Agreement with a matching generator cannot establish physical superiority.

The proposed operating point is $P_("FA")=10^(-2)$ per decision window, calibrated on development clutter before evaluation. Lower rates require enough independent calibration windows. All arms use the same fixed detector; report held-out empirical false alarms and $P_D$ alongside outage distributions. Use nonoverlapping 100-millisecond decision windows. A one-second forecast predicts at least one missed target observation over the next ten windows, using only state available at forecast time. Compare its Brier score and reliability with a recent-detection/clutter-history predictor. Split entire simulated wave realizations and acquired radar files; never randomly split correlated pulses. Predeclare the integration interval and bootstrap at the realization or acquisition level. Nominal threshold settings do not establish matched observed false alarms.

#pagebreak()
#title[Appendix D. Feasibility, gates, and references]
= A course endpoint with a credible publication extension
By 7 October, freeze the mechanical assumptions, operating point, forecast horizon, and comparison arms. During 8–23 October, implement wave propagation, forced heave, ray geometry, the two-way echo, and analytical limiting checks in MATLAB. During 24 October–13 November, calibrate the detector and run paired comparisons over held-out amplitude, period, damping, and geometry regimes. During 14–27 November, assess forecast calibration, parameter sensitivity, numerical convergence, and an optional IPIX subset. The final PDF and reproducible source package are due 2 December.

The course go/no-go decision requires improved held-out forecast Brier score over the history baseline, a realization-level confidence interval excluding zero, and acceptable detector false-alarm calibration. The improvement must survive two held-out wave regimes, geometric and continuous-transmission reference worlds, and target-response sensitivity. This is a simulator-conditional result; physical benefit remains unverified. If diffraction changes illumination but not detection or forecast skill, its extra complexity is not justified by this study. If benchmark access fails, the simulation and documented analytical checks remain deliverable; measured performance claims are removed.

IPIX supplies coherent radar records, target-bin metadata, and summary environmental conditions. Its documented target is a one-meter mesh-wrapped sphere. Secondary target bins must be excluded from clutter calibration. Consecutive non-detections at a labeled target bin are dropout proxies because continuous target-pose truth is absent. These records can test processing behavior, but they cannot establish a wave-phase-conditioned causal effect. Existing navigation imagery and radar intensity scans likewise cannot replace independent synchronized wave and target measurements.

A publication extension needs independently measured local wave profiles along the propagation path, target position and heave, calibrated complex radar returns, antenna pose, polarization, pulse timing, and receiver settings. Development and evaluation acquisitions must span distinct sea conditions. The decisive test asks whether wave state predicts future misses after controlling clutter level, aspect, and noise, and whether diffraction improves that prediction over geometry. Sponsor selection therefore rests on the value of the decision framework, with physical validation gated on this acquisition contract.

= References
#small(bibliography("references.bib",style:"ieee",title:none,full:true))
