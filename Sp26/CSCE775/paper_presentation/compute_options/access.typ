#import "_style.typ": *
#show: report-setup.with(title: "ACCESS", program: "NSF ACCESS")
#title-block(program: "NSF ACCESS", tagline: "Explore · Discover · Accelerate · Maximize tiers on TACC, PSC, SDSC, NCSA, and partner systems")

= Program Overview

The _Advanced Cyberinfrastructure Coordination Ecosystem: Services & Support_ (ACCESS) is the National Science Foundation's flagship cyberinfrastructure allocation program, launched in September 2022 as the operational successor to XSEDE. ACCESS coordinates open-science access to a federated portfolio of NSF-funded computing, storage, visualization, and cloud resources hosted at university and national laboratory partners. The program is administered through five service tracks (Allocations, User Support, Operations, Metrics, and Community Engagement & Performance) led by a consortium that includes the University of Illinois (NCSA), the Pittsburgh Supercomputing Center (PSC), the San Diego Supercomputer Center (SDSC), the Texas Advanced Computing Center (TACC), and others.

The federation includes some of the largest open-science systems in the United States. Representative member systems are TACC's _Stampede3_, _Vista_ (Grace-Hopper GH200), and the NSF Leadership-Class _Frontera_; PSC's _Bridges-2_ and _Neocortex_ (Cerebras wafer-scale); SDSC's _Expanse_ and _Voyager_ (Habana Gaudi); NCSA's _Delta_ and the AI-focused _DeltaAI_; Purdue's _Anvil_; and Indiana University's cloud-style _Jetstream2_. Allocations are denominated in a unified currency called _ACCESS Credits_, which users exchange at fixed per-resource rates for service units on individual systems. One ACCESS Credit is calibrated to roughly one CPU core-hour or one gigabyte-month of storage, with GPU-hours costing many credits depending on the device.

= Hardware Specifications

The table below summarizes per-GPU characteristics for the ACCESS systems most relevant to deep-learning workloads. Dense FP16/BF16 tensor TFLOPS are reported with sparsity disabled; bandwidth and TDP are vendor-published values. _Neocortex_ is included for completeness even though its Cerebras CS-2 wafer-scale engine is not GPU-comparable.

#table(
  columns: (auto, auto, auto, auto, auto, auto, auto),
  align: (left, left, center, center, center, center, center),
  table.header[System][GPU][GPUs/node][VRAM (GB)][FP16 TFLOPS][BW (TB/s)][TDP (W)],
  [NCSA Delta], [A100 SXM4], [4], [40 / 80], [312], [1.55 / 2.0], [400],
  [NCSA Delta], [A40 PCIe], [4], [48], [149.7], [0.696], [300],
  [NCSA DeltaAI], [GH200 (H100)], [4 (per node)], [96 (HBM3)], [756], [4.0], [~700],
  [TACC Vista], [GH200 (H100)], [1 (superchip)], [96 (HBM3)], [756], [4.0], [~700],
  [TACC Vista], [H100 PCIe], [2], [80 (HBM3)], [756], [3.35], [350],
  [SDSC Expanse], [V100 SXM2], [4], [32], [125], [0.9], [300],
  [Purdue Anvil], [A100 SXM4], [4], [40], [312], [1.55], [400],
  [PSC Bridges-2], [V100 SXM2], [8], [16 / 32], [125], [0.9], [300],
  [IU Jetstream2], [A100], [4], [40], [312], [1.55], [400],
  [PSC Neocortex], [Cerebras WSE-2], [n/a], [40 (SRAM)], [_n/a, wafer-scale_], [20 PB/s], [~23 kW],
)

The H200 SXM reference (#h200_fp16_tflops TFLOPS dense FP16, #h200_vram_gb GB HBM3e, #h200_bw_tbs TB/s) used throughout this report exceeds every device above on FP16 throughput and on memory capacity, and exceeds all but the GH200 on bandwidth. Per-GPU FP16/BF16 ratios versus the H200 are approximately 0.32 (A100), 0.13 (V100), 0.15 (A40), and 0.76 (GH200/H100).

= Allocation Tiers and Credit Conversion

ACCESS offers four project tiers. _Explore_ is for graduate-student projects, course work, and pilot studies, with a cap of 400 000 ACCESS Credits and a streamlined eligibility-only review on a rolling basis. _Discover_ supports research projects with modest needs and is capped at 1 500 000 credits, also reviewed on a rolling streamlined basis. _Accelerate_ funds mid-scale collaborative work up to 3 000 000 credits and is reviewed by panels approximately every quarter. _Maximize_ has no fixed credit cap and is awarded directly in resource units following a semiannual merit-review panel.

#table(
  columns: (auto, auto, auto, auto, auto),
  align: (left, center, center, center, left),
  table.header[Tier][Credit cap][Duration][Review][Submission cadence],
  [Explore], [400 000], [12 mo or grant], [Eligibility], [Rolling, hours-days],
  [Discover], [1 500 000], [12 mo or grant], [Streamlined], [Rolling, days-weeks],
  [Accelerate], [3 000 000], [12 mo or grant], [Panel merit], [Quarterly],
  [Maximize], [Variable, in-units], [12 months], [Panel merit, 10-page], [Semiannual],
)

_Rolling_ submission for the lower tiers means that proposals can be submitted at any time and reviewed in the order received, rather than waiting for a fixed deadline window.

#emph[Worked credit-to-H200-hour conversion.] On Delta, the published exchange rate places one A100 GPU-hour at one Delta GPU service unit, and the ACCESS Credit Calculator currently issues approximately 100 credits per Delta A100 GPU-hour. Spending #emph[200 000] credits therefore buys roughly 2 000 A100 GPU-hours on Delta. The A100 delivers 312 dense FP16 TFLOPS, while the H200 delivers #h200_fp16_tflops. The FP16-equivalent throughput is therefore

$ "H200-hours" approx 2000 times 312 / 989 approx 631 . $

For Anvil GPU the calculator returns roughly 6 000 A100 GPU-hours per 400 000 credits (about 66.7 credits per GPU-hour), which scales to approximately 1 893 H200-hours of FP16 work. On DeltaAI the per-GH200-hour rate is roughly 250 credits, so 200 000 credits yield about 800 GH200-hours, or approximately 612 H200-FP16-equivalent hours.

= Approval Timeline and Application Components

Explore reviews complete in hours to a few business days because the review is purely an eligibility check. Discover requests, which require a one-page abstract and a one-page resource justification, typically clear in a few business days to two weeks. Accelerate proposals require a three-page project description plus a CV and a prior-usage report and are panel-reviewed roughly every quarter, so wall-clock time from submission to award is typically four to six weeks. Maximize is the most demanding tier, with a ten-page project description, detailed scaling and benchmarking evidence, a prior-usage report, and CVs for all senior personnel; the semiannual panel cadence yields awards approximately three months after the submission window closes. All tiers require a brief renewal or progress narrative tied to the prior allocation.

= Eligibility

Eligible principal investigators must be researchers, faculty, postdoctoral scholars, or staff at U.S.-based accredited degree-granting institutions, federally funded research and development centers, or non-profit research organizations. Graduate students may not serve as PI but can request and manage allocations under a faculty sponsor or advisor. All ACCESS-funded work must be _open science_, meaning results must be intended for unrestricted publication; export-controlled, ITAR, classified, or HIPAA-protected work is not permitted on standard ACCESS resources.

= Things I Should Know

The most useful first-time trick is that any new account is automatically eligible for a small _startup_ Explore allocation that can be requested with an abstract of just a few sentences, providing immediate access while a larger Discover or Accelerate request is being prepared. ACCESS storage is requested separately from compute, but a single project can hold one compute allocation per system and a co-located storage allocation, so users should request storage on the same site as their primary compute to avoid cross-site data movement. The _ACCESS Campus Champions_ program embeds local cyberinfrastructure liaisons at most U.S. research universities; champions can sponsor startup allocations and shepherd new users through the proposal process.

Allocations can be _renewed_ with a short progress narrative or _supplemented_ mid-cycle if a project exhausts its credits early and can demonstrate productive use. Most major systems expose web gateways through Open OnDemand and JupyterHub, which lower the barrier to interactive ML development. Export-control limits prohibit storing ITAR or EAR-restricted data on shared file systems. Default scratch retention is short (commonly 30 days untouched), and project file systems are purged at the end of an allocation unless data is migrated to long-term storage or to the user's home institution.

= Strategic Fit for AI/ML Graduate Work

For AI/ML thesis work the practical question is how quickly a student can reach H100/H200-class throughput. _DeltaAI_ is currently the strongest single answer in ACCESS: its quad-Grace-Hopper nodes provide H100-class tensor performance with 96 GB of HBM3 per GPU, NVLink-C2C to a 480 GB Grace CPU memory pool, and an exchange rate that makes a 400 000-credit Explore allocation translate to roughly 1 600 GH200 GPU-hours. _Vista_ at TACC offers comparable per-GPU performance and is the second-fastest path. _Anvil_ and _Delta_ A100 partitions remain the workhorses for sub-100B-parameter training, fine-tuning, and reinforcement learning. _Expanse_ and _Bridges-2_ V100 partitions are best reserved for inference, smaller models, or capacity sweeps where 32 GB of VRAM suffices.

A successful ML proposal for ACCESS reviewers should foreground three things. First, a concrete scaling argument tying model size, batch size, and step time to the requested GPU-hours. Second, a clear training-versus-inference budget, since reviewers are sensitive to "I will use it for everything" requests. Third, a data-provenance and openness statement that confirms the work is publishable and that any datasets are not export-controlled. Compared to _NAIRR Pilot_, which currently emphasizes industry-donated H100 capacity, model API credits, and curated AI-ready datasets with a single coordinated review, ACCESS offers larger absolute GPU-hour budgets, longer time horizons, and more flexible compute-plus-storage bundling, at the cost of a heavier proposal burden at the Accelerate and Maximize tiers.

= Summary Ranking

#table(
  columns: (auto, auto, auto, auto, auto, auto),
  align: (left, center, center, center, center, left),
  table.header[Tier][Approval][Typical size][H200-hr equiv.][Difficulty][Best use],
  [Explore], [Hours-days], [400 k credits], [~1 200-1 600], [Trivial], [Pilots, coursework, thesis prelims],
  [Discover], [Days-weeks], [1.5 M credits], [~4 700-6 000], [Low], [Single-PI ML research project],
  [Accelerate], [4-6 weeks], [3 M credits], [~9 500-12 000], [Moderate], [Multi-student lab, mid-scale training],
  [Maximize], [~3 months], [Variable, in-units], [10 000+], [High], [Large-scale pretraining, leadership runs],
)

#h200-note

= Sources

- ACCESS Allocations, Project Types, https://allocations.access-ci.org/project-types
- ACCESS Allocations, Credit Exchange & Calculator, https://allocations.access-ci.org/exchange_calculator
- ACCESS Allocations, Resources catalog, https://allocations.access-ci.org/resources
- ACCESS Allocations, DeltaAI resource page, https://allocations.access-ci.org/resources/deltaai.ncsa.access-ci.org
- ACCESS Allocations, Delta resource page, https://allocations.access-ci.org/resources/delta.ncsa.access-ci.org
- NCSA, Delta Hardware and Network, https://delta.ncsa.illinois.edu/hardware_and_network/
- NCSA, DeltaAI Hardware and Network, https://delta.ncsa.illinois.edu/deltaai-hardware-and-network/
- NCSA, DeltaAI User Guide System Architecture, https://docs.ncsa.illinois.edu/systems/deltaai/en/latest/user-guide/architecture.html
- NCSA, DeltaAI Job Accounting, https://docs.ncsa.illinois.edu/systems/deltaai/en/latest/user-guide/job-accounting.html
- TACC, Vista system page, https://tacc.utexas.edu/systems/vista/
- TACC, Vista user documentation, https://docs.tacc.utexas.edu/hpc/vista/
- SDSC, Expanse system architecture, https://www.sdsc.edu/systems/expanse/system_architecture.html
- ACCESS Operations, Active Resources, https://operations.access-ci.org/resources/access-allocated
- ACCESS Operations, Anvil CPU discounted exchange rate, https://operations.access-ci.org/node/788
- Purdue RCAC, Anvil through ACCESS, https://www.rcac.purdue.edu/knowledge/anvil/access/anvil_through_access
- PSC, Neocortex resource page, https://www.psc.edu/resources/neocortex/
- PSC, Neocortex System Specifications, https://portal.neocortex.psc.edu/docs/system-specifications.html
- NVIDIA, H200 Tensor Core GPU, https://www.nvidia.com/en-us/data-center/h200/
