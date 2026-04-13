#import "_style.typ": *
#show: report-setup.with(title: "CloudLab & Chameleon", program: "CloudLab / Chameleon Cloud")
#title-block(program: "CloudLab & Chameleon Cloud", tagline: "Free bare-metal NSF testbeds for systems research and experimental GPU workloads")

= Program Overview

CloudLab and Chameleon Cloud are the two flagship National Science Foundation
(NSF) experimental research testbeds for cloud, systems, and networking
research in the United States. Both provide _bare-metal_ access to whole
servers (no hypervisor), root privileges, full network reconfiguration, and
custom OS images, and both are free to U.S.-affiliated researchers who agree
to publish their results in the open. They are not production HPC clusters.
They are instruments for conducting reproducible computer-science experiments
on real hardware, and their allocation, scheduling, and storage models reflect
that experimental orientation.

_CloudLab_ is operated by the University of Utah in partnership with the
University of Wisconsin-Madison, Clemson University, and the University of
Massachusetts Amherst, with additional federated sites at APT (Utah) and on
the Mass Open Cloud. The platform exposes roughly 1,800 servers across the
four primary sites, with continuously refreshed hardware generations and an
emphasis on cloud-stack research, software-defined networking, distributed
systems, kernel and OS work, and increasingly ML-systems experimentation.
Users instantiate _profiles_ (declarative experiment specifications stored on
GitHub) that allocate one or more bare-metal nodes, optionally wire them into
custom topologies through the underlying Emulab fabric, and boot arbitrary
disk images.

_Chameleon Cloud_ is led by the Texas Advanced Computing Center (TACC) and
the University of Chicago, with additional sites at Northwestern University
(StarLight) and the National Center for Atmospheric Research (NCAR). Like
CloudLab, Chameleon offers bare-metal reservations on heterogeneous
generations of hardware. Unlike CloudLab, Chameleon places strong emphasis on
_reproducibility tooling_. The Trovi catalog hosts shareable Jupyter
artifacts that bundle a reservation script, an image, and an analysis
notebook, so a paper's reviewer can re-run the entire experiment with a
single click against a fresh lease. Chameleon also operates a Swift-based
object store for persistent data, an OpenStack KVM partition (CHI\@Edge,
CHI\@KVM) for lightweight workloads, and since 2023 has expanded an explicit
_AI research_ track that has grown into the "Chameleon 2.0" AI hardware
program.

Both projects are funded under NSF's CISE Community Research Infrastructure
program. CloudLab's current renewal runs through 2026; Chameleon's third
phase ("Chameleon 2.0") was funded in 2024 and runs through 2028 with
explicit AI-systems hardware investments.

= CloudLab Hardware

CloudLab's hardware is highly heterogeneous and rotates frequently. The
table below lists representative GPU-bearing node types verified against
#link("https://www.cloudlab.us/hardware.php")[cloudlab.us/hardware]. Many
non-GPU node families (c220g1, c220g2, m400, xl170, etc.) exist alongside
these and are useful for distributed-systems and networking experiments.

#table(
  columns: (auto, auto, auto, auto, auto, auto, 1.1fr, auto, auto),
  align: (left, left, center, right, right, right, left, right, left),
  table.header[Cluster][Node][GPUs][VRAM (GB)][FP16 TFLOPS][BW (TB/s)][CPU][RAM (GB)][NIC],
  [Utah], [d740], [1× A100 PCIe], [40], [312], [1.55], [2× Xeon Gold 6336Y (24c)], [128], [25 GbE],
  [Utah], [d430], [—], [—], [—], [—], [2× Xeon E5-2630v3 (8c)], [64], [10 GbE],
  [Wisconsin], [c6525-100g], [—], [—], [—], [—], [2× AMD EPYC 7402P (24c)], [128], [2× 100 GbE],
  [Wisconsin], [c6525-25g], [—], [—], [—], [—], [2× AMD EPYC 7402P (24c)], [128], [2× 25 GbE],
  [Wisconsin], [c220g5], [optional 1× V100], [16/32], [125], [0.90], [2× Xeon Silver 4114 (10c)], [192], [10 GbE],
  [Wisconsin], [c4130], [4× V100 SXM2], [16], [125], [0.90], [2× Xeon E5-2680v4 (14c)], [256], [10 GbE],
  [Wisconsin], [c240g5 / T4], [1× T4], [16], [65], [0.32], [2× Xeon Silver 4114 (10c)], [192], [10 GbE],
  [Clemson], [c8220], [—], [—], [—], [—], [2× Xeon E5-2660v2 (10c)], [256], [10 GbE],
  [Clemson], [r320], [—], [—], [—], [—], [1× Xeon E5-2450 (8c)], [16], [1 GbE],
  [Clemson], [ibm8335 (P9)], [4× V100 SXM2], [16], [125], [0.90], [2× POWER9 (16c)], [512], [25 GbE],
  [Mass], [rs440xl], [optional 1× P100], [16], [21], [0.73], [2× Xeon Gold 6240R (24c)], [384], [25 GbE],
  [Mass], [sm220u], [—], [—], [—], [—], [2× Xeon Silver 4214R (12c)], [192], [25 GbE],
)

GPU inventory on CloudLab is genuinely scarce by AI-cluster standards. The
A100 d740 nodes at Utah and the V100 c4130/ibm8335 nodes at Wisconsin and
Clemson are the high-end tier, and they routinely show full reservation
calendars 1--2 weeks ahead. The Mass site is mostly CPU and storage
oriented. CloudLab's strength is _network-attached experiments_, not raw
GPU throughput.

= Chameleon Hardware

Chameleon's hardware is documented at
#link("https://www.chameleoncloud.org/hardware/")[chameleoncloud.org/hardware],
with each node grouped under a _node\_type_ string used in `blazar` lease
requests. Representative GPU node types verified against the public hardware
catalog appear below.

#table(
  columns: (auto, 1.2fr, auto, auto, auto, auto, 1.1fr, auto, auto),
  align: (left, left, center, right, right, right, left, right, left),
  table.header[Site][Node type][GPUs][VRAM (GB)][FP16 TFLOPS][BW (TB/s)][CPU][RAM (GB)][NIC],
  [CHI\@TACC], [compute_gpu_p100], [2× P100 PCIe], [16], [21], [0.73], [2× Xeon E5-2670v3 (12c)], [192], [10 GbE],
  [CHI\@TACC], [compute_gpu_rtx_6000], [2× RTX 6000], [24], [130], [0.67], [2× Xeon Gold 6240R (24c)], [192], [25 GbE],
  [CHI\@TACC], [compute_liqid (mixed)], [up to 8× A100/V100 (composable)], [40/32], [312/125], [1.55/0.90], [2× Xeon Gold 6230 (20c)], [384], [100 GbE],
  [CHI\@UC], [compute_gpu_a100_nvlink], [4× A100 SXM4 80GB], [80], [312], [2.04], [2× AMD EPYC 7763 (64c)], [1024], [2× 100 GbE],
  [CHI\@UC], [compute_gpu_a100_pcie], [2× A100 PCIe 40GB], [40], [312], [1.55], [2× AMD EPYC 7543 (32c)], [512], [100 GbE],
  [CHI\@UC], [compute_gpu_v100], [2× V100 PCIe], [32], [125], [0.90], [2× Xeon Gold 6126 (12c)], [192], [25 GbE],
  [CHI\@UC], [compute_gpu_mi100], [1× AMD MI100], [32], [185], [1.23], [2× AMD EPYC 7543 (32c)], [256], [25 GbE],
  [CHI\@NW], [compute_gpu_p100_nvlink (StarLight)], [4× P100 SXM2], [16], [21], [0.73], [2× Xeon E5-2680v4 (14c)], [256], [40 GbE],
  [CHI\@NCAR], [compute_cascadelake_r], [—], [—], [—], [—], [2× Xeon Gold 6248R (24c)], [192], [25 GbE],
)

== Chameleon 2.0 AI Hardware

Chameleon 2.0, the 2024--2028 phase, is rolling out an explicit AI hardware
tier targeted at machine-learning systems research. Verified through the
2024--2026 hardware announcements, the planned and partially-deployed
inventory includes the following.

#table(
  columns: (auto, 1.2fr, auto, auto, auto, auto, 1fr),
  align: (left, left, center, right, right, right, left),
  table.header[Site][Node type / project][GPUs][VRAM (GB)][FP16 TFLOPS][BW (TB/s)][Status],
  [CHI\@TACC], [compute_gpu_h100 (Liqid composable)], [up to 8× H100 PCIe], [80], [756], [2.00], [Deployed 2024],
  [CHI\@UC], [compute_gpu_h100_nvlink], [4× H100 SXM5], [80], [989], [3.35], [Deployed 2025],
  [CHI\@UC], [compute_gpu_gh200], [1× GH200 Grace-Hopper], [96], [989], [4.00], [Deployed 2025],
  [CHI\@UC], [compute_gpu_mi210], [2× AMD MI210], [64], [181], [1.64], [Deployed 2024],
  [CHI\@TACC], [compute_gpu_h200 (announced)], [4× H200 SXM5], [141], [989], [4.80], [Pilot 2026],
  [CHI\@NCAR], [atmospheric AI testbed (NSF NCAR)], [mixed A100/H100], [40--80], [312--989], [1.55--3.35], [Phased 2025--2026],
)

The Liqid composable fabric at CHI\@TACC is unique among NSF testbeds. It
allows researchers to dynamically attach 1--8 GPUs to a single host over
PCIe, which makes it ideal for studying GPU-disaggregation, heterogeneous
scheduling, and oversubscription policies that cannot be expressed on a
fixed-topology system.

= Allocation Model and H200-Hour Equivalence

Both testbeds use a _reservation_ model rather than a queue. A user requests
a specific node type for a specific window; if the calendar is open the
node is held exclusively for that user, booted into the chosen image, and
released back to the pool when the lease expires.

CloudLab leases default to 16 hours and may be extended through the web UI
up to roughly 7 days, with longer holds requiring a short justification
emailed to the operations team. There is no explicit credit currency.
Fairness is enforced by per-user concurrent-experiment caps and by the
operations team intervening if a small group monopolizes scarce nodes.

Chameleon meters usage in _Service Units_ (SUs), where 1 SU equals one
node-hour regardless of node type. New projects receive an initial
allocation, commonly 20,000 SUs for a six-month renewable term, with
top-ups by request. Leases default to 1 day and may be extended up to 7
days at a time, with a hard ceiling near 30 days for advance reservation.

The H200-hour equivalence below converts a typical 20,000 SU project-year
on Chameleon to dense FP16 H200-hours, summed over the GPUs attached to the
reserved node and using $"hours" times "GPUs" times "TFLOPS" / 989$ as the
conversion. The "utilization caveat" matters more here than on a queued HPC
system, because a researcher pays SUs for the entire wall-clock lease even
when the GPUs sit idle during instrumentation, debugging, or kernel
recompiles.

#table(
  columns: (1.4fr, auto, auto, auto, auto),
  align: (left, right, right, right, right),
  table.header[Reservation profile][Node-hours][GPUs / node][Per-GPU TFLOPS][H200-hr equivalent],
  [Chameleon 20k SUs on a100_nvlink (4× A100 80GB)], [20,000], [4], [312], [~25,228],
  [Chameleon 20k SUs on h100_nvlink (4× H100 SXM5)], [20,000], [4], [989], [~80,000],
  [Chameleon 20k SUs on gh200 (1× GH200)], [20,000], [1], [989], [~20,000],
  [Chameleon 20k SUs on rtx_6000 (2× RTX 6000)], [20,000], [2], [130], [~5,258],
  [Chameleon 20k SUs on p100 (2× P100)], [20,000], [2], [21], [~849],
  [CloudLab d740 A100 (1 node, 1 wk × 26 wk)], [4,368], [1], [312], [~1,378],
  [CloudLab c4130 V100 (1 node, 1 wk × 26 wk)], [4,368], [4], [125], [~2,208],
)

A 20,000 SU pool on the H100 NVLink node corresponds to roughly 80,000 dense
FP16 H200-hours of compute, which is competitive with mid-tier ACCESS or
NAIRR awards. In practice, a Chameleon project rarely converts that
favourably because the SU meter does not pause when nodes are idle.

= Approval Timeline

Account creation on either testbed takes one to three business days,
gated on institutional-email verification. Project creation is a separate
step requiring a short scientific description, an open-science commitment,
and (for student requesters) a faculty sponsor; project review usually
completes within one week. Once a project is approved, reservations are
made directly through the web UI or the API, with availability the only
constraint. Popular GPU node types on both testbeds, particularly the
A100 NVLink and H100 nodes on Chameleon and the d740 and c4130 nodes on
CloudLab, can require booking 1--2 weeks ahead, especially around paper
deadlines.

= Eligibility

Both testbeds require a U.S.-based or U.S.-collaborating affiliation and an
open-science research project. CloudLab's stated scope is _systems,
networking, OS, and cloud-architecture experimental research_, and pure
machine-learning training without an explicit systems contribution is
technically out-of-scope, although enforcement is light when a project
description frames the work in systems terms (scheduling, parallelism,
memory hierarchy, communication, fault tolerance). Chameleon has been more
permissive of AI workloads since 2023 and now actively recruits
ML-systems projects under the Chameleon 2.0 AI track. International
collaborators may be added to either project as users but cannot serve as
the lead PI.

= Things to Know

Researchers receive _full root_ on every allocated node and are expected to
treat each lease as a clean install. There is no shared cluster filesystem
in the HPC sense. Home directories are small (typically a few GB on
CloudLab, similarly modest on Chameleon login nodes), and any large dataset
must either stream from the Chameleon Object Store (Swift), be staged from
external object storage, or be re-downloaded at the start of each lease.
Persistent images can be saved to either testbed's image repository, which
preserves installed software but not bulk data.

Neither testbed permits 24/7 services. Reservations are finite, and a
forgotten extension that lapses will tear the node down, return it to the
pool, and wipe the local disk. Hardware is heterogeneous and refreshes year
to year; hardware pages are worth checking monthly because retired node
types simply disappear from the reservation calendar.

CloudLab's GitHub-hosted profiles are the dominant productivity multiplier.
A well-written profile turns a multi-hour manual setup into a 90-second
boot, and existing community profiles cover Kubernetes, Spark, OpenStack,
RDMA testbeds, and many other common stacks. On Chameleon the equivalent
artifact is a _Trovi notebook_, which bundles the lease, the image, and the
analysis Jupyter pipeline into a single shareable record that another
researcher can re-execute to reproduce a published figure.

GPU availability is the single biggest practical constraint on either
platform. Network experiments and CPU-bound systems work scale almost
arbitrarily; GPU experiments compete for a small inventory and benefit from
booking off-peak (overnight, weekends) and from being prepared to fall back
to an older accelerator generation when the latest tier is full.

= Strategic Fit

CloudLab and Chameleon are outstanding fits for projects whose _research
contribution is in the systems layer_. Distributed training-system
benchmarks, scheduler designs, communication-library experiments,
GPU-disaggregation studies, parallelism strategies, memory-hierarchy
characterization, network-protocol prototyping, and reproducibility
infrastructure all line up cleanly with the bare-metal, root-access,
custom-image programming model. They are poor fits for projects whose only
goal is to train a model end-to-end, since the SU economics, the lease
ceilings, and the GPU inventory all penalize long, monolithic training
runs.

The recommended pattern is to combine the testbeds with a production AI
allocation. Train and validate the model on NAIRR or ACCESS where
weeks-long jobs and large inventories are normal, then port the workload to
Chameleon or CloudLab for instrumented profiling, ablations on parallelism
strategy, communication-collective microbenchmarking, and any measurement
that requires deterministic single-tenant hardware.

= Summary

#table(
  columns: (1.2fr, auto, auto, auto, 1fr),
  align: (left, left, right, left, left),
  table.header[Platform][Hardware tier][Project-yr H200-hr eq.][Approval][Best fit],
  [CloudLab Utah d740], [A100 PCIe 40GB], [~1,400], [1--2 wk], [ML-systems],
  [CloudLab Wisconsin c4130], [4× V100 SXM2], [~2,200], [1--2 wk], [ML-systems / networking],
  [CloudLab Clemson ibm8335], [4× V100 + POWER9], [~2,200], [1--2 wk], [Systems / accelerator-arch],
  [Chameleon CHI\@UC a100_nvlink], [4× A100 80GB], [~25,000], [1--2 wk], [ML-systems / training],
  [Chameleon CHI\@UC h100_nvlink], [4× H100 SXM5], [~80,000], [1--2 wk], [ML-systems / training],
  [Chameleon CHI\@TACC Liqid H100], [up to 8× H100 PCIe (composable)], [~60,000--160,000], [1--2 wk], [GPU-disaggregation research],
  [Chameleon CHI\@UC gh200], [1× GH200], [~20,000], [1--2 wk], [Grace-Hopper / unified-memory],
  [Chameleon CHI\@TACC rtx_6000], [2× RTX 6000], [~5,300], [1--2 wk], [Inference / graphics],
)

#h200-note

= Sources

#set text(size: 9pt)
- CloudLab program and hardware: #link("https://www.cloudlab.us/")[cloudlab.us] · #link("https://www.cloudlab.us/hardware.php")[/hardware.php] · #link("https://docs.cloudlab.us/")[docs.cloudlab.us]
- CloudLab profiles and GitHub catalog: #link("https://www.cloudlab.us/p")[cloudlab.us/p] · #link("https://gitlab.flux.utah.edu/emulab/emulab-devel")[Emulab profile repos]
- Chameleon Cloud program and hardware: #link("https://www.chameleoncloud.org/")[chameleoncloud.org] · #link("https://www.chameleoncloud.org/hardware/")[/hardware] · #link("https://chameleoncloud.readthedocs.io/")[chameleoncloud.readthedocs.io]
- Chameleon Trovi reproducibility catalog: #link("https://www.chameleoncloud.org/experiment/share/")[Trovi share] · #link("https://chameleoncloud.readthedocs.io/en/latest/technical/sharing.html")[Trovi docs]
- Chameleon 2.0 AI hardware announcements: #link("https://www.chameleoncloud.org/blog/")[chameleoncloud.org/blog] · #link("https://www.chameleoncloud.org/news/")[news] (H100 NVLink, GH200, MI210, Liqid H100 deployment posts, 2024--2026)
- NSF awards: NSF CNS-1743363 (CloudLab Phase II), NSF OAC-2229466 (Chameleon Phase 3 / "Chameleon 2.0", 2024--2028)
- GPU specs cross-checked against NVIDIA P100, V100, T4, RTX 6000, A100, H100, H200, GH200 datasheets and AMD MI100/MI210 product briefs.
