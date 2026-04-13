#import "_style.typ": *
#show: report-setup.with(title: "DOE ALCC", program: "DOE ALCC")
#title-block(program: "DOE ALCC", tagline: "ASCR Leadership Computing Challenge — Frontier, Aurora, Polaris, NERSC allocations aligned to DOE mission")

= Program overview

The _ASCR Leadership Computing Challenge_ (ALCC) is the second of the two large open allocation programs run by the U.S. Department of Energy Office of Science. It is administered by the Office of _Advanced Scientific Computing Research_ (ASCR) and is the mission-aligned counterpart to INCITE. Where INCITE is curiosity-driven and open to any domain that can defend a leadership-scale science case, ALCC is explicitly steered toward the DOE mission portfolio. Energy production and storage, climate and Earth-system modeling, nuclear security, fusion and plasma science, accelerator design, and scientific artificial intelligence are the recurring priority themes.

ALCC awards approximately _30 percent_ of the available compute time on the DOE leadership-class systems. The eligible machines are the OLCF Frontier system at Oak Ridge, the ALCF Aurora and Polaris systems at Argonne, and the NERSC Perlmutter system at Lawrence Berkeley. Awards are one-year allocations that begin on _July 1_ and run through _June 30_ of the following year. The program complements INCITE by providing a second, mission-targeted entry point on the same hardware in the same calendar.

= Hardware specs

The four ALCC-eligible systems span three accelerator generations. Frontier is _AMD MI250X_, Aurora is _Intel Ponte Vecchio_ (Data Center GPU Max 1550), and the two NERSC and ALCF Ampere systems use _NVIDIA A100_ in slightly different memory configurations.

#table(
  columns: (auto, auto, auto, auto, auto, auto, auto),
  align: (left, left, center, center, center, left, center),
  table.header[System][Accelerator][VRAM][FP16/BF16 (TFLOPS, dense)][Mem BW (TB/s)][Interconnect][Nodes (ALCC-eligible)],
  [Frontier (OLCF)], [AMD MI250X (per GCD)], [128 GB], [383], [3.2], [Slingshot-11, 4 NICs/node], [9{,}408],
  [Aurora (ALCF)], [Intel PVC Max 1550], [128 GB], [839], [3.3], [Slingshot-11, 8 NICs/node], [10{,}624],
  [Polaris (ALCF)], [NVIDIA A100 40 GB], [40 GB], [312], [1.56], [Slingshot-10, HPE Apollo], [560],
  [Perlmutter GPU (NERSC)], [NVIDIA A100 40/80 GB], [40 / 80 GB], [312], [1.56 / 2.0], [Slingshot-11, 4 NICs/node], [1{,}792],
)

Frontier and Aurora are _exascale_ machines and dominate the available aggregate FLOPs in the ALCC pool; Polaris and Perlmutter remain attractive for projects that need NVIDIA-CUDA tooling at production scale.

= Allocation sizes and H200-hour equivalents

Typical ALCC awards range from roughly _50{,}000 node-hours_ for a focused single-system project to _500{,}000 node-hours_ for a flagship mission-aligned campaign. Conversion to H200-hour equivalents uses the dense FP16/BF16 tensor throughput ratio against the H200 reference value of #h200_fp16_tflops TFLOPS, multiplied by the GPUs per node on the awarded system.

#table(
  columns: (auto, auto, auto, auto, auto, auto),
  align: (left, center, center, center, center, center),
  table.header[System][GPUs/node][Per-GPU FP16 TFLOPS][Node-hours][Per-node ratio vs H200][H200-hour equivalent],
  [Frontier (small, 50k nh)], [8 GCDs], [383], [50{,}000], [$8 times 383 / 989 = 3.10$], [$approx 154{,}900$],
  [Frontier (large, 500k nh)], [8 GCDs], [383], [500{,}000], [3.10], [$approx 1{,}549{,}000$],
  [Aurora (small, 50k nh)], [6 tiles], [839], [50{,}000], [$6 times 839 / 989 = 5.09$], [$approx 254{,}500$],
  [Aurora (large, 500k nh)], [6 tiles], [839], [500{,}000], [5.09], [$approx 2{,}544{,}500$],
  [Polaris (small, 50k nh)], [4 A100], [312], [50{,}000], [$4 times 312 / 989 = 1.26$], [$approx 63{,}100$],
  [Polaris (large, 500k nh)], [4 A100], [312], [500{,}000], [1.26], [$approx 631{,}000$],
  [Perlmutter (small, 50k nh)], [4 A100], [312], [50{,}000], [1.26], [$approx 63{,}100$],
  [Perlmutter (large, 500k nh)], [4 A100], [312], [500{,}000], [1.26], [$approx 631{,}000$],
)

The headline takeaway is that an ALCC award sits in the same _millions of H200-hours_ tier as INCITE. A 500{,}000 node-hour Aurora allocation alone exceeds 2.5 million H200-hours of equivalent FP16 throughput.

= Approval timeline

ALCC runs on a strict annual cycle synchronized with the DOE fiscal calendar. The call for proposals opens in _February_, with a submission deadline in _early April_. ASCR convenes a peer-review panel through April and May. Awards are announced in _June_, and the allocation begins on _July 1_ and runs through _June 30_ of the following year.

The proposal package itself is a _10-page_ science and computational narrative, accompanied by a separate _computational readiness_ document that demonstrates the code can use the targeted system at scale, and a _data management plan_ describing storage, retention, and release. ASCR reviews on scientific merit, mission relevance, and technical readiness; the readiness component routinely eliminates otherwise strong science proposals when the team cannot show prior scaling runs.

= Eligibility

ALCC is open to researchers at _U.S. national laboratories_, _universities_, _industry_, and _other federal agencies_. Foreign collaborators are permitted on the project team, although the principal investigator and the lead institution typically must be U.S.-based. The PI is usually a senior researcher with a track record of leadership-scale runs, and graduate students and postdocs participate as co-investigators or as named team members. The work itself must align with a stated DOE mission area; method-development work without a clear mission anchor is generally re-directed to INCITE.

= Things to know

ALCC has a strong revealed preference for _applied, mission-relevant science_ over basic method development. Reviewers want to see how the compute moves a DOE program forward this fiscal year, not how it advances an algorithm in the abstract. Because ALCC and INCITE compete for the same physical machines, queue dynamics in the second half of an award year can be tight, and projects that cannot absorb that risk should plan for it explicitly.

A practical pre-application path is to first acquire _Director's Discretionary_ (DD) hours at the target facility, use them to run the scaling and readiness studies, and cite those runs in the ALCC proposal. _Scientific AI_, particularly large-model training and inference for drug discovery, materials, climate emulation, and fusion control, is an increasingly competitive sub-portfolio inside ALCC and now routinely captures awards that would historically have gone to traditional simulation.

= Strategic fit

For a single graduate student without an established DOE-aligned advisor, ALCC is _not a realistic first application_. It sits at the same tier as INCITE in terms of scale and review depth, and the mission-alignment requirement adds an additional constraint that is hard to satisfy from outside an ongoing DOE program. The realistic path is identical to INCITE. The student joins an advisor-led DOE-funded thread, contributes to the readiness runs on Director's Discretionary time, and is named on the ALCC proposal as a co-investigator. The reward is also identical, namely access to _millions of H200-equivalent hours_ on a leadership-class system for a full year.

= ALCC vs INCITE vs DD

#table(
  columns: (auto, auto, auto, auto, auto, auto),
  align: (left, left, left, left, left, left),
  table.header[Program][Tier][Share of machine][Approval difficulty][Typical award][One-line summary],
  [INCITE], [Leadership], [$approx 60%$], [Very high], [$10^5$–$10^6$ node-hours], [Open, curiosity-driven, peer-reviewed at the highest bar.],
  [ALCC], [Leadership], [$approx 30%$], [High], [$5 times 10^4$–$5 times 10^5$ node-hours], [Mission-aligned counterpart to INCITE on the same machines.],
  [Director's Discretionary], [Per-facility], [$approx 10%$], [Low to moderate], [$10^3$–$10^4$ node-hours], [Facility-director's pool for startup, scaling, and readiness work.],
)

= Summary

#table(
  columns: (auto, auto, auto, auto),
  align: (left, center, center, center),
  table.header[System][Typical ALCC allocation][H200-hour equivalent (range)][Fit rating],
  [Frontier (OLCF)], [50k–500k node-hours], [$approx 1.5 times 10^5$ – $1.5 times 10^6$], [Stretch with DOE-aligned advisor],
  [Aurora (ALCF)], [50k–500k node-hours], [$approx 2.5 times 10^5$ – $2.5 times 10^6$], [Stretch with DOE-aligned advisor],
  [Polaris (ALCF)], [50k–500k node-hours], [$approx 6.3 times 10^4$ – $6.3 times 10^5$], [Plausible via co-investigator role],
  [Perlmutter GPU (NERSC)], [50k–500k node-hours], [$approx 6.3 times 10^4$ – $6.3 times 10^5$], [Plausible via co-investigator role],
)

#h200-note

= Sources

#set text(size: 9pt)
- DOE Office of Science, ASCR Leadership Computing Challenge program page, science.osti.gov/ascr/alcc (verified 2024–2026).
- Oak Ridge Leadership Computing Facility, Frontier system specifications, olcf.ornl.gov/frontier (verified 2024–2026).
- Argonne Leadership Computing Facility, Aurora and Polaris system documentation, alcf.anl.gov (verified 2024–2026).
- National Energy Research Scientific Computing Center, Perlmutter architecture documentation, docs.nersc.gov/systems/perlmutter (verified 2024–2026).
- ALCC FY2024 and FY2025 awards announcements, science.osti.gov/ascr (verified 2024–2026 via WebSearch and WebFetch).
- NVIDIA H200 SXM datasheet, used as the H200-hour reference (989 TFLOPS dense FP16/BF16 tensor, 141 GB HBM3e, 4.8 TB/s).
