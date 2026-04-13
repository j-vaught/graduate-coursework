#import "_style.typ": *
#show: report-setup.with(title: "OSG", program: "OSG / OSPool")
#title-block(program: "Open Science Pool (OSPool)", tagline: "Free high-throughput computing via opportunistic scavenger pool — great for embarrassingly-parallel ML workloads")

= Program Overview

The Open Science Grid (OSG) operates the _Open Science Pool_ (OSPool), a
nationally distributed pool of opportunistic compute resources contributed
by United States universities, national laboratories, and a handful of
international partners. Resources are aggregated and scheduled through
HTCondor, and jobs are matched to whichever site happens to have idle
capacity when the user submits. The pool is explicitly _high-throughput_
rather than _high-performance_. It is engineered around large numbers of
small, independent jobs that can be re-run if preempted, not around tightly
coupled MPI codes that require a low-latency fabric.

OSPool is free to use for United States open-science research, with no
allocation request, no peer review, and no cost share. The service is
governed by the OSG Partnership, a consortium led by the University of
Wisconsin-Madison Center for High Throughput Computing (CHTC), the
University of Chicago, the University of Nebraska-Lincoln Holland Computing
Center, the University of California San Diego (UCSD), and Syracuse
University, with additional contributing sites at Florida, Clemson, Purdue,
Caltech, and many others. Users access the pool through an _Access Point_
(AP) such as OSG Connect (`ap40.uw.osg-htc.org`), the CHTC submit nodes,
or a campus AP federated into the pool.

= Hardware Specs

OSPool is highly heterogeneous because each contributing site donates
whatever spare cycles it has at any given moment. CPU jobs are abundant and
land on a wide range of Intel and AMD nodes. GPU availability is a strict
subset of sites and a strict subset of nodes within those sites. The table
below lists the GPU types most frequently observed on the OSPool dashboard
during 2024--2026, with dense FP16 tensor throughput stated without
sparsity for direct comparison against the 989 TFLOPS H200 SXM baseline.

#table(
  columns: (auto, auto, auto, auto, auto, auto),
  align: (left, right, right, right, left, left),
  table.header[GPU][VRAM (GB)][FP16 TFLOPS][BW (TB/s)][Per-job limit][Preemption risk],
  [A100 80GB], [80], [312], [2.04], [1 GPU], [Low--medium],
  [A100 40GB], [40], [312], [1.55], [1 GPU], [Low--medium],
  [A40], [48], [150], [0.70], [1 GPU], [Medium],
  [V100], [16/32], [125], [0.90], [1--2 GPU], [Medium],
  [P100], [16], [21], [0.73], [1--2 GPU], [Low],
  [RTX 3090], [24], [142], [0.94], [1 GPU], [High],
  [RTX 2080 Ti], [11], [108], [0.62], [1--2 GPU], [High],
  [T4], [16], [65], [0.32], [1--2 GPU], [Medium],
)

The dominant GPU classes in steady state are V100, RTX 2080 Ti, and T4.
A100 capacity exists but is contended, and H100 / H200 nodes are
essentially absent from the opportunistic pool. Memory per CPU core
typically caps at 8--16 GB, and per-job disk in `$_CONDOR_SCRATCH_DIR` is
usually bounded near 20--75 GB depending on site.

= Allocation Model

There is no fixed allocation. A user with an Access Point account submits
HTCondor jobs and they begin matching against idle slots within minutes.
Per-job constraints are imposed in lieu of a project quota. Wallclock is
typically capped at 24 hours, with most sites preferring jobs under 10
hours so that preemption losses stay bounded. Memory is typically capped
near 16 GB per core, jobs are single-node only (no MPI across nodes), and
persistent storage is _not_ provided — input and output staging is handled
through the _Open Science Data Federation_ (OSDF), which caches data near
the execution site for the lifetime of the job.

GPU jobs are subject to additional limits. A user is normally restricted
to one GPU per job and a small number of concurrent GPU slots (often
20--100 in practice for a single submitter, occasionally more). CPU
throughput is far more elastic. A well-formed CPU workload can routinely
saturate several thousand cores during a sustained burn, yielding tens of
thousands of CPU-core-hours per day with no formal request. GPU-hours
arrive more slowly and at a lower per-GPU tier than NAIRR, ACCESS, or
commercial cloud.

= Throughput Model and H200-hour Equivalence

Because the GPU mix is heterogeneous and concurrency depends on
moment-to-moment supply, useful equivalence figures are _scenario-based_
rather than fixed allocations. A reference upper bound is straightforward.
One thousand concurrent A100 job-slots running for one wallclock hour is
$1000 times 312 / 989 approx 315$ H200-hours per wallclock hour. That
ceiling is rare. A more realistic steady-state for a single user is
20--100 concurrent GPU slots drawn mostly from V100 and RTX-class cards,
with 10--30\% of jobs preempted and re-run.

The table below sketches three weekly scenarios, assuming a representative
GPU mix of 40\% V100 (125 TFLOPS), 30\% RTX (110 TFLOPS), 20\% A100 (312
TFLOPS), and 10\% T4 (65 TFLOPS), giving a blended ~144 TFLOPS per slot,
and netting out a 20\% preemption tax.

#table(
  columns: (auto, auto, auto, auto, auto),
  align: (left, right, right, right, right),
  table.header[Scenario][GPU job-hours/wk][Blended TFLOPS][Preempt. tax][H200-hr eq./wk],
  [Small individual user], [1,000], [144], [20\%], [~117],
  [Medium sustained burn], [10,000], [144], [20\%], [~1,165],
  [Large coordinated campaign], [100,000], [144], [20\%], [~11,650],
)

CPU equivalence is not stated in H200-hours because CPU and tensor-GPU
throughput are not interchangeable for ML workloads. For preprocessing,
feature extraction, and Monte Carlo, the CPU pool can deliver the
equivalent of several large clusters worth of cycles per week at no cost.

= Approval Timeline

Onboarding takes approximately one week. The user fills a short
registration form with an Access Point, declares a project name and brief
description, identifies a faculty or staff sponsor, and receives a login
on the AP. There is no per-project review, no allocation committee, and no
ranking against other applicants. A first job typically runs the same day
the account is activated.

= Eligibility

Access is open to United States-based open-science researchers, including
graduate students with advisor sign-off. Non-US collaborators may
participate as members of a US-based principal investigator's project.
Classified, ITAR-controlled, export-controlled, and HIPAA-restricted work
is forbidden on OSPool, since the opportunistic execution sites cannot
guarantee the data-handling controls those regimes require.

= Things to Know

Several practical points dominate day-to-day use. Workloads must be
refactorable into independent short jobs. There is no MPI across nodes,
and jobs that exceed wallclock or memory caps are killed. Checkpointing is
the user's responsibility, and any job longer than a few hours should
write periodic state to OSDF so that a preemption loss costs minutes
rather than hours. Singularity / Apptainer containers are strongly
recommended, both because they make the job portable across heterogeneous
sites and because they sidestep host library mismatches that would
otherwise produce cryptic CUDA failures.

OSDF handles input and output staging but is not persistent storage.
Datasets must be pushed to OSDF (or an HTTP/S3 origin federated into OSDF)
before the campaign and pulled back to durable storage afterward.
Preemption rates of 10--30\% are normal and should be modeled into job
sizing. The sweet spot is hyperparameter sweeps, Monte Carlo, ensemble
inference, feature extraction over large datasets, and genome-analysis-style
pipelines. The pool is not appropriate for end-to-end training of a 7B-class
language model, which would require multi-node NVLink-class fabric that the
opportunistic pool does not expose.

= Strategic Fit

OSPool is excellent _complementary_ compute for any project that can be
embarrassingly parallelized. It is poorly suited to tightly coupled
multi-GPU foundation-model training. The recommended pattern is to train a
model on NAIRR or ACCESS, then run sweeps, ablations, ensemble inference,
and large-scale feature extraction on OSPool. CPU-side preprocessing of
multi-terabyte datasets is also a natural fit, since the CPU pool is
effectively unmetered for a well-formed submitter.

= Summary

#table(
  columns: (1.4fr, auto, auto, auto),
  align: (left, right, left, left),
  table.header[Workload type][H200-hr eq. /wk][Effort to port][Fit],
  [Hyperparameter sweep (small models)], [~1,000--10,000], [Low], [Excellent],
  [Ensemble / Monte Carlo inference], [~1,000--10,000], [Low], [Excellent],
  [Feature extraction over large datasets], [CPU-bound, very high], [Low--medium], [Excellent],
  [Single-GPU fine-tuning (≤7B)], [~100--1,000], [Medium (checkpoint)], [Good],
  [Multi-GPU single-node training], [~50--500], [Medium], [Marginal],
  [Multi-node MPI / 7B+ pretraining], [N/A], [Not supported], [Unsuitable],
)

#h200-note

= Sources

#set text(size: 9pt)
- OSG Consortium home and OSPool: #link("https://osg-htc.org/")[osg-htc.org] · #link("https://ospool.osg-htc.org/")[ospool.osg-htc.org]
- OSG Connect Access Point and onboarding: #link("https://portal.osg-htc.org/")[portal.osg-htc.org] · #link("https://portal.osg-htc.org/documentation/")[OSG documentation]
- OSPool dashboard and resource accounting: #link("https://gracc.opensciencegrid.org/")[GRACC accounting] · #link("https://display.ospool.osg-htc.org/")[OSPool live dashboard]
- OSDF data federation: #link("https://osg-htc.org/services/osdf.html")[OSDF service page] · #link("https://osg-htc.org/docs/data/")[OSG data documentation]
- HTCondor user manual (job submission, preemption, GPU requests): #link("https://htcondor.readthedocs.io/")[htcondor.readthedocs.io]
- CHTC and contributing-site documentation: #link("https://chtc.cs.wisc.edu/")[CHTC] · #link("https://hcc.unl.edu/")[Nebraska HCC] · #link("https://www.sdsc.edu/")[UCSD SDSC]
- GPU specifications cross-checked against NVIDIA A100, A40, V100, P100, T4, RTX 3090, and RTX 2080 Ti datasheets.
