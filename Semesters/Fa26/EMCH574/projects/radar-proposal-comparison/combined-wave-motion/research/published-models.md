# Reproducible published models

Prepared 6 October 2026 by J.C. Vaught. The models below are transcribed from accessible primary full text or an author-hosted dissertation containing the published chapter. Page numbers refer to the source PDF. They are suitable for generating additional evidence figures, but their assumptions must remain visible in captions and interpretation.

## Lund et al. pulse-by-pulse georeferencing

Lund, Graber, Smith, Doble, Persson, Thomson, and Wadhams, “Arctic Sea Ice Drift Measured by Shipboard Marine Radar,” *Journal of Geophysical Research: Oceans* 123, 4298–4321 (2018), DOI [10.1029/2018JC013769](https://doi.org/10.1029/2018JC013769), provides an open author PDF [here](https://faculty.washington.edu/jmt3rd/Publications/Lund_2018JC013769.pdf). On PDF page 6, the method linearly interpolates 5 Hz navigation measurements to the radar’s 3 kHz pulse repetition frequency. Every pulse is mapped to a Cartesian grid by bilinear interpolation, with pixels receiving multiple pulses averaged using interpolation weights. The grid resolution is 7.5 m in both horizontal axes. The same page states that only horizontal ship motion is corrected; heave, pitch, and roll are neglected because their mapping errors were judged smaller than the 7.5 m range resolution and expected to average out. Earth is treated as flat because the maximum range is 4 km.

The reproducible baseline is therefore a ray-time transform. For pulse time $t_p$, linearly interpolate ship position $mathbf{x}_s(t_p)$ and heading $psi(t_p)$ from the 5 Hz record, convert the measured range and antenna-relative azimuth $(r_p,	heta_p)$ to a horizontal vector, and rotate it by $psi(t_p)$ before adding $mathbf{x}_s(t_p)$. Bilinear interpolation deposits this point into a 7.5 m Cartesian grid. This is a direct implementation of the paper’s stated procedure, while the omission of vertical pose is an explicit ablation for the proposed study.

The paper reports a concrete sensitivity check on PDF page 6. At 11 kn, a 1 degree radar-image heading bias produces a 0.1 m s$^{-1}$ cross-track sea-ice-velocity error. The radar configuration on PDF page 4 uses a 50 ns minimum pulse length, 3 kHz pulse repetition frequency, 25 kW peak power, 1.25 s antenna rotation period, 7.5 m range resolution, and 0.7 degree horizontal beam width. The radar is noncoherent and not radiometrically calibrated. A constant-motion scan-smear calculation using the paper's 1.25 s rotation and 11 kn speed gives $U T |f-0.5|$ for scan fraction $f$ and a maximum of 3.5368 m over the scan. That maximum is our derived diagnostic, not a measured error reported by Lund et al. These values permit a real-parameter pulse-time and attitude-ablation plot without treating the result as small-target detection validation.

## Wijaya and van Groesen synthetic sea and geometric shadow model

Wijaya and van Groesen, “Determination of the significant wave height from shadowing in synthetic radar images,” *Ocean Engineering* 114, 204–215 (2016), DOI [10.1016/j.oceaneng.2016.01.011](https://doi.org/10.1016/j.oceaneng.2016.01.011), is reproduced in the author’s 2017 dissertation chapter [PDF](https://ris.utwente.nl/ws/files/13493346/thesis_AP_Wijaya.pdf). Chapter 3, PDF pages 40–41, defines a directional spectrum $E_2(\omega,\theta)=E(\omega)D(\theta)$ and the normalized spreading function

$$D(\alpha)=A\cos^{2s}(\alpha-\alpha_0),\quad |\alpha-\alpha_0|\leq \pi/2,$$

with $D=0$ outside that interval and $A$ selected so that its directional integral is one. Their single-summation realization uses equidistant frequencies and one randomly drawn direction per frequency. Equation (3.2) gives

$$\eta(r,\theta,t)=\sum_{n=1}^{N}\sqrt{2E(\omega_n)\Delta\omega}\cos\!\left(k_n r\cos(\theta-\psi_n)-\omega_n t+\phi_n\right),$$

where $k_n$ follows the exact linear-wave dispersion relation, $psi_n$ is sampled from $D$, and $phi_n$ is uniform on $[0,2\pi]$. Equation (3.3) samples radar snapshots at multiples of the rotation interval. This is directly computable from a selected spectrum and documented random seed.

For each ray, the radar image keeps only geometrically visible surface points. The source defines the normalized variables $h=H_r/H_s$ and $\rho=r/\lambda_p$ on PDF page 43. For a long-crested harmonic wave, Equation (3.8), PDF page 44, gives visibility as $(\xi_l(r)+\xi_r(r))/\lambda$ when $r>\lambda H_r/(2\pi A)$ and unity otherwise. The geometric construction uses the near crest tangent and the next crest intersection with the critical ray. This supplies a reproducible binary-shadow arm for comparison with a continuous diffraction arm.

The executed harmonic reproduction follows Figure 3.4 in the dissertation chapter reproduced from the 2016 journal paper. It uses $T=9$ s, water depth 50 m, radar-height to harmonic-amplitude ratios $h=H_r/A=5$ and 10, and $M=1400$ phase samples. The executed implementation evaluates the full geometric visibility indicator from Equation (3.4) and its phase average from Equation (3.7), with wavelength $\lambda=124.8286$ m and radial spacing $\lambda/400$. Refining to 2800 phase samples and $\lambda/800$ radial spacing changes the reported visibility by at most 0.001072. The ratio $H_r/H_s$ is the normalization for irregular waves; it should not replace the harmonic Figure 3.4 ratio $H_r/A$. The model includes geometric shadowing only; tilt modulation, hydrodynamic modulation, wind modulation, scattering, and vessel motion are outside its construction.

## Models not yet reproducible from verified full text

McCann and Bell, DOI [10.1109/ACCESS.2018.2814081](https://doi.org/10.1109/ACCESS.2018.2814081), has verified metadata and an accessible abstract/record, but the full article equations were not available in the checked sources. The exact registration objective and parameter values are therefore not transcribed here. Lund’s paper states that its constant 1.328 degree radar-image heading offset was identified by the McCann and Bell calibration procedure, which is a verified reuse of that result.

Janssen, Belmont, Christmas, and Ferrier, DOI [10.1016/j.apor.2026.105183](https://doi.org/10.1016/j.apor.2026.105183), has a verified publisher record and the sibling evidence record confirms its two-dimensional incident-field path-sum scope. The full text and equations were not accessible during this pass, so no path-sum equation or numerical parameter is claimed here. The proposed implementation should use it only after the paper is obtained and equation numbers are checked.

## Reproducibility boundary

The Lund transform supplies real radar and navigation parameters for pulse-time pose ablations. The Wijaya model supplies a synchronized synthetic wave field, random directional components, and geometric visibility. Their combination can generate evidence beyond a schematic while keeping the binary-shadow assumption distinct from diffraction and target backscatter. Neither source validates the full proposed small-target outage chain. Independent synchronized wave geometry, vessel pose, target truth, and calibrated radar remain required for experimental validation.
