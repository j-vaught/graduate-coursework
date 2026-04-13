#import "_style.typ": *
#show: report-setup.with(title: "University HPC", program: "University HPC (USC focus)")
#title-block(program: "University HPC Centers", tagline: "The fastest win — your own campus cluster, with a deep-dive on USC Hyperion")

= Why This Matters First

For most graduate students, the campus HPC center is the fastest, lowest-friction
compute pathway on the planet. Hardware is already paid for out of indirect-cost
recovery, capital reserves, or institutional research funds. There is no
competitive review, no merit panel, no narrative justification beyond an
advisor's signature. Onboarding is typically same-day or next-day. Wall-clock
time from "I should learn Slurm" to "my first job is queued on an A100" is
routinely under 48 hours.

This report argues that any grad student building a compute strategy should
investigate their home institution's HPC offering #emph[before] writing a
single federal proposal. NAIRR, ACCESS, INCITE, and ALCC are powerful
multipliers, but they are slower, more competitive, and more administratively
heavy. A campus cluster covers exploration, debugging, baseline runs, ablations,
and the long tail of small experiments that dominate the actual research
calendar. Federal allocations are then reserved for the few large-scale runs
that truly need them.

The same logic applies to industry credit programs. Google TRC, AWS Cloud
Credits for Research, and Azure for Researchers are excellent, but every hour
spent debugging a Docker container on a rented spot instance is an hour you
could have spent training on a node your tuition already paid for.

= The General University-HPC Landscape

Campus HPC centers in the United States cluster around three operational
models. Understanding which model your institution uses determines how you ask
for time, how much you get, and how predictable your queue waits are.

The #emph[condo model] is dominant at large land-grant and R1 systems.
Faculty PIs purchase nodes out of grant funds, and those nodes are integrated
into the central cluster. The PI gets priority access to the equivalent of what
they bought, and the broader user community gets cycle-scavenging access to
idle condo nodes through a low-priority preemptable queue. Examples include
Clemson Palmetto2, Purdue's community clusters, and Iowa State's Nova.

The #emph[open or institutional model] funds a shared pool centrally. Any
researcher with an advisor sponsor gets fair-share access. There is no
buy-in, but priority is uniform and queue depth at peak times can be painful.
Many smaller R1s and most R2s use this model.

The #emph[hybrid model] is the most common in practice. A central
institutional pool covers everyone, condo nodes layer on top for funded labs,
and a small "AI partition" or "GPU partition" is funded out of a recent NSF
MRI, NIH S10, or internal strategic-investment award. USC's current posture
fits this hybrid pattern, with Hyperion as the institutional backbone and
Theia as the strategic AI add-on.

== Typical GPU Tiers in 2026

Mid-size R1 campus clusters in the 2024--2026 refresh cycle now commonly carry
some mix of NVIDIA A100 (40 or 80 GB), H100 (80 GB), L40S (48 GB), and
RTX 6000 Ada (48 GB). H200 and B200 nodes are starting to appear at the
largest campuses but remain rare. Older V100 and P100 nodes from the
2018--2020 era are still in service at most sites and are perfectly adequate
for development, debugging, and small fine-tunes.

== Software, Storage, and Liaisons

Slurm is the de facto scheduler at almost every U.S. campus HPC. PBS Pro
survives at a handful of sites. Storage is universally tiered into a small
backed-up #emph[home] directory (typically 25--100 GB), a large
unbacked-up #emph[scratch] space with a purge policy (typically 1--10 TB
per user, purged after 30--90 days of inactivity), and a #emph[project]
or #emph[group] space that is either purchased or allocated by the
center. A #emph[Globus] endpoint is standard for moving data in and out.

The NSF-funded #emph[Campus Champions] program embeds a local liaison at
each member institution who can fast-track the user to ACCESS allocations and
broker introductions to other regional resources. Checking whether your campus
is a Campus Champion site is a 30-second exercise that often saves weeks of
proposal-writing later.

= USC Research Computing — Hyperion and Theia

USC Research Computing sits inside the Division of Information Technology and
operates three production clusters as of the 2025--2026 academic year. The
flagship general-purpose system is #emph[Hyperion], the new AI-focused
system is #emph[Theia], and the teaching-only cluster is
#emph[Bolden]. All three are managed under Bright Cluster Manager and
scheduled with Slurm.

== Hyperion (Phase III, in production since 2023)

Hyperion Phase III provisions 356 nodes totaling 16,616 CPU cores and a
peak of approximately 1.5 PFLOPS. The mix is roughly 295 standard compute
nodes, 44--45 GPU nodes, and 8 big-memory nodes. Compute and GPU nodes carry
128--256 GB of system RAM, big-memory nodes carry 2 TB. The interconnect is
EDR InfiniBand at 100 Gb/s, a step below the NDR-400 fabric used on Theia.

The GPU complement on Hyperion includes DGX-style nodes with 8x A100 GPUs
and older dual-V100 nodes. Storage consists of 450 TB of GPFS home space and
1.4 PB of GPFS scratch. Two dedicated data-transfer nodes serve as Globus
endpoints. Specific GPU partition names, per-user quota numbers, and condo
priority weights are not enumerated on the public RCI pages and should be
confirmed by emailing #raw("rci@mailbox.sc.edu") at account-creation time.

== Theia (NSF MRI-funded, AI-focused)

Theia is the newer, AI-targeted system, funded by an NSF Major Research
Instrumentation award to expand AI access across South Carolina institutions.
The published configuration is 28 CPU nodes at 112 cores each, 10 quad-GPU
nodes (nine quad-A100 nodes and one quad-H100 node), and 1.5 PB of GPFS
scratch over a 400 Gb/s NDR InfiniBand fabric. Aggregate is 3,808 CPU cores
and approximately 675 combined CPU+GPU TFLOPS at peak. Theia is the
recommended target for any modern AI/ML workload at USC.

== Bolden (teaching)

Bolden is a 20-node teaching cluster with 460 cores and 300 TB of Lustre
scratch. It is reserved for course use and is not a research target.

== Support and Training

The RCI team runs periodic Slurm and HPC-onboarding sessions through DoIT and
the AI Institute, and offers consulting hours by appointment. The general
contact for accounts, allocations, and consulting is
#raw("rci@mailbox.sc.edu"). Faculty in CSE, the AI Institute, and the College
of Engineering and Computing have standing relationships with the RCI staff
and can usually broker an introduction.

= Hardware Specs at a Mid-Size R1

The table below summarizes the GPU types most likely to appear on a mid-size
R1 campus cluster in 2026. The FP16/BF16 column is dense tensor throughput
without sparsity, directly comparable to the 989 TFLOPS H200 baseline used
elsewhere in this report series. The right-hand column is a typical node count
of that GPU type at a mid-size R1, useful for estimating queue depth.

#table(
  columns: (1.2fr, auto, auto, auto, auto),
  align: (left, right, right, right, right),
  table.header[GPU model][VRAM (GB)][FP16 TFLOPS][BW (TB/s)][Typical nodes],
  [V100 SXM2], [32], [125], [0.90], [4--12],
  [RTX 6000 Ada], [48], [364], [0.96], [2--8],
  [L40S], [48], [362], [0.86], [2--8],
  [A100 40GB], [40], [312], [1.55], [4--16],
  [A100 80GB], [80], [312], [2.04], [2--12],
  [H100 SXM5], [80], [989], [3.35], [1--8],
  [H200 SXM5], [141], [989], [4.80], [0--2],
)

USC's current footprint slots into this picture at the A100-heavy end. Theia's
quad-A100 nodes plus its single quad-H100 node are well-aligned with what a
typical mid-size R1 carries, with Hyperion's DGX A100 chassis and V100 nodes
filling out the older tier.

= Allocation Model and Throughput Estimate

Campus clusters almost never price allocations in service-unit hours the way
ACCESS or INCITE do. Instead, they allocate by Slurm fair-share weights and
partition membership. A new grad student joining an unfunded lab gets baseline
fair-share, can submit to any open partition, and is preempted on condo
partitions when the owning PI submits. A student in a funded lab inherits the
PI's fair-share weight and any condo priority the PI has purchased.

For the purpose of this report series, the question is realistic
#emph[steady-state throughput] over a 90-day semester. A new USC student
on Theia or Hyperion can plausibly hold 1--2 A100 GPUs continuously without
preemption, with bursts to 4--8 A100s for shorter runs. The table below
converts steady-state occupancy into H200-hour equivalents using the 312
TFLOPS A100 vs 989 TFLOPS H200 ratio (approximately 0.316 H200-hour per
A100-hour).

#table(
  columns: (auto, auto, auto, auto),
  align: (right, left, right, right),
  table.header[Steady GPUs][GPU type][A100-hours / 90 days][H200-hour equiv],
  [1], [A100 40/80GB], [2,160], [681],
  [2], [A100 40/80GB], [4,320], [1,363],
  [4], [A100 40/80GB], [8,640], [2,725],
  [8], [A100 40/80GB], [17,280], [5,450],
  [4], [H100 80GB], [8,640], [8,640],
  [8], [H100 80GB], [17,280], [17,280],
)

The two A100-row example matches the canonical estimate. Steady 2x A100 over
90 days yields 90 x 24 x 2 x 312 / 989 approximately 1,362 H200-hours, an
allocation envelope that is comparable to a small NAIRR Start-Up grant
delivered with zero proposal overhead.

= Approval Timeline

Account creation at USC RCI is form-driven. The user submits the account
request through the DoIT Research Computing portal, the listed advisor or PI
approves by email, the user completes a short training module on cluster
etiquette and Slurm basics, and SSH keys are provisioned. End-to-end
turnaround is typically 1--3 business days for a routine request and rarely
exceeds a week. There is no committee, no scoring rubric, and no narrative
proposal.

= Eligibility

Any USC researcher with an active appointment and an advisor sponsor is
eligible. This includes graduate students, postdocs, undergraduate research
assistants, and visiting scholars. The default partitions on Hyperion and
Theia carry no per-user cost. Priority partitions tied to condo investments
require the owning PI to add the user to their group. Course-only access on
Bolden is granted to enrolled students through the instructor.

= Things to Know

Campus storage quotas tend to bite well before compute does. Home directories
in the 25--100 GB range fill quickly with conda environments, model
checkpoints, and pip caches. Plan to keep working data on scratch and to set
up a project-space request early if the workflow exceeds 1--2 TB.

GPU-partition queue waits at peak times such as paper-deadline season can run
from hours to several days. The unwritten rule at most campus clusters is to
develop and debug interactively on a single GPU, then submit batch arrays
during off-peak windows.

USC's status as an ACCESS Campus Champion site is worth verifying with RCI
directly. If USC is a member, the local liaison can fast-track an ACCESS
Explore allocation, which is the natural next step after exhausting campus
fair-share. Combining campus HPC with NAIRR Start-Up and AFMR credits is the
recommended stack for a grad student in 2026, with each layer covering a
different scale of run.

Campus IT often subsidizes a quota of consulting hours with RCI staff. Use
them early. A 30-minute conversation about how Slurm is actually configured
locally saves weeks of trial-and-error. Some campuses also run a graduate
seed-grant program that bundles a small compute allocation with mentoring;
checking the AI Institute and the Office of the Vice President for Research
for current calls is worth a single email.

= Strategic Fit

The campus HPC is the first compute pathway any USC grad student should
exercise. Zero competitive overhead, immediate access, and a moderate but
real H200-hour-equivalent throughput over a semester make it the workhorse
layer in any sensible compute strategy. Use Hyperion and Theia for everything
that fits, and reserve external programs covered elsewhere in this report
series for the runs that genuinely outgrow the campus envelope.

= Summary Table

The scenarios below assume a single grad-student user on USC Theia or
Hyperion, sustaining the listed concurrency over a 90-day semester. Effort is
the wall-clock cost of obtaining and maintaining the allocation, not the
science work itself.

#table(
  columns: (auto, auto, auto, auto, auto),
  align: (left, left, right, left, left),
  table.header[Scenario][GPU type][H200-hr equiv / sem][Approval time][Effort],
  [1 GPU steady], [A100 40/80GB], [681], [1--3 days], [Trivial],
  [2 GPU steady], [A100 40/80GB], [1,363], [1--3 days], [Trivial],
  [4 GPU steady], [A100 40/80GB], [2,725], [1--3 days], [Low],
  [8 GPU steady], [A100 40/80GB], [5,450], [1--3 days + condo], [Low--Mod.],
  [4 GPU steady], [L40S 48GB], [3,160], [1--3 days], [Low],
  [4 GPU steady], [H100 80GB], [8,640], [1--3 days + queue], [Low],
  [8 GPU steady], [H100 80GB], [17,280], [1--3 days + condo], [Moderate],
)

#h200-note

= Sources

Verified April 2026 via WebSearch and WebFetch against USC DoIT Research
Computing pages and adjacent USC sources.

- USC DoIT Research Computing, Resources page. #link("https://sc.edu/about/offices_and_divisions/division_of_information_technology/rc/resources/")
- USC DoIT Research Computing, Hyperion Phase III in production (2023). #link("https://sc.edu/about/offices_and_divisions/division_of_information_technology/rc/news/2023/phasethree_hyperion.php")
- USC DoIT Research Computing, news index. #link("https://sc.edu/about/offices_and_divisions/division_of_information_technology/rc/news/")
- USC DoIT Research Computing, landing page. #link("https://sc.edu/about/offices_and_divisions/division_of_information_technology/rc/index.php")
- USC College of Engineering and Computing, AI Institute Facilities. #link("https://research.cec.sc.edu/aii/facilities")
- USC CSE, NSF MRI award announcement (Theia). #link("https://www.cse.sc.edu/research/news/usc-awarded-nsf-mri-grant-acquire-hpc-cluster-ai-science-research-and-education-south")
- ACCESS Campus Champions program directory. #link("https://campuschampions.cyberinfrastructure.org/")
- Primary contact for accounts and allocations: #raw("rci@mailbox.sc.edu")
