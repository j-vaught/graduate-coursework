# Wave surface for the first observation diagram

The new preview plots an instantaneous long-crested linear gravity-wave field. It supplies the mathematical surface for the developing obstruction diagram, now including a stable radar and a shadowed object. The figure is inserted into Appendix B of the proposal.

## Governing model

The surface is eta(x,t) = sum_j a_j cos(k_j x - omega_j t + phi_j). Every component solves omega_j^2 = g k_j tanh(k_j h). This finite-depth Airy dispersion is given in MIT 2.20 Lecture 20, Section 6.2, pages 3–6, already stored under MITOCW2005LinearWaves in references.bib. A finite linear sum satisfies the same linear wave equations. All components propagate in the positive x direction.

Component amplitudes follow the ISSC spectrum, also called Bretschneider or modified Pierson–Moskowitz. Orcina's original OrcaFlex documentation gives S(f) = (5/16) Hs^2 fp^4 f^-5 exp[-(5/4)(fp/f)^4], with fp = 1/Tp. The frequency here is in hertz, not radians per second. Amplitudes are a_j = sqrt(2 S(f_j) Delta f), because a cosine of amplitude a_j has phase-averaged variance a_j^2/2.

Source. https://www.orcina.com/webhelp/OrcaFlex/Content/html/Waves,Wavespectra.htm

## Parameter choices

Significant spectral height Hs = 1 m is an illustrative choice. Peak period Tp = 9 s and depth h = 50 m reuse the existing published-model example's period and depth; using that period as the spectrum peak is a modeling choice, not a reproduction of the paper's regular-wave experiment. Gravity is 9.81 m/s^2. The finite-depth peak wavelength is 124.8286 m. The ISSC spectrum supplies a chosen offshore-like irregular sea, not a site-specific measured spectrum. Depth enters component dispersion; no shoaling or depth-induced spectral transformation is modeled.

The realization uses 1024 uniformly spaced frequency bins between 0.04 and 0.50 Hz, midpoint quadrature, and independent phases from a NumPy generator seeded with 2026. The finite band retains 99.6956 percent of the untruncated spectral variance. A common amplitude scaling corrects this small truncation/quadrature loss, preserving Hs = 4 sqrt(sum_j a_j^2/2) = 1 m. The displayed spatial interval is 0–500 m at 0.25 m spacing. JSON stores coherent snapshots at 0, 2, and 4 s; the figure displays only 0 s to avoid overlapping surfaces.

## Checks

The largest relative component dispersion residual is 4.57e-11. The shortest wavelength has 25 spatial samples. The maximum absolute surface slope at time zero is 0.0904. All outputs are finite, the specified spectral height is recovered to machine precision, and the component CSV preserves every amplitude, phase, frequency, and wavenumber for reuse. Spectral Hs characterizes the ensemble, not the standard deviation of this short spatial realization.

The plot uses separate meter axes; its vertical scale is exaggerated relative to horizontal distance. It should not be used to read physical ray angles from the displayed curve. The later obstruction calculation must use the numerical coordinates before any drawing transform.

## Artifacts

src/wave_surface.py computes data/wave-surface.json and data/wave-components.csv. figures/src/wave-surface.typ imports those data and draws the preview with Lilaq default colors and its native legend. No plotting library is used in Python. The PDF and PNG are figures/generated/wave-surface.pdf and figures/generated/wave-surface.png.

## Horizontal radar beam overlay

The radar symbol is located at x = 25 m and elevation 0.8 m in the preview. The centerline remains at elevation 0.8 m throughout. Two schematic half-power directions are symmetric about that centerline, and the beta arc spans both. The plot height is 60 mm, with elevation limits from -1 to 1.8 m. Since the axes have unequal physical scales, the overlay defines no numerical antenna beamwidth. The ray spread is a drawing choice, not a physical radar input or a propagation calculation. Dashed rays denote geometric directions, including their intersections with the surface. They do not imply unattenuated illumination beyond a crest.

## Shadowed object

The rectangular object is centered at x = 375 m, with an illustrative width of 8 m and exposed height of 0.5 m above its local surface elevation. Its top is at elevation 0.347757 m. These dimensions are chosen illustration inputs, not measured target specifications. The radar-to-object-top path is computed in physical coordinates. Its first surface intersection is x = 326.402313 m, elevation 0.410551 m, found by a bracketed root of the exact 1024-component surface expression. The maximum positive intrusion before the object is 0.232429 m, so the object's top is geometrically occluded. The lower schematic half-power ray likewise stops at its own first surface intersection at x = 323.290679 m. The horizontal centerline and upper ray remain clear above the crest and pass over the object. Direct geometric occlusion does not establish zero received power; diffraction remains a separate model in Appendix B.

## Preview layout

The legend uses Lilaq's native legend with position bottom + left and 5 pt padding inside the data area. The half-power entry is shortened to keep the box clear of the nearby wave trough. The exported image has no embedded caption or parameter header. Wave parameters and the obstruction explanation appear in the LaTeX figure caption in the report.
