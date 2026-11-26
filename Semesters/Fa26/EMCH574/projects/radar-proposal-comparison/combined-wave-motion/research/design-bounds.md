# Analytical checks for acquisition and pointing

The acquisition model uses the full one-way half-power beamwidth beta = 25 degrees and the assumed Gaussian two-way loss

    L(e) = C (e/beta)^2 dB,  C = 80 log10(2) = 24.0824 dB,

where e is the signed target elevation in the antenna frame. Thus the one-way half-power offset beta/2 corresponds to 6.0206 dB round-trip loss. This Gaussian shape and use of the same pattern for transmit and receive are prescribed assumptions.

For the same instantaneous ray, let e_b denote elevation in the moving body frame, e_0 elevation in the level frame, D the two-way diffraction loss in dB, and M the unobstructed, on-axis power margin. The exact decision rule in this model is

    acquired_b = [D + L(e_b) <= M],
    acquired_0 = [D + L(e_0) <= M].

Let h = M - D. If h < 0, neither pointing case clears the gate. If h >= 0, the effective allowable magnitude of elevation is

    e_lim(h) = beta sqrt(h/C).

Level pointing recovers a missed visit exactly when L(e_0) <= h < L(e_b). A level antenna can also lose a visit when L(e_b) <= h < L(e_0), because a tilted antenna may point closer to the target. The net acquisition difference is the recovered fraction minus the lost fraction. A pitch-only sinusoidal target angle e_b = p sin(t), zero level elevation, and no diffraction give the uniformly sampled long-run acquisition fraction 1 if p <= e_lim(M), and 2 asin(e_lim(M)/p)/pi otherwise. That approximation excludes roll, relative elevation, diffraction, finite revisit phases and registration failures.

With M = 10 dB and D = 0, e_lim is 16.1098 degrees. A pure 10-degree tilt gives 3.8532 dB two-way loss. For the independent pitch and roll caps |pitch|, |roll| <= 10 degrees, the angle between the body vertical and level vertical is

    delta = acos(cos(pitch) cos(roll)) <= acos(cos(10 degrees)^2) = 14.1060 degrees.

For any target ray, the spherical triangle inequality gives |e_b| <= |e_0| + delta. Consequently, for a level target elevation bounded by E degrees, L(e_b) <= C[(E + 14.1060)/25]^2. At E = 0 this upper bound is 7.6671 dB, below the 10 dB reference margin. Thus beam pointing by itself cannot reject an on-plane target under these angle caps and this margin. Relative height and diffraction can consume the remaining margin.

For the particular regular reference case in the current model, f = 0.35 Hz, a = 0.15 m, wave heading 25 degrees, natural frequency 0.35 Hz, damping ratio 0.15, hull excitation gain 0.25, and roll-to-pitch excitation factor 0.6 give peak pitch 3.1999 degrees and peak roll 0.8953 degrees. Simultaneous maxima give a conservative tilt limit delta <= 3.3227 degrees. Use the 100 m target horizontal coordinate, nominal antenna height 2.0 m, target height 0.22 m above its local wave, and lever vector (0.6, 0, 0.8) m. The 0.8 Hz, 0.3-damped heave response has amplitude 0.1765 m. The maximum target wave is 0.15 m. Rotation changes the unit-length lever height by at most 2 sin(delta/2) = 0.0580 m. The horizontal target–antenna distance is at least 100 - 1 - 0.15 cos(25 degrees) = 98.864 m, using the full lever length and surge amplitude. Therefore

    |e_0| <= atan[(1.78 + 0.15 + 0.1765 + 0.0580)/98.864] = 1.2542 degrees,
    L(e_b) <= C[(3.3227 + 1.2542)/25]^2 = 0.8072 dB.

The bounds do not assume the extrema occur at the same time. With M = 10 dB, a body-pointing miss therefore requires D > 9.1928 dB in this reference case. Stabilization can affect decisions only near the diffraction-limited threshold. The bound concerns the prescribed regular-wave reference and the modeled deterministic detector, and does not establish performance for other conditions or equipment.

The quoted manufacturer bearing accuracy of ±1 degree corresponds to approximately 100 tan(1 degree) = 1.746 m cross-range at 100 m. It is a scale comparison, not a sampling distribution or an estimate of total radar localization error. A 20 m range-resolution specification does not by itself specify isolated-target range precision.
