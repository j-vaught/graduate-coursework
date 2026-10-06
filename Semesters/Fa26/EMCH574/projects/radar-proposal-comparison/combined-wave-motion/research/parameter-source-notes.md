# Parameter source notes

Prepared 6 October 2026 by J.C. Vaught. These notes support the parameter-design section in `proposal.tex`. The proposal uses centralized bibliography keys and does not assert that proposed intervals are measured properties.

## Primary sources used

MIT OpenCourseWare, *Linear wave-body interactions*, Lecture 9, official lecture PDF. URL: <https://ocw.mit.edu/courses/2-24-ocean-wave-interaction-with-ships-and-offshore-energy-systems-13-022-spring-2002/f500bf012ed64ef2cb8e8d6f45a21bfd_lecture9.pdf>. The official appendix gives the linear encounter-frequency relation under its stated heading convention and motivates response-amplitude operators. BibTeX key already present: `MITOCW2002WaveBody`.

Lund et al., “Arctic Sea Ice Drift Measured by Shipboard Marine Radar,” *Journal of Geophysical Research: Oceans* 123, 4298–4321, 2018. DOI: <https://doi.org/10.1029/2018JC013769>. Author PDF: <https://faculty.washington.edu/jmt3rd/Publications/Lund_2018JC013769.pdf>. The paper documents 5 Hz navigation interpolation to 3 kHz pulse timing, a 1.25 s rotation period, 7.5 m grid, and 0.7 degree beam width in its specific experiment. Those values are external examples, not proposed sensor specifications. BibTeX key already present: `Lund2018SeaIceDrift`.

Navtech Radar, *RAS6 Series Datasheet*, 2024. URL: <https://navtechradar.com/wp-content/uploads/2024/06/RAS6-Series-datasheet-updated-11.06.24.pdf>. This is a hardware source for bounding an explicitly RAS6-based acquisition scenario. It does not justify importing the datasheet values into the illustrative model without matching antenna, waveform, range mode, and calibration. BibTeX key already present: `Navtech2024RAS6`.

Panagopoulos and Soraghan, “Small-target detection in sea clutter,” *IEEE Transactions on Geoscience and Remote Sensing* 42(7), 1355–1361, 2004. DOI: <https://doi.org/10.1109/TGRS.2004.827259>. This primary paper supports treating sea-clutter conditioning and small-target detection as detector-specific concerns. It does not set the proposed $P_{\mathrm{FA}}$ or calibration count. BibTeX key already present: `Panagopoulos2004SmallTarget`.

## Integrated bibliography records

The entries below use the integrated bibliography keys in `references.bib`.

MIT OpenCourseWare, *Linear Waves*, Lecture 20, 2.20 Marine Hydrodynamics. The PDF resolves with HTTP 200 and supports the small-slope linear-wave assumption. URL: <https://ocw.mit.edu/courses/2-20-marine-hydrodynamics-13-021-spring-2005/5d48a5937971d973fd8ca90c051a83f8_lecture20.pdf>.

```bibtex
@misc{MITOCW2011DampedOscillator,
  author       = {{Massachusetts Institute of Technology OpenCourseWare}},
  title        = {Damped Harmonic Oscillators},
  year         = {2011},
  howpublished = {18.03SC Differential Equations},
  url          = {https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011/911bc225e5913ba15517dbd70528c27a_MIT18_03SCF11_s13_1text.pdf}
}

@misc{MITOCW2005LinearWaves,
  author       = {{Massachusetts Institute of Technology OpenCourseWare}},
  title        = {Water Waves and Linearized (Airy) Wave Theory},
  year         = {2005},
  howpublished = {2.20 Marine Hydrodynamics, MIT OpenCourseWare, Lecture 20},
  url          = {https://ocw.mit.edu/courses/2-20-marine-hydrodynamics-13-021-spring-2005/5d48a5937971d973fd8ca90c051a83f8_lecture20.pdf}
}

@article{Rohling1983RadarCFAR,
  author  = {Rohling, Hermann},
  title   = {Radar CFAR Thresholding in Clutter and Multiple Target Situations},
  journal = {IEEE Transactions on Aerospace and Electronic Systems},
  year    = {1983},
  volume  = {AES-19},
  number  = {4},
  pages   = {608--621},
  doi     = {10.1109/TAES.1983.309350}
}

@article{McKay1979LatinHypercube,
  author  = {McKay, M. D. and Beckman, R. J. and Conover, W. J.},
  title   = {Comparison of Three Methods for Selecting Values of Input Variables in the Analysis of Output from a Computer Code},
  journal = {Technometrics},
  year    = {1979},
  volume  = {21},
  number  = {2},
  pages   = {239--245},
  doi     = {10.1080/00401706.1979.10489755}
}
```

The numerical standard-error calculation in the proposal is derived directly from the Bernoulli variance and is not presented as an externally documented parameter. The $ka\leq0.20$ screen is explicitly a chosen model-eligibility rule. It should not be described as a universal physical limit.

## Executable numerical verification

The deep-water checks in the proposal were recomputed with Python using $k=(2\pi f)^2/g$, $\lambda=2\pi/k$, and $a_{\max}=0.20/k$.

```text
f=0.15: k=0.0905468294  lambda=69.3915551881  a_max=2.2088018034
f=0.25: k=0.2515189705  lambda=24.9809598677  a_max=0.7951686492
f=0.35: k=0.4929771821  lambda=12.7453876876  a_max=0.4056982904
f=0.50: k=1.0060758819  lambda=6.2452399669   a_max=0.1987921623
case f=0.35, a=0.30: ka=0.1478931546
case f=0.35, a=0.50: ka=0.2464885911
case f=0.50, a=0.30: ka=0.3018227646
case f=0.25, a=0.30: ka=0.0754556911
```

The executable values establish that the central $0.35\,\mathrm{Hz}$, $0.30\,\mathrm{m}$ case has $ka\approx0.1479$, not $0.075$. The $ka\approx0.0755$ value belongs to the $0.25\,\mathrm{Hz}$, $0.30\,\mathrm{m}$ case.
