#import "_style.typ": *
#show: report-setup.with(title: "NAIRR Pilot", program: "NAIRR Pilot")
#title-block(program: "NAIRR Pilot", tagline: "National AI Research Resource — lightweight path to DGX Cloud, Azure, and DOE GPUs")

= Program Overview

The National Artificial Intelligence Research Resource (NAIRR) Pilot launched
in January 2024 as a coordinated two-year demonstration project led by the
U.S. National Science Foundation (NSF) in partnership with the Department of
Energy (DOE), the National Institutes of Health (NIH), DARPA, NASA, NIST, and
a broad consortium of industry and academic providers. The Pilot is the
precursor to a full-scale, statutorily authorized NAIRR that the
administration and Congress are now moving to stand up as a permanent
program. NSF released the NAIRR Operations Center (NAIRR-OC) solicitation in
late 2025 with a full proposal deadline of February 4, 2026, signaling the
transition from pilot to permanence. The Pilot itself is funded and
provisioned to operate through approximately mid-2026, with allocations
remaining open until provider resources are exhausted.

The provider list is unusually broad for a federal compute program. On the
commercial side, NVIDIA contributes roughly \$30M of value, including
\$24M in DGX Cloud credits (H100 and H200 systems). Microsoft contributes
\$20M in Azure credits across ND H100 v5 and ND H200 v5 families, plus
named-model access. Amazon Web Services, Google Cloud, OpenAI, Anthropic,
Hugging Face, Meta, IBM, Cerebras, Groq, and several other vendors provide
either credits, model access, or hosted inference. On the public side,
Argonne National Laboratory (Polaris, Aurora, AI Testbed), Oak Ridge
National Laboratory, Lawrence Berkeley National Laboratory's NERSC
(Perlmutter), TACC (Vista, Lonestar6), PSC (Bridges-2, Neocortex), NCSA
(Delta, DeltaAI), SDSC (Expanse), Purdue (Anvil), and Indiana University
(Jetstream-2) all contribute capacity. The Pilot's scientific scope is
deliberately AI/ML-only, in contrast to ACCESS, which is general HPC.

= Four Call Types

The Pilot is organized around four primary calls plus a Deep Partnerships
track. The structure rewards small, fast asks for routine work and reserves
heavier review for the largest grants.

#table(
  columns: (auto, 1fr, auto, auto),
  align: (left, left, left, left),
  table.header[Call][Purpose][Term][Cadence],
  [Classroom], [Course-integrated AI/ML instruction with shared student accounts and curated datasets.], [1 semester], [Rolling, ~2 weeks],
  [Research], [Open-ended AI/ML research at the project level; the workhorse track for grad students and PIs.], [12 months], [Rolling, ~3--4 weeks],
  [Education], [Workshops, tutorials, summer schools, REUs, and broader training events.], [Event-bound], [Rolling, ~2--3 weeks],
  [Software], [Tooling, benchmarks, model hubs, and infrastructure that the broader NAIRR community will reuse.], [12 months], [Rolling, ~3--4 weeks],
)

A separate Start-Up call provides 3-month, capped allocations
(approximately 2,000 GPU-hours on TACC Vista, Purdue Anvil AI, SDSC Expanse
AI, or PSC Bridges-2 GPU; 500 node-hours on the ANL AI Testbed; or 50 CS-2
hours on PSC Neocortex) with a turnaround inside three weeks. Start-Up is
the recommended on-ramp for new users, and a successful Start-Up project
makes a follow-on Research request straightforward.

= Hardware Specs

The table below lists the public, AI-relevant accelerators reachable via a
NAIRR allocation. Aurora is included for completeness even though its Intel
Max 1550 (Ponte Vecchio) GPUs are not CUDA-compatible and require oneAPI or
SYCL ports. The "TFLOPS" column is dense FP16/BF16 tensor throughput
without sparsity, so figures are directly comparable to the 989 TFLOPS H200
baseline used elsewhere in this report.

#table(
  columns: (1.3fr, auto, auto, auto, auto, 1.4fr),
  align: (left, left, right, right, right, left),
  table.header[Resource][GPU][VRAM (GB)][FP16 TFLOPS][BW (TB/s)][Interconnect],
  [NVIDIA DGX Cloud], [H100 SXM], [80], [989], [3.35], [NVLink 4 + 3.2 Tbps IB],
  [NVIDIA DGX Cloud], [H200 SXM], [141], [989], [4.80], [NVLink 4 + 3.2 Tbps IB],
  [Azure ND H100 v5], [H100 SXM], [80], [989], [3.35], [NVLink 4 + 1.6 Tbps IB],
  [Azure ND H200 v5], [H200 SXM], [141], [989], [4.80], [NVLink 4 + 3.2 Tbps IB],
  [ANL Polaris], [A100 40GB], [40], [312], [1.55], [HPE Slingshot 11],
  [ANL Aurora #footnote[Intel Max 1550 GPUs require oneAPI/SYCL; CUDA code does not run unmodified.]], [Intel Max 1550], [128], [419], [3.30], [HPE Slingshot 11],
  [NERSC Perlmutter], [A100 40GB], [40], [312], [1.55], [HPE Slingshot 10],
  [NCSA Delta], [A100 40GB], [40], [312], [1.55], [HPE Slingshot 10],
  [NCSA DeltaAI], [GH200], [96], [989], [4.00], [HPE Slingshot 11],
  [Purdue Anvil AI], [A100 40GB], [40], [312], [1.55], [HDR-200 InfiniBand],
  [TACC Vista], [GH200], [96], [989], [4.00], [NDR-400 InfiniBand],
)

= Allocation Sizes

NAIRR allocations are denominated inconsistently across providers. Cloud
partners issue dollar credits, DOE labs issue node-hours, and NSF systems
issue service units (SUs) or GPU-hours that map to ACCESS conventions. The
table below normalizes typical Research-call awards into _H200-hour
equivalents_ using dense FP16 throughput. Conversions are
$"hours" times "TFLOPS"_"system" / 989$, summed over the per-project award
size, with cloud credits converted at on-demand list pricing for the
relevant SKU.

#table(
  columns: (1.3fr, 1.3fr, auto, auto),
  align: (left, left, right, right),
  table.header[Resource][Typical award][Native units][H200-hr equivalent],
  [NVIDIA DGX Cloud], [\$25k credit (H100/H200)], [~640 GPU-hr], [~640],
  [Azure ND H200 v5], [\$5k--\$80k tiered], [125--2,000 GPU-hr], [125--2,000],
  [Azure ND H100 v5], [\$5k--\$80k tiered], [150--2,400 GPU-hr], [150--2,400],
  [ANL Polaris], [25,000 node-hr (4×A100)], [100,000 GPU-hr], [~31,500],
  [NERSC Perlmutter], [50,000 GPU-hr], [50,000 GPU-hr], [~15,800],
  [NCSA Delta (A100)], [40,000 GPU-hr], [40,000 GPU-hr], [~12,600],
  [NCSA DeltaAI (GH200)], [10,000 GPU-hr], [10,000 GPU-hr], [~10,000],
  [Purdue Anvil AI], [10,000 GPU-hr], [10,000 GPU-hr], [~3,160],
  [TACC Vista (GH200)], [10,000 GPU-hr], [10,000 GPU-hr], [~10,000],
  [ANL Aurora], [5,000 node-hr (6×Max1550)], [30,000 GPU-hr], [~12,700],
)

== Worked Example

A 50,000 GPU-hour Perlmutter A100 award contributes
$50000 times 312 / 989 approx 15780$ H200-hours of dense FP16 compute. The
same project supplemented by a \$25k DGX Cloud H200 credit (about 640
H200-hours at the published reservation rate of roughly \$3.90/GPU-hr) and
a 10,000 GPU-hour DeltaAI GH200 award yields roughly
$15780 + 640 + 10000 = 26420$ H200-hours total. That is enough to train a
13B-parameter dense transformer from scratch on ~300B tokens at
industry-standard utilization, or to run several thousand fine-tuning
sweeps on 7B-class models.

= Approval Timeline

NAIRR review cadence is one of its main competitive advantages. Start-Up
projects are reviewed continuously and decided within three weeks. Research
allocations are reviewed monthly, with most awards posted two to four weeks
after submission. Classroom requests are typically turned around in under
two weeks, and Education event allocations are reviewed against the event
date. The exception is _DGX Cloud_, which is heavily oversubscribed; the
review committee meets monthly but the queue can stretch several months
when demand spikes, and not every meritorious request is funded on the
first cycle. Azure ND H200 v5 has been the most consistently available
high-end tier through 2025--2026.

The application itself is short. The standard Research request is a 2--3
page project description with no required letters of support, no required
faculty sponsor for postdocs, and a one-page methods/compute-justification
section. Graduate students may apply with a PI sponsor signature; the PI
need not be the requester. There is no cost share and no indirect cost
recovery.

= Eligibility

Eligibility is broader than ACCESS but narrower than purely commercial
credit programs. Requesters must be affiliated with a U.S.-based academic,
nonprofit, or federal research institution, or with a U.S. small business.
Graduate students and postdocs are eligible directly with PI sponsorship.
Non-U.S. collaborators may be added to a project but cannot be the lead
PI, and certain partner resources (notably DGX Cloud and some DOE
testbeds) require additional citizenship or institutional screening before
account activation. Projects involving export-controlled data, classified
work, or human-subjects data carrying HIPAA obligations face additional
review and are routed only to compatible providers.

= Things to Know

Several practical points materially affect how to use NAIRR. _DGX Cloud_
and _Azure_ behave very differently in practice. DGX Cloud is requested as
a dollar credit, drawn down on a managed reservation, and the review
committee actively allocates against a fixed pool, so framing the request
around throughput-per-experiment rather than wall-clock helps. Azure
credits are spent against on-demand or reserved SKUs, and underused credits
expire at the end of the 12-month term with no rollover, so plan a burn
schedule up front.

Storage is generally _not_ part of the allocation. DOE labs provide scratch
and project filesystems sized to the compute award, but cloud providers
expect researchers to provision and pay for their own object storage out of
the same credit pool, which can quietly consume 10--20\% of an Azure award
on multi-terabyte datasets. NAIRR also imposes an open-science requirement.
Resulting publications, code, and (where licensing permits) trained model
artifacts must be deposited in a public repository and acknowledged with
the standard NAIRR citation.

NAIRR allocations stack with ACCESS allocations, and there is no penalty
for holding both. The recommended pattern is to use ACCESS Explore or
Discover for general HPC and CPU-heavy preprocessing, NAIRR Research for
H100/H200/GH200 training, and NAIRR Start-Up to bridge the gap during
ACCESS review.

= Strategic Fit

For a graduate AI researcher who needs Hopper-class GPUs in weeks rather
than months, NAIRR is the fastest legitimate path. The application is
roughly one-third the length of an ACCESS Accelerate request, requires no
letters, and is reviewed monthly against an AI-only docket where ML
projects are not competing against general HPC. Recommend NAIRR Start-Up as
the first-line application for any new project; promote to NAIRR Research
once preliminary results justify a 12-month award; and request DGX Cloud or
Azure ND H200 v5 only when a documented capability gap (FP8 training,
NVLink-4 all-reduce bandwidth, 141 GB VRAM for activation memory) makes the
on-prem A100 systems inadequate.

= Summary

#table(
  columns: (1.3fr, auto, auto, auto, auto),
  align: (left, left, left, right, left),
  table.header[Resource][Approval][Typical size][H200-hr eq.][Ease],
  [NAIRR Start-Up], [< 3 wk], [2,000 GPU-hr], [~640--2,000], [Very high],
  [Research / Anvil A100], [3--4 wk], [10,000 GPU-hr], [~3,160], [High],
  [Research / Perlmutter], [3--4 wk], [50,000 GPU-hr], [~15,800], [High],
  [Research / Polaris], [3--4 wk], [25,000 node-hr], [~31,500], [High],
  [Research / DeltaAI GH200], [3--4 wk], [10,000 GPU-hr], [~10,000], [Medium],
  [Research / TACC Vista], [3--4 wk], [10,000 GPU-hr], [~10,000], [Medium],
  [Research / Azure H200], [3--4 wk], [\$5k--\$80k], [125--2,000], [Medium],
  [Research / DGX Cloud], [4--12 wk], [\$25k credit], [~640], [Low (queue)],
  [Aurora (Intel Max)], [3--4 wk], [5,000 node-hr], [~12,700], [Low (port)],
)

#h200-note

= Sources

#set text(size: 9pt)
- NAIRR Pilot home and allocations catalog: #link("https://nairrpilot.org/")[nairrpilot.org] · #link("https://nairrpilot.org/allocations")[/allocations] · #link("https://nairrpilot.org/opportunities/allocations")[/opportunities/allocations] · #link("https://nairrpilot.org/opportunities/startup-project")[/opportunities/startup-project]
- NAIRR Pilot proposal instructions and FAQ: #link("https://nairrpilot.org/nairr-pilot-proposal-instructions")[proposal instructions] · #link("https://nairrpilot.org/help")[FAQ]
- NAIRR Deep Partnerships and Azure Deep Partnership: #link("https://nairrpilot.org/opportunities/deep-partnerships")[NAIRR Deep Partnerships] · #link("https://www.cloudbank.org/news/new-nairr-deep-partnership-opportunity-microsoft-azure-apply-september-15-2025")[CloudBank Azure Deep Partnership]
- NSF NAIRR program page and 2-year update: #link("https://www.nsf.gov/focus-areas/ai/nairr")[nsf.gov/focus-areas/ai/nairr] · #link("https://www.nsf.gov/cise/updates/nairr-2-years-advancing-american-artificial-intelligence")[NAIRR at 2 years]
- NAIRR-OC solicitation (transition to permanent program): #link("https://www.nsf.gov/funding/opportunities/nairr-oc-foundations-operating-national-artificial-intelligence")[NSF NAIRR-OC]
- Provider documentation: #link("https://www.rcac.purdue.edu/anvil/anvilnairr")[Purdue Anvil NAIRR] · #link("https://delta.ncsa.illinois.edu/delta-allocations/")[NCSA Delta allocations] · #link("https://www.ncsa.illinois.edu/ncsas-delta-prominent-choice-of-nairr-pilot-researchers/")[NCSA Delta usage report]
- Industry contributions: #link("https://www.fiercesensors.com/electronics/nairr-pilot-gets-30m-nvidia-20m-azure")[NVIDIA \$30M / Azure \$20M] · #link("https://www.microsoft.com/en-us/research/project/national-ai-research-resource-nairr-pilot/")[Microsoft Research NAIRR]
- Hardware specs cross-checked against NVIDIA H100/H200/GH200 datasheets, Intel Data Center GPU Max 1550 brief, and Azure ND H100/H200 v5 product pages.
