#import "_style.typ": *
#show: report-setup.with(title: "NERSC", program: "NERSC")
#title-block(program: "NERSC", tagline: "DOE SC user facility at LBNL — Perlmutter and the upcoming Doudna system")

= Program overview

The National Energy Research Scientific Computing Center (NERSC) is a U.S. Department of Energy (DOE) Office of Science user facility located at Lawrence Berkeley National Laboratory (LBNL). It is the mission high-performance computing (HPC) center for the DOE Office of Science, supporting roughly 11,000 researchers across more than 1,000 projects each year. The current production flagship is _Perlmutter_, an HPE Cray EX system that combines NVIDIA A100 GPU nodes with AMD EPYC CPU nodes on the HPE Slingshot-11 interconnect.

In May 2025 NERSC announced its next-generation system, _Doudna_ (NERSC-10), named for Nobel laureate Jennifer Doudna. Doudna will be a Dell-integrated system built around the NVIDIA Rubin-class GPU platform with Vera CPUs, NVIDIA Quantum-X800 InfiniBand, and an IBM Storage Scale all-flash tier. It is expected to enter production in 2026 and is designed to deliver more than 10x the application performance of Perlmutter while integrating tightly with DOE experimental facilities. Primary eligibility for either system requires DOE Office of Science funding, mission alignment, or access through a partner allocation program such as NAIRR.

= Hardware specifications

#table(
  columns: (1.4fr, 1fr, 1fr, 1fr, 1fr, 1fr),
  align: (left, left, left, left, left, left),
  table.header[Partition][GPU / CPU][Node count][Per-GPU FP16][Per-GPU BW][Interconnect],
  [Perlmutter GPU (40 GB)], [4× A100 40 GB SXM4], [1536], [312 TFLOPS], [1.56 TB/s], [Slingshot-11],
  [Perlmutter GPU (80 GB)], [4× A100 80 GB SXM4], [subset], [312 TFLOPS], [2.0 TB/s], [Slingshot-11],
  [Perlmutter CPU], [2× AMD EPYC Milan], [3072], [n/a], [n/a], [Slingshot-11],
  [Doudna (NERSC-10)], [NVIDIA Rubin (Vera CPU)], [TBD], [TBD (Rubin)], [TBD (HBM4)], [Quantum-X800 IB],
)

Per Perlmutter GPU node, four A100s deliver an aggregate dense FP16 tensor throughput of roughly 1248 TFLOPS, with 160 GB or 320 GB of HBM2e per node depending on the partition. NVLink3 provides intra-node GPU-GPU bandwidth of 600 GB/s. Doudna disclosures as of late 2025 confirm Rubin GPUs and Vera CPUs but withhold per-node TFLOPS and memory figures, so those entries remain _TBD_ pending NERSC's final acceptance documentation.

= Allocation types

NERSC awards compute through several distinct programs. _ERCAP_ (Energy Research Computing Allocations Process) is the main path and runs an annual DOE Office of Science peer review tied to mission alignment. _DDR_ (Director's Discretionary Reserve) holds approximately 10% of cycles and is the competitive route for projects without direct DOE funding. _ALCC_ (ASCR Leadership Computing Challenge) and _INCITE_ are separate DOE-wide programs, but both can land time on Perlmutter when reviewers route awards there. NERSC is also a compute partner in the National AI Research Resource (_NAIRR_) Pilot, which sidesteps DOE-funding gatekeeping for AI-focused academic research. Finally, _Education and Training_ accounts support classroom use, tutorials, and short-term workshops.

= Allocation sizes and H200-hour equivalence

ERCAP awards are denominated in _GPU node-hours_, where one node contains four A100 GPUs. Typical academic awards range from 10,000 to 500,000 GPU node-hours per year, with strategic DOE projects receiving more. Using the per-node aggregate of 1248 TFLOPS FP16 against the H200 SXM reference of 989 TFLOPS, one Perlmutter GPU node-hour is approximately $1248 / 989 approx 1.262$ H200-hours.

#table(
  columns: (1fr, 1fr, 1fr),
  align: (left, left, left),
  table.header[ERCAP award (node-hours)][Per-node FP16 TFLOPS][H200-hour equivalent],
  [50,000], [1248], [≈ 63,100],
  [100,000], [1248], [≈ 126,200],
  [500,000], [1248], [≈ 631,000],
)

These conversions assume compute-bound dense FP16 workloads. Memory-bandwidth-bound training (long-context attention, recommender embeddings) scales closer to the 2.0 / 4.8 TB/s ratio, which favors H200 by roughly 2.4x per GPU; readers should recompute against their own kernel mix.

= Approval timeline

The ERCAP cycle is fixed and slow. The annual call typically opens in early July, closes in early September, awards are announced in November, and allocations begin January 1 of the following calendar year. _DDR_ requests are accepted on a rolling basis and usually return decisions in two to six weeks. The _NAIRR_ path to Perlmutter generally clears in two to four weeks once the NAIRR review board routes the request. ALCC opens once per year (typically February) and INCITE once per year (typically April).

= Eligibility

ERCAP requires DOE Office of Science funding or a strong, documented mission alignment with one of the six SC program offices (ASCR, BER, BES, FES, HEP, NP). DDR is open to investigators whose work is _DOE-relevant_ even without direct DOE funding, and is the most common entry point for new academic groups. The NAIRR Pilot route bypasses the DOE-funding requirement entirely and treats Perlmutter as an AI research resource for U.S. academic and non-profit researchers. Education and training accounts cover instructor-led courses and short hackathons. All paths require export-control screening and U.S.-person or approved foreign-national status checks before account activation.

= Things to know

The pricing unit on Perlmutter is the _node-hour_, not the GPU-hour; a one-hour run on a single node consumes one node-hour but uses four A100s. The Burst Buffer and the Community File System (CFS) are quota-constrained and require explicit storage allocations separate from compute. NERSC maintains a strong AI and MLPerf engineering team, so the Jupyter, PyTorch, JAX, and container (_podman-hpc_, Shifter) stacks are unusually well-supported for an HPC site. Export-control compliance and project-level data classification are mandatory. The Doudna transition is expected to gap production AI capacity during portions of 2026 as Perlmutter is partially decommissioned and Doudna ramps to acceptance.

= Strategic fit

For a graduate student without DOE funding, _ERCAP is not realistic_ in the short term. The pragmatic paths are NAIRR-on-Perlmutter for AI-coded academic work, or a DDR proposal framed against a DOE Office of Science mission area. Perlmutter A100 throughput remains excellent for training at the 1B–13B parameter scale and for large-batch fine-tuning, but it is roughly one architectural generation behind H100 and two behind H200 for FP8 training and long-context inference. Researchers with workloads dominated by FP8 throughput or HBM bandwidth will see better wall-clock returns on H200-class systems; those with throughput-bound FP16 jobs and a tolerance for batch queuing will find Perlmutter highly productive.

= Summary

#table(
  columns: (1fr, 1fr, 1fr, 1fr, 1fr),
  align: (left, left, left, left, left),
  table.header[Allocation][Typical size][H200-hour equiv.][Approval time][Effort],
  [ERCAP], [10k–500k node-hr], [12.6k–631k], [3–6 months], [High],
  [DDR], [5k–50k node-hr], [6.3k–63.1k], [2–6 weeks], [Medium],
  [ALCC], [100k–1M node-hr], [126k–1.26M], [3–5 months], [High],
  [INCITE], [250k–2M node-hr], [315k–2.52M], [6–9 months], [Very high],
  [NAIRR (Perlmutter)], [1k–25k node-hr], [1.3k–31.6k], [2–4 weeks], [Low],
  [Education/Training], [≤ 1k node-hr], [≤ 1.3k], [1–2 weeks], [Very low],
)

#h200-note

= Sources

Verified 2024–2026 via NERSC documentation and partner announcement pages. Primary references include _nersc.gov/systems/perlmutter_ for hardware specifications, _nersc.gov/users/accounts/allocations_ and the ERCAP portal at _iris.nersc.gov_ for allocation policy and timelines, the NAIRR Pilot resource catalog at _nairrpilot.org_ for Perlmutter NAIRR access, and the May 2025 NERSC and NVIDIA press releases for the Doudna (NERSC-10) Rubin/Vera/Dell announcement. ALCC and INCITE policy come from _science.osti.gov/ascr_ and _doeleadershipcomputing.org_ respectively.
