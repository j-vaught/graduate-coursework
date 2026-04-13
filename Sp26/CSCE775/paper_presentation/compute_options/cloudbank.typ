#import "_style.typ": *
#show: report-setup.with(title: "NSF CloudBank", program: "NSF CloudBank")
#title-block(program: "NSF CloudBank", tagline: "Managed access to AWS, Azure, GCP, and IBM Cloud for NSF-funded projects")

= Program overview

NSF CloudBank is a service, not a credits grant program. It is funded by the National Science Foundation under Award #1925001 and operated by a consortium of the San Diego Supercomputer Center (SDSC), the University of Washington, the University of California Berkeley, and the University of North Carolina at Chapel Hill. CloudBank handles the procurement, billing, cost monitoring, training, and technical onboarding required for NSF-funded researchers to use commercial cloud platforms (AWS, Microsoft Azure, Google Cloud, and IBM Cloud) without the institutional friction that normally accompanies cloud procurement.

The distinction is important. CloudBank does not, on its own, give a researcher free GPU hours. To use CloudBank a project must already have an active NSF award whose budget includes commercial cloud, _or_ the project must be funded through an NSF directorate solicitation that explicitly permits or pre-bundles CloudBank access (CISE supplements, CSSI, POSE, and similar). Once one of those conditions is met, CloudBank converts grant dollars into managed cloud spend and provides the wraparound services that turn raw cloud accounts into a usable research environment.

= What CloudBank provides

CloudBank operates a single portal that fronts AWS, Azure, GCP, and IBM Cloud accounts under a unified billing and identity layer. The service includes onboarding sessions, instructor-led and self-paced training, cost dashboards with anomaly alerts, migration assistance from on-premise or campus clusters, and special educational-use accounts for accredited courses. The educational accounts are an underused offering and can support entire classrooms with sandboxed cloud credits managed by the instructor.

CloudBank does _not_ include free credits by default. Credits flow either from the researcher's NSF award funds or from CloudBank-partnered credit programs (occasional AWS/GCP research credit drops that CloudBank brokers). Treat the platform as a managed cloud reseller with a research support staff attached, not as an XSEDE-style allocation system.

= Hardware specs

The instance families below are the GPU shapes CloudBank-funded researchers most frequently purchase. On-demand pricing is approximate public list pricing for 2024-2026 and varies by region. Reserved pricing assumes a one-year commitment and is also approximate.

== AWS GPU instances

#table(
  columns: 8,
  align: (left, center, center, center, center, center, center, center),
  table.header[Instance][GPUs][VRAM/GPU][FP16 TFLOPS][Mem BW][On-dem \$/GPU-hr][1-yr Res \$/GPU-hr][Notes],
  [p5.48xlarge], [8x H100], [80 GB], [989], [3.35 TB/s], [\$12.29], [\~\$7.50], [SXM, NVLink],
  [p5e.48xlarge], [8x H200], [141 GB], [989], [4.8 TB/s], [\~\$10.30], [\~\$6.50], [SXM, NVLink],
  [p4d.24xlarge], [8x A100], [40 GB], [312], [1.55 TB/s], [\~\$4.10], [\~\$2.50], [SXM, NVLink],
  [g5.48xlarge], [8x A10G], [24 GB], [125], [0.6 TB/s], [\~\$2.05], [\~\$1.30], [PCIe, inference],
  [g6.48xlarge], [8x L4], [24 GB], [121], [0.3 TB/s], [\~\$1.65], [\~\$1.05], [PCIe, inference],
)

== Azure GPU instances

#table(
  columns: 8,
  align: (left, center, center, center, center, center, center, center),
  table.header[Instance][GPUs][VRAM/GPU][FP16 TFLOPS][Mem BW][On-dem \$/GPU-hr][1-yr Res \$/GPU-hr][Notes],
  [ND H200 v5], [8x H200], [141 GB], [989], [4.8 TB/s], [\~\$9.00], [\~\$5.80], [SXM, NVLink],
  [ND H100 v5], [8x H100], [80 GB], [989], [3.35 TB/s], [\~\$8.50], [\~\$5.50], [SXM, NVLink],
  [ND A100 v4], [8x A100], [80 GB], [312], [2.0 TB/s], [\~\$3.85], [\~\$2.40], [SXM, NVLink],
  [NC A100 v4], [1-4x A100], [80 GB], [312], [2.0 TB/s], [\~\$3.65], [\~\$2.30], [PCIe],
)

== GCP GPU instances

#table(
  columns: 8,
  align: (left, center, center, center, center, center, center, center),
  table.header[Instance][GPUs][VRAM/GPU][FP16 TFLOPS][Mem BW][On-dem \$/GPU-hr][1-yr Res \$/GPU-hr][Notes],
  [a3-ultragpu-8g], [8x H200], [141 GB], [989], [4.8 TB/s], [\~\$10.50], [\~\$6.80], [3.2 Tbps fabric],
  [a3-megagpu-8g], [8x H100], [80 GB], [989], [3.35 TB/s], [\~\$11.00], [\~\$7.10], [SXM],
  [a2-ultragpu-8g], [8x A100], [80 GB], [312], [2.0 TB/s], [\~\$5.07], [\~\$3.20], [SXM],
  [g2-standard-96], [8x L4], [24 GB], [121], [0.3 TB/s], [\~\$0.85], [\~\$0.55], [PCIe, inference],
)

= How to get funded hours

There are three realistic paths to spending CloudBank dollars on GPUs.

The first path is to include CloudBank in the budget justification of a new NSF proposal. The PI writes a cloud-spend line item, names CloudBank as the procurement vehicle, and on award the funds are routed through the CloudBank portal. This is the cleanest path but is gated by the underlying NSF proposal cycle.

The second path is to apply to a solicitation that pre-bundles CloudBank access. CISE has historically issued CloudBank supplements to existing CISE awards, and CSSI and POSE solicitations frequently allow cloud line items routed through CloudBank. These are usually faster than a fresh proposal.

The third path is to take an existing NSF project that has unspent funds and a permissible budget category (cloud or computing services) and route a slice of it through CloudBank for the discount and management benefits. This is the fastest path and can sometimes be set up in a few weeks.

== Conversion table: cloud budget to H200-hours

The reference rates below use AWS p5e on-demand at \$10.30/GPU-hr and reserved at \$6.50/GPU-hr; Azure ND H200 v5 on-demand at \$9.00/GPU-hr and reserved at \$5.80/GPU-hr. _All figures are gross of egress, storage, and CloudBank's small administrative overhead._

#table(
  columns: 5,
  align: (left, center, center, center, center),
  table.header[Cloud budget][AWS p5e on-dem H200-hr][AWS p5e 1-yr res H200-hr][Azure ND H200 v5 on-dem H200-hr][Azure ND H200 v5 1-yr res H200-hr],
  [\$10,000], [\~970], [\~1,540], [\~1,110], [\~1,720],
  [\$25,000], [\~2,425], [\~3,845], [\~2,780], [\~4,310],
  [\$100,000], [\~9,710], [\~15,385], [\~11,110], [\~17,240],
)

For a sense of scale, \$25,000 on Azure reserved H200 instances buys roughly 4,300 H200-GPU-hours, or about 22 days of an 8x H200 node running 24/7. That is enough to fine-tune mid-sized 7B-13B parameter models several times or to run a meaningful pretraining ablation sweep.

= Approval timeline

Timelines depend entirely on which path is taken. Embedding CloudBank in a fresh NSF proposal inherits the proposal cycle, which is six months at a minimum and typically nine to twelve months from submission to first usable dollar. CloudBank-aware supplements to existing CISE awards run faster, generally two to three months from submission to portal access. Onboarding existing project funds is the quickest route at roughly two to three weeks once the institutional sub-agreement and credit card or invoice setup are in place.

= Eligibility

The principal eligibility requirement is an active NSF award held by the requesting PI or co-PI, or a documented role on a team whose lead PI holds such an award. Graduate students cannot apply on their own behalf. Educational accounts are available for accredited courses at US institutions, in which the instructor of record is the eligible party.

= Things to know

Credits and budget allocations expire with the project end date and any unspent balance is forfeited at award close, so back-loading large GPU runs into the final months is risky if institutional invoicing is slow. Egress and storage are consistently the most underestimated line items; multi-terabyte dataset transfers, cross-region replication, and persistent block storage can easily double a naive compute-only budget. GPU quota increases on H100 and H200 instance families still require explicit approval from the underlying cloud provider regardless of CloudBank involvement, and these reviews can take one to four weeks. Spot and preemptible instances cut effective cost by 60-80% but require checkpoint-aware training code. The training and human support that CloudBank provides is, for many groups, the most valuable part of the program. Finally, CloudBank cannot be used to spend non-NSF funds, so DOE, DARPA, NIH, or industry-funded projects must look elsewhere.

= Strategic fit

CloudBank is _not_ a free-GPU pathway for an unaffiliated graduate student. There is no mechanism to apply directly without an underlying NSF award. The program becomes useful in a specific scenario, when a student's advisor already holds an active CISE, CSSI, POSE, or similar NSF grant whose budget includes (or can be supplemented to include) commercial cloud, and the student wants to convert part of that budget into H200 training hours with reduced procurement friction and competent cost monitoring. For that scenario CloudBank is excellent. For any other scenario it is the wrong door to knock on, and direct cloud research credit programs (AWS Activate, Google Research Credits, Azure for Researchers) or NSF ACCESS allocations are better starting points.

= Summary table

#table(
  columns: 4,
  align: (left, center, center, center),
  table.header[Scenario][Typical H200-hour equivalent][Approval time][Effort],
  [PI writes CloudBank into new NSF proposal], [hundreds to tens of thousands], [9-12 months], [High],
  [CloudBank supplement to active CISE award], [\~1,000-5,000], [2-3 months], [Medium],
  [Onboard existing project funds], [varies with budget], [2-3 weeks], [Low],
  [Educational classroom account], [hundreds (CPU-heavy)], [2-4 weeks], [Low],
  [Grad student with no PI award], [zero], [n/a], [Not eligible],
)

#h200-note

= Sources

- CloudBank program site, services and eligibility, https://www.cloudbank.org/
- NSF Award #1925001, "CloudBank: Managed Services to Simplify Cloud Access for Computer Science Research and Education", https://www.nsf.gov/awardsearch/showAward?AWD_ID=1925001
- AWS EC2 P5 and P5e on-demand pricing, https://aws.amazon.com/ec2/instance-types/p5/ and https://aws.amazon.com/ec2/pricing/on-demand/
- Microsoft Azure ND H200 v5 series pricing and specs, https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/ndh200v5-series and https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/
- Google Cloud A3 Ultra (H200) and A3 Mega (H100) pricing, https://cloud.google.com/compute/gpus-pricing and https://cloud.google.com/blog/products/compute/introducing-a3-ultra-vms-with-nvidia-h200-gpus
- IBM Cloud GPU virtual servers, https://www.ibm.com/cloud/gpu

#v(1em)
#text(size: 9pt, fill: black70, style: "italic")[Pricing verified April 2026; commercial cloud rates change quarterly and reserved-instance discounts depend on contract terms negotiated through CloudBank.]
