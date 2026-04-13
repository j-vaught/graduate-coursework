#import "_style.typ": *
#show: report-setup.with(title: "AWS Research", program: "AWS Cloud Credit for Research")
#title-block(program: "AWS Cloud Credit for Research", tagline: "Application-based AWS credits for academic research — scales with justification")

= Program Overview

Amazon Web Services has run an academic credit program under several names
since 2013. The original _AWS Cloud Credit for Research_ accepted open
proposals against a public application form, but in 2022 AWS retired the
public intake and folded the program into a smaller set of more tightly
managed channels. As of the 2024--2026 cycle, the practical paths into AWS
research credits are three. The first is the _AWS Promotional Credits for
Research_ track, which is functionally the successor to the old Cloud
Credit for Research program but is now routed through institutional AWS
contacts and account managers rather than a public form. The second is the
_AWS Research and Educational Program_ request, a managed-account-level
credit grant for accredited institutions that an AWS account manager (or
a sponsoring AWS Solutions Architect) submits internally on behalf of the
researcher. The third is the _AWS IMAGINE Grant_ for nonprofits, which
issues larger awards (frequently \$50k--\$150k in credits plus
professional services) to mission-driven organizations including
university research centers; the IMAGINE Grant runs an annual public RFP
and is the most discoverable of the three.

Two adjacent programs are worth knowing because they are frequently
conflated with the credit programs but are operationally distinct. The
_AWS Generative AI Innovation Center_ runs academic engagements that
pair a research group with an AWS applied scientist team for a
multi-week prototyping sprint; credits may be bundled, but the
deliverable is consulting time rather than a pure compute allocation, and
intake is by referral. The _AWS Diagnostic Development Initiative_,
launched in 2020 with an initial \$20M commitment for COVID-era
diagnostics research, was extended through public-health and
infectious-disease use cases and remains active as of early 2026 with a
narrower scope; it issues credits and technical support against
disease-surveillance and diagnostics proposals. _AWS Build On_ is a
separate educational tier aimed at student builders and hackathons,
typically issuing \$25--\$300 in credits per participant rather than
research-grade allocations.

= Hardware Specs

The table below lists the AI-relevant accelerated instance families on
AWS as of the 2026 EC2 catalog. Per-GPU on-demand and 1-year
standard-reserved prices are computed by dividing the published instance
list price (us-east-1) by the GPU count, rounded to the nearest dollar.
The TFLOPS column is dense FP16/BF16 tensor throughput without sparsity,
directly comparable to the 989 TFLOPS H200 baseline used elsewhere in
this report. Trainium and Inferentia entries report BF16 dense throughput
because those parts have no FP16 tensor mode in the conventional sense.

#table(
  columns: (auto, auto, auto, auto, auto, auto, auto),
  align: (left, center, right, right, right, right, right),
  table.header[Instance][GPUs][VRAM (GB)][FP16/BF16 TFLOPS][BW (TB/s)][On-demand \$/GPU-hr][1-yr RI \$/GPU-hr],
  [p5.48xlarge (H100)], [8], [80], [989], [3.35], [\$12.29], [\$7.57],
  [p5e.48xlarge (H200)], [8], [141], [989], [4.80], [\$11.06], [\$5.07],
  [p5en.48xlarge (H200)], [8], [141], [989], [4.80], [\$11.57], [\$5.71],
  [p4d.24xlarge (A100 40)], [8], [40], [312], [1.55], [\$4.10], [\$2.55],
  [p4de.24xlarge (A100 80)], [8], [80], [312], [2.00], [\$5.12], [\$3.20],
  [g6e.48xlarge (L40S)], [8], [48], [362], [0.86], [\$3.04], [\$1.92],
  [g6.48xlarge (L4)], [8], [24], [121], [0.30], [\$1.78], [\$1.10],
  [g5.48xlarge (A10G)], [8], [24], [125], [0.60], [\$2.06], [\$1.30],
  [trn1.32xlarge (Trainium1)], [16], [32], [190], [0.82], [\$1.36], [\$0.85],
  [trn2.48xlarge (Trainium2)], [16], [96], [667], [2.90], [\$3.12], [\$1.95],
  [inf2.48xlarge (Inferentia2)], [12], [32], [191], [0.82], [\$1.05], [\$0.66],
)

The dominant cost-per-FLOP winners for training are Trainium2 and the
H200-based p5e family, which is why most credit-funded H100/H200
training campaigns in 2025--2026 target p5e specifically rather than the
older p5 (H100) or p4d (A100) families. The g6e family with L40S is the
most cost-effective option for fine-tuning and inference workloads that
fit in 48 GB per GPU.

= Credit Amount and H200-Hour Equivalence

Research-tier awards in 2024--2026 cluster around \$5k--\$20k for first-time
PI requests, \$25k--\$50k for follow-on awards backed by publications, and
\$50k--\$100k+ for IMAGINE grants or institutionally-sponsored multi-year
engagements. The _H200-hour equivalence_ of a credit award is highly
sensitive to which purchasing mode the researcher uses. The table below
converts each award tier to H200-hours on p5e (the dominant H200
instance) and on p4d (A100 reference) under on-demand, 1-year reserved,
and spot pricing. Spot prices are taken at the 2025--2026 average of
roughly 60% off on-demand for p5e (when capacity is available) and
roughly 70% off for p4d.

#table(
  columns: (auto, auto, auto, auto, auto, auto),
  align: (left, right, right, right, right, right),
  table.header[Award][p5e on-dem.][p5e 1-yr RI][p5e spot][p4d on-dem.][p4d spot],
  [\$5,000], [452 hr], [986 hr], [1,131 hr], [1,220 hr], [4,065 hr],
  [\$10,000], [904 hr], [1,972 hr], [2,262 hr], [2,439 hr], [8,130 hr],
  [\$25,000], [2,261 hr], [4,931 hr], [5,654 hr], [6,098 hr], [20,325 hr],
  [\$50,000], [4,521 hr], [9,862 hr], [11,308 hr], [12,195 hr], [40,650 hr],
  [\$100,000], [9,042 hr], [19,724 hr], [22,617 hr], [24,390 hr], [81,301 hr],
)

== Worked Conversions

A \$5,000 award spent at the p5e on-demand list price of \$11.06/GPU-hr
yields $5000 / 11.06 approx 452$ H200-hours. The same \$5,000 spent
against a 1-year standard-reserved p5e at \$5.07/GPU-hr (the lowest
no-upfront RI rate published in 2026) yields about 986 H200-hours, more
than doubling the throughput per dollar at the cost of a 12-month
commitment that most credit awards cannot fully fund. Spot capacity on
p5e, when available, sits near \$4.42/GPU-hr (a roughly 60% discount on
on-demand) and yields about 1,131 H200-hours per \$5,000, but
availability is thin in the popular us-east-1 and us-west-2 regions and
preemption mid-job is common. A \$25,000 award on p5e on-demand is
roughly $25000 / 11.06 approx 2261$ H200-hours, which is enough to
fine-tune several 70B-class models with LoRA or to do a single
~7B-parameter pretraining run on a few tens of billions of tokens at
realistic utilization. The same \$25,000 stretched onto p4d spot yields
roughly 20,325 A100-hours of compute, equivalent to about 6,400
H200-hours after the FP16-throughput correction
($20325 times 312 / 989 approx 6411$), which is the largest effective
allocation any of the three tiers produces and the standard recipe for
running large fine-tuning sweeps on academic credits.

= Approval Timeline

The current AWS process is slower and less predictable than the
NSF-side programs. A typical Promotional Credits for Research request
moves through three steps. First, the PI contacts an institutional AWS
account manager (most R1 universities have one) or a regional AWS
Public Sector representative. Second, the PI submits a 2--3 page
proposal that includes the research question, an architecture sketch,
a line-itemed AWS budget keyed to specific SKUs, the AWS account ID
that will receive the credits, and a one-page PI CV. Third, the
account manager routes the request internally to AWS Research Programs
for review. End-to-end turnaround is typically 4--8 weeks for a
\$5k--\$25k request and 8--12 weeks for a \$50k+ request, with longer
queues around AWS re:Invent (late November through January) and the
end of AWS's fiscal year (June--July). IMAGINE Grant decisions follow
the public RFP cycle and are announced annually, with awards typically
issued 6--10 weeks after the application deadline.

= Eligibility

Eligible applicants are faculty, postdocs, and graduate students at
accredited academic institutions and qualifying nonprofit research
organizations worldwide, though U.S.-based institutions move through the
process noticeably faster. There is an explicit open-publication
expectation. Resulting work should be submitted for peer review or
posted to a public preprint server, and AWS asks for an acknowledgment
in the resulting paper. Credits are deposited as time-limited
promotional credits on the requester's AWS account and almost always
expire 12 months from the issue date with no rollover; unused credits
simply lapse. Credits cannot be transferred between accounts, cannot be
applied retroactively to past usage, and cannot be redeemed for cash or
support contracts.

= Things to Know

Several practical points materially affect how to use AWS credits.
First, _credits do not cover every SKU_. AWS Marketplace third-party
software (including some packaged ML container images), AWS Support
plans above Basic, Reserved Instance upfront payments, and certain
premium services (notably some Outposts and dedicated-host SKUs) are
excluded; the exclusion list is published in the credit terms and
should be cross-checked before budget commitment. Second, _egress fees
are the silent killer_. Pulling a multi-terabyte trained model or
dataset out of S3 to an on-prem cluster at the published \$0.09/GB
egress rate can consume 20--40% of a small credit award; researchers
who plan to keep artifacts inside AWS (S3 to SageMaker to EC2) avoid
this almost entirely.

Third, _quota for p5, p5e, p5en, and p4d is gated_. New AWS accounts
have a default vCPU quota of 0 for the relevant capacity-block
families, and a Service Quotas request must be filed and approved
before the first instance can launch. Approval typically takes 1--3
weeks, occasionally longer when global H100/H200 supply is tight, and
the request must justify the requested concurrent vCPU count against
the project plan. Fourth, _spot p5e availability is genuinely thin_. On
many days in 2025--2026, p5e spot was simply not available in
us-east-1 or us-west-2 regardless of bid; the workable fallbacks are
p5 (H100) spot, p4d (A100) spot, or scheduled _Capacity Blocks for ML_,
which are reservation-style purchases priced between on-demand and RI
and typically available 1--14 days out. Finally, the _Generative AI
Innovation Center_ academic engagement is more consulting than pure
credits. The AWS team co-develops the prototype and any bundled
credits cover the prototype's compute footprint, not an open-ended
research budget; treat it as a partnership channel rather than a
credit program.

= Strategic Fit

For a graduate AI researcher who needs Hopper-class compute and
already has a NAIRR Pilot allocation, AWS credits are the natural
backup channel. More dollars tend to convert to more H200-hours than
NAIRR's bounded DGX Cloud allocation does, especially when spent on
1-year reserved p5e or on p4d spot, and the SKU catalog is broader
than any single NAIRR provider. The trade-offs are the slower 4--8 week
approval, the cold-start tax of the Service Quotas request, and the
12-month credit-expiration window. The recommended pattern is to apply
for NAIRR Start-Up first (turnaround under three weeks), use NAIRR
Research for the bulk of H100/H200 training, and submit an AWS
Promotional Credits for Research request in parallel as a
quota-isolated backup that becomes available for elasticity bursts and
post-NAIRR continuation work. Pair the AWS account with _CloudBank_
billing dashboards (or AWS-native Cost Explorer plus Budgets) to
monitor burn rate against the 12-month expiration clock; a credit
unspent at month 12 is simply forfeited.

= Summary

#table(
  columns: (auto, auto, auto, auto, auto, auto),
  align: (left, right, right, right, auto, auto),
  table.header[Credit tier][On-demand H200-hr][1-yr RI H200-hr][Spot H200-hr][Approval][Effort],
  [\$5k (first-time)], [~452], [~986], [~1,131], [4--6 wk], [Low],
  [\$10k (follow-on)], [~904], [~1,972], [~2,262], [4--6 wk], [Low],
  [\$25k (with publication)], [~2,261], [~4,931], [~5,654], [6--8 wk], [Medium],
  [\$50k (institutional)], [~4,521], [~9,862], [~11,308], [8--10 wk], [Medium],
  [\$100k (IMAGINE / GenAI IC)], [~9,042], [~19,724], [~22,617], [10--14 wk], [High],
)

#h200-note

= Sources

#set text(size: 9pt)
- AWS Cloud Credit for Research and successor programs: #link("https://aws.amazon.com/government-education/research-and-technical-computing/cloud-credit-for-research/")[aws.amazon.com/government-education/research-and-technical-computing/cloud-credit-for-research/]
- AWS IMAGINE Grant for nonprofits: #link("https://aws.amazon.com/government-education/nonprofits/aws-imagine-grant-program/")[aws.amazon.com/government-education/nonprofits/aws-imagine-grant-program/]
- AWS Generative AI Innovation Center: #link("https://aws.amazon.com/ai/generative-ai/innovation-center/")[aws.amazon.com/ai/generative-ai/innovation-center/]
- AWS Diagnostic Development Initiative: #link("https://aws.amazon.com/government-education/nonprofits/disaster-response/diagnostic-development-initiative/")[aws.amazon.com/government-education/nonprofits/disaster-response/diagnostic-development-initiative/]
- EC2 P5/P5e/P5en (H100/H200) instance and pricing pages: #link("https://aws.amazon.com/ec2/instance-types/p5/")[/ec2/instance-types/p5] · #link("https://aws.amazon.com/ec2/pricing/on-demand/")[/ec2/pricing/on-demand]
- EC2 P4d/P4de (A100), G5/G6/G6e (A10G/L4/L40S), Trn1/Trn2 (Trainium), Inf2 (Inferentia2) instance pages: #link("https://aws.amazon.com/ec2/instance-types/p4/")[/p4] · #link("https://aws.amazon.com/ec2/instance-types/g6e/")[/g6e] · #link("https://aws.amazon.com/ec2/instance-types/trn2/")[/trn2] · #link("https://aws.amazon.com/ec2/instance-types/inf2/")[/inf2]
- EC2 Capacity Blocks for ML: #link("https://aws.amazon.com/ec2/capacityblocks/")[aws.amazon.com/ec2/capacityblocks/]
- AWS Service Quotas (P5/P5e/P4d vCPU quota requests): #link("https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html")[docs.aws.amazon.com/servicequotas/]
- Hardware specs cross-checked against NVIDIA H100, H200, A100, A10G, L4, L40S datasheets and AWS Trainium2 / Inferentia2 product briefs. On-demand pricing verified against the AWS pricing pages in us-east-1 (2024--2026); spot multipliers derived from EC2 Spot Instance Advisor historical averages.
