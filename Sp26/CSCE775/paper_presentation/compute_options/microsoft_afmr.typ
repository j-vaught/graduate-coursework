#import "_style.typ": *
#show: report-setup.with(title: "Microsoft AFMR", program: "Microsoft AFMR + Azure for Research")
#title-block(program: "Microsoft AFMR & Azure for Research", tagline: "Azure credits for frontier-model and AI-for-science research — OpenAI API access included")

= Program Overview

The Microsoft Research _Accelerating Foundation Models Research_ (AFMR)
program is the principal channel through which Microsoft distributes Azure
compute and Azure OpenAI API quota to academic researchers working on
foundation models. Launched in late 2023 and expanded materially through
2024 and 2025, AFMR funds projects in four broad themes. Aligning AI with
human goals and values, improving the reliability and safety of foundation
models, accelerating scientific discovery in the natural and life sciences,
and broadening societal benefit including health, sustainability, and
accessibility. Awards are issued as Azure credit grants paired, where
relevant, with managed Azure OpenAI Service quota covering GPT-4o, GPT-4.1,
the o-series reasoning models, and selected open-weight models hosted on
Azure AI Foundry.

The older _Azure for Research_ banner historically offered smaller, broader
awards distributed through Microsoft Research Outreach. That program has
largely been folded into AFMR for foundation-model work and into the Azure
sponsorship program for traditional cloud research, so new applicants
should default to AFMR. The _Microsoft AI for Good_ research lab runs a
separate engagement model centered on direct collaboration with Microsoft
researchers on humanitarian and sustainability projects, and occasionally
co-funds AFMR proposals that align with its mission. AFMR runs on a themed
call cadence, with three to four open calls per year, and a permanent
public RFP page for general submissions between calls.

= Hardware Specs

Azure exposes foundation-model GPUs through the _ND_ (high-bandwidth,
multi-GPU) and _NC_ (single-tenant, smaller) VM families. Pricing varies by
region and contract term. The on-demand and one-year reserved figures
below are normalized to a per-GPU-hour basis from published Azure list
prices for East US 2 and South Central US, where Hopper-class capacity
concentrates. Spot pricing typically runs 40--70\% below on-demand but is
preemptible and not available in every region.

#table(
  columns: (1.2fr, auto, auto, auto, auto, 1.2fr, auto, auto),
  align: (left, left, right, right, right, left, right, right),
  table.header[VM size][GPUs][VRAM (GB)][FP16 TFLOPS][BW (TB/s)][Interconnect][On-dem \$/GPU-hr][1-yr \$/GPU-hr],
  [ND H200 v5], [8 × H200 SXM], [141], [989], [4.80], [NVLink-4 900 GB/s + 8 × NDR 400 Gbps], [~9.00], [~4.50],
  [ND H100 v5], [8 × H100 SXM], [80], [989], [3.35], [NVLink-4 900 GB/s + 8 × NDR 400 Gbps], [~6.98], [~3.85],
  [NDv4 (A100 80GB)], [8 × A100 SXM4], [80], [312], [2.00], [NVLink-3 600 GB/s + 8 × HDR 200 Gbps], [~3.67], [~2.10],
  [NC A100 v4], [1--4 × A100 PCIe], [80], [312], [1.94], [PCIe Gen4, no NVLink], [~3.40], [~2.00],
  [ND MI300X v5], [8 × AMD MI300X], [192], [1307], [5.30], [Infinity Fabric 896 GB/s + 8 × NDR 400 Gbps], [~7.20], [~3.90],
)

The _MI300X_ row is included because AFMR explicitly invites proposals on
AMD silicon and Microsoft has been actively building out MI300X capacity in
South Central US through 2025--2026. The 192 GB HBM3 per GPU is the
largest single-package memory currently available on Azure and is
attractive for long-context inference, large mixture-of-experts routing,
and activation-heavy training, but the software stack is _ROCm_ rather
than CUDA and porting effort is non-trivial.

= AFMR Allocation Size

AFMR awards are issued as Azure credit balances, sized to the proposal
rather than to a fixed tier. Routine thematic-call awards land in the
\$10k--\$40k range, with larger flagship calls (notably the science
acceleration and safety themes) occasionally reaching ~\$80k for
multi-investigator teams. Azure OpenAI API quota is granted separately as
tokens-per-minute and requests-per-minute caps against named deployments,
and does not draw down the compute credit balance.

The conversion below maps a dollar credit to _H200-hours_ on ND H200 v5,
under three pricing scenarios. On-demand uses the ~\$9/GPU-hr list rate;
one-year reserved uses ~\$4.50/GPU-hr; spot is illustrated at ~\$2.70/GPU-hr
(roughly 70\% below on-demand) and is appropriate for checkpointable
training runs only.

#table(
  columns: (auto, auto, auto, auto),
  align: (right, right, right, right),
  table.header[Credit award][On-demand H200-hr][1-yr reserved H200-hr][Spot H200-hr],
  [\$10,000], [~1,111], [~2,222], [~3,704],
  [\$25,000], [~2,778], [~5,556], [~9,259],
  [\$40,000], [~4,444], [~8,889], [~14,815],
  [\$80,000], [~8,889], [~17,778], [~29,630],
)

A typical \$25k thematic award therefore funds roughly 2,800 H200-hours of
on-demand 8-GPU training, or about 5,500 H200-hours under a one-year
reservation. For comparison, that is enough to fine-tune a 13B-parameter
dense transformer on ~50B tokens at industry utilization, or to run several
hundred 7B-class supervised fine-tuning sweeps. Spot pricing roughly
doubles the budget again for resumable workloads.

= Approval Timeline

AFMR runs themed _calls_ rather than rolling submission. Each call posts a
short description, a deadline (typically four to six weeks out), and a
target award range. From submission to award notice is generally four to
eight weeks, with the Azure subscription provisioning and OpenAI quota
ticket landing one to two weeks after notification. Researchers should
plan for roughly two to three months from initial proposal to first
GPU-hour billed.

The proposal itself is lightweight. Two to four pages of research
description, a one-paragraph compute and quota budget, short team
biographies, and an institutional contact are the standard package.
Letters of support are not required. There is no indirect cost recovery
because the award is in-kind cloud credit rather than cash.

= Eligibility

AFMR is open to academic researchers globally at accredited institutions,
which is unusually permissive among foundation-model compute programs.
Faculty PIs are the default applicant class, and postdocs may apply with a
faculty co-PI. _Graduate students_ may serve as PI on certain themed calls
when Microsoft explicitly opens the call to students; otherwise they
participate as named team members under a faculty PI. All AFMR projects
must commit to open publication of results, and use of the Azure OpenAI
Service requires accepting Microsoft's data-use and responsible-AI
agreements, including content filtering, abuse monitoring, and a
prohibition on using outputs to train competing models without separate
agreement.

= Things to Know

AFMR is currently the most accessible path for an academic researcher to
obtain ND H200 v5 capacity together with GPT-4-class API access in a
single grant, and the proposal burden is among the lowest in the field.
Several practical points materially affect how the award is used. _Awards
expire twelve months from activation_, with no rollover, so a burn
schedule should be drafted before the subscription is provisioned. _Azure
egress is not free_, and a multi-terabyte dataset moved out of region or
out of cloud can quietly consume 5--15\% of the credit pool; staging
datasets in the same region as the compute is essential. _Multi-region
ND H200 v5 availability is uneven_, with East US 2 and South Central US
the most reliable through 2025--2026 and other regions occasionally
queuing for capacity. Microsoft requests, but does not require, that
resulting publications acknowledge AFMR by name, and the program team
tracks acknowledgments when scoping subsequent calls. The _MI300X_ tier
is attractive for memory-bound work but locks the codebase to _ROCm_, so
proposals should budget engineering time accordingly.

= Strategic Fit

For a graduate AI researcher building agentic, evaluation, or
foundation-model research, AFMR is best paired with the NAIRR Pilot's
Azure pathway. NAIRR delivers a federally reviewed Azure credit through
the NAIRR Deep Partnership track, while AFMR delivers a thematically
reviewed Azure credit plus Azure OpenAI quota directly from Microsoft
Research. Combined, the two programs realistically yield 3,000--5,000
H200-hours per year for a single grad student with a faculty PI, plus
substantial GPT-4-class API quota for evaluation harnesses and
agent-loop experiments. Where an advisor already holds an active NSF
award, _CloudBank_ is the right wrapper for cost-managed Azure spend
outside the AFMR award. The combination of AFMR (in-kind credit + API),
NAIRR (federal Azure pathway), and CloudBank (NSF-funded paid Azure)
covers the full spectrum from prototype to production training without
requiring on-prem capacity.

= Summary

#table(
  columns: (1.4fr, auto, auto, auto, 1.2fr),
  align: (left, right, right, left, left),
  table.header[Tier / program][On-dem H200-hr][1-yr H200-hr][Approval][Best use],
  [AFMR thematic, \$10k], [~1,111], [~2,222], [4--8 wk], [Pilot fine-tunes, eval harnesses],
  [AFMR thematic, \$25k], [~2,778], [~5,556], [4--8 wk], [Mid-scale SFT, RLHF on 7B],
  [AFMR thematic, \$40k], [~4,444], [~8,889], [4--8 wk], [13B-class fine-tune, ablations],
  [AFMR flagship, \$80k], [~8,889], [~17,778], [6--10 wk], [Multi-PI training campaigns],
  [Azure OpenAI quota], [n/a], [n/a], [Bundled], [GPT-4o / o-series eval, agents],
  [AI for Good engagement], [Variable], [Variable], [3--6 mo], [Humanitarian, sustainability],
)

#h200-note

= Sources

#set text(size: 9pt)
- AFMR program home and themed calls: #link("https://www.microsoft.com/en-us/research/collaboration/accelerating-foundation-models-research/")[microsoft.com/research/collaboration/accelerating-foundation-models-research]
- AFMR RFP and submission portal: #link("https://www.microsoft.com/en-us/research/collaboration/accelerating-foundation-models-research/rfp/")[AFMR RFP] · #link("https://www.microsoft.com/en-us/research/academic-program/accelerate-foundation-models-research/")[AFMR academic program]
- Azure ND H200 v5 product page and pricing: #link("https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/ndh200v5-series")[ND H200 v5] · #link("https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/")[Azure VM pricing]
- Azure ND H100 v5 product page: #link("https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/ndh100v5-series")[ND H100 v5]
- Azure NDv4 (A100) product page: #link("https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/nda100v4-series")[NDv4 A100]
- Azure ND MI300X v5 announcement: #link("https://techcommunity.microsoft.com/t5/azure-high-performance-computing/announcing-general-availability-of-azure-nd-mi300x-v5-vms/ba-p/4145152")[ND MI300X v5 GA]
- Azure OpenAI Service quotas and models: #link("https://learn.microsoft.com/en-us/azure/ai-services/openai/quotas-limits")[OpenAI quotas] · #link("https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models")[OpenAI models]
- Microsoft AI for Good Research Lab: #link("https://www.microsoft.com/en-us/research/group/ai-for-good-research-lab/")[AI for Good]
- NAIRR Microsoft Azure contribution: #link("https://www.microsoft.com/en-us/research/project/national-ai-research-resource-nairr-pilot/")[Microsoft Research NAIRR]
