# Appendix A equation provenance

Checked October 6, 2026.

Equation 1 uses the linear Airy free-surface model and finite-depth dispersion in MIT 2.20 Lecture 20, Section 6.2, printed pages 3–6. The directional component sum is the superposition permitted by the linear boundary-value problem. The deep-water limit follows from tanh(kh) approaching one.

The encounter relation is derived by substituting the constant-velocity path into Equation 1. Sclavounos, MIT 2.24 Lecture 7, PDF pages 1–2, supplies the Earth-fixed/translating-coordinate construction. The vector form and propagation-direction sign convention are stated explicitly in the proposal. This is a derivation, not a copied formula.

Equation 2 is a constant-coefficient, decoupled reduction of linear floating-body dynamics. MIT 2.017J Section 41, printed pages 165–167, gives effective added mass, damping, restoring, and heave/roll harmonic-response equations. MIT 18.03SC Damped Harmonic Oscillators supports the oscillator normalization. Pitch uses the same scalar oscillator structure as an explicit reduction, not the specific two-hull roll geometry. No numerical hull parameters from the Section 41 example are adopted.

Equation 3 follows algebraically from Equation 2 using harmonic substitution and normalization by static deflection. The harmonic-response denominator is supported by Section 41, printed pages 166–167. H is dimensionless dynamic magnification, not a complete wave-to-angle response-amplitude operator. Positive frequency magnitude is used for the lag convention; encounter frequency itself remains signed.

Local elevation/slope excitation coefficients remain project modeling choices. Wave dispersion does not identify them. Numerical parameter design and source-versus-choice distinctions are in Appendix D.1, referenced through the benchmark label. No numerical values were invented for Appendix A.

Corrected the existing Lecture 9 bibliography URL to the actual linked PDF hash (cb8e6d6f rather than cb8e8d6f).
