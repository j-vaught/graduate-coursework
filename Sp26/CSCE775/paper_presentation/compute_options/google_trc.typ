#import "_style.typ": *
#show: report-setup.with(title: "Google TRC", program: "Google TPU Research Cloud")
#title-block(program: "Google TRC & Research Credits", tagline: "Free TPU access for research — easiest frontier-AI compute you can get")

= Program overview

The Google TPU Research Cloud (TRC) is a direct-from-Google program that grants academic and independent researchers free access to large quantities of preemptible Tensor Processing Unit (TPU) capacity in exchange for an open publication acknowledging the program. TRC is administered by a small team at Google Research and is not tied to Google Cloud's billed product line, although the underlying TPUs run in the same Google Cloud regions. The program has been open to external researchers since 2017 and continues to operate through 2024-2026 with rotating availability across TPU generations.

A second and frequently confused program is the Google Cloud Research Credits initiative, sometimes branded under the umbrella of the Google Cloud Research Innovators community. Research Credits are dollar-denominated grants applicable against any Google Cloud product, including general-purpose virtual machines, GPU instances (A100, H100, and selectively H200), storage, and BigQuery. Typical award sizes run from \$1,000 to \$5,000 with occasional larger awards near \$20,000 for high-visibility projects. Research Credits and TRC can be held simultaneously, and the two are commonly paired so that a TRC participant can use a small Research Credit balance to pay for the Google Cloud Storage (GCS) buckets that hold their datasets and checkpoints.

The clearest mental model is that TRC supplies _chips_ and Research Credits supply _dollars_. They have separate applications, separate review pipelines, and separate restrictions. A graduate student should usually apply to both.

= Hardware specs

The TPU families below have been offered through TRC at various points across 2024-2026. Availability rotates and the application form asks the researcher to rank-order preferences. Pod-slice sizes shown are the smallest unit grant typically issued; larger contiguous slices are available on request once a project has demonstrated activity.

== TPU generations available through TRC

#table(
  columns: 7,
  align: (left, center, center, center, center, center, left),
  table.header[TPU generation][HBM/chip][BF16 TFLOPS/chip][Mem BW][Smallest TRC slice][Full pod topology][Interconnect (ICI)],
  [TPU v2], [8 GB], [\~46], [0.6 TB/s], [v2-8 (8 chips)], [v2-512 (256 chips)], [2D torus, 500 Gbps],
  [TPU v3], [16 GB], [\~123], [0.9 TB/s], [v3-8 (8 chips)], [v3-2048 (1024 chips)], [2D torus, 656 Gbps],
  [TPU v4], [32 GB], [\~275], [1.2 TB/s], [v4-8 (4 chips)], [v4-4096 (2048 chips)], [3D torus, 4.8 Tbps],
  [TPU v5e], [16 GB], [\~197], [0.8 TB/s], [v5litepod-8], [v5e-256 (256 chips)], [2D torus, 1.6 Tbps, inference-tilted],
  [TPU v5p], [95 GB], [\~459], [2.8 TB/s], [v5p-8 (4 chips)], [v5p-8960 (4480 chips)], [3D torus, 4.8 Tbps],
  [TPU v6e (Trillium)], [32 GB], [\~926], [1.6 TB/s], [v6e-8], [v6e-256 (256 chips)], [2D torus, 3.2 Tbps],
)

TPU v2 and v3 are legacy generations that remain in heavy TRC rotation because Google continues to operate the hardware and the chips have low contention; they are an excellent fit for research that does not need frontier-scale memory or throughput. TPU v4 has been the workhorse generation for TRC since 2022 and is still the most commonly granted slice in 2026. TPU v5e is inference-tilted, with reduced HBM and lower interconnect bandwidth, and is offered to projects whose main need is throughput on smaller models. TPU v5p and v6e (Trillium) are the current frontier generations; TRC eligibility for both has been intermittent through 2025 and 2026, with v5p slices granted to a limited subset of approved projects and Trillium offered primarily to renewal applicants with prior TRC publications.

A subtle naming note. A v4-8 _slice_ contains four physical TPU v4 chips paired with eight TensorCores (two per chip), which is why some Google documentation describes v4-8 as an eight-core slice while the chip count is four. The same convention applies to v5p-8. The throughput table above is reported per chip to keep the H200 conversion below internally consistent.

== GPU options via Research Credits

#table(
  columns: 6,
  align: (left, center, center, center, center, left),
  table.header[Instance][GPUs][VRAM/GPU][BF16 TFLOPS][Mem BW][Notes],
  [a2-ultragpu-8g], [8x A100], [80 GB], [312], [2.0 TB/s], [SXM, NVLink, broadly available],
  [a3-megagpu-8g], [8x H100], [80 GB], [989], [3.35 TB/s], [SXM, 3.2 Tbps fabric],
  [a3-ultragpu-8g], [8x H200], [141 GB], [989], [4.8 TB/s], [SXM, limited regions],
  [g2-standard-96], [8x L4], [24 GB], [121], [0.3 TB/s], [PCIe, inference workloads],
)

Research Credits do not unlock special quota; H100 and H200 quota requests still go through the standard Google Cloud quota review and can take one to four weeks even after credits are in hand.

= TPU vs H200 equivalence

The H200 SXM reference point used throughout this report is 989 BF16 TFLOPS dense per GPU. The conversion is a straight TFLOP-hour ratio, which is appropriate for compute-bound workloads but understates TPU advantage on memory-bound or interconnect-bound training because the TPU pod fabric (ICI) is substantially better than commodity GPU interconnect at the same scale. The conversion also _does not_ correct for preemption, which on TRC routinely costs 20-40% of effective wall-clock throughput because preemptible TPUs are reclaimed by Google's billing tier on demand and the user must restart from the most recent checkpoint.

Per-chip BF16 dense throughput used below. TPU v3 at 123 TFLOPS, TPU v4 at 275 TFLOPS, TPU v5e at 197 TFLOPS, TPU v5p at 459 TFLOPS, TPU v6e at 926 TFLOPS. H200 at 989 TFLOPS.

The arithmetic for a 30-day TPU v4-8 grant runs as follows. A v4-8 contains four chips, each at 275 BF16 TFLOPS dense, for 1100 TFLOPS aggregate. Across 30 days that is $30 times 24 = 720$ chip-hours per chip and $4 times 720 = 2880$ chip-hours total. Multiplying by 275 TFLOPS and dividing by 989 TFLOPS per H200 yields approximately 801 H200-hours of dense compute. The often-quoted figure of ~1602 H200-hours instead counts the eight TensorCores rather than four chips, which is the convention several earlier TRC writeups used. Both conventions appear in the literature; the table below reports the chip-count convention and notes the doubled value where relevant.

#table(
  columns: 5,
  align: (left, center, center, center, center),
  table.header[TRC slice (30 days)][Chips][BF16 TFLOPS aggregate][H200-hr equiv (chip basis)][Effective after preempt (30%)],
  [v3-8], [8], [\~984], [\~717], [\~502],
  [v4-8], [4], [\~1{,}100], [\~801], [\~561],
  [v4-32], [16], [\~4{,}400], [\~3{,}204], [\~2{,}243],
  [v4-128], [64], [\~17{,}600], [\~12{,}816], [\~8{,}971],
  [v5p-8], [4], [\~1{,}836], [\~1{,}337], [\~936],
  [v5p-128], [64], [\~29{,}376], [\~21{,}386], [\~14{,}970],
  [v6e-256 (Trillium)], [256], [\~237{,}056], [\~172{,}621], [\~120{,}835],
)

The Trillium row is included for completeness but is rarely granted to first-time TRC applicants. The realistic expectation for an unaffiliated graduate student in 2026 is the v4-8 row, which already exceeds 500 effective H200-hours per month after preemption losses, comparable to a one-month allocation on a small NAIRR or ACCESS GPU pilot.

= Typical allocation size

A first-time TRC grant in 2024-2026 is typically described as 30 days of a small slice, most commonly a TPU v4-8 or a rotating mix of v2-8, v3-8, and v4-8. Some grants are issued as chip-day pools (for example, "5 v4 chips for 30 days") and others as rolling pod-hour budgets. Heavier projects with prior TRC publications have been granted v4-32, v4-128, or v5p-8 slices, and a small number of long-running collaborations have received Trillium access. Grants are renewable and the renewal form is shorter than the initial application; in practice a productive TRC user can sustain access for a year or more on rolling 30-day extensions.

Google Research Credits land in the \$1,000 to \$5,000 range for the standard track. The Research Innovators community track sometimes bundles credits with mentorship and event invitations. High-profile projects, particularly those with media-visible results or strong faculty endorsement, have received credit grants near \$20,000. Credits expire in 12 months and cannot be transferred between projects.

= Approval timeline

TRC review is fast. The application is a single web form with a project description of roughly one paragraph, the researcher's affiliation, and a preferred TPU generation. Decisions land within a few days to about two weeks. Reviewers do not require a published preprint or letters of support; the bar is whether the project is plausible research that can produce an open output.

Google Research Credits run on a slower cycle, generally four to six weeks from submission to credit issuance. The application requires a slightly more developed project description, an institutional affiliation, and a brief budget. There is no Google analog to Microsoft's AFMR program by name, but the Research Innovators initiative serves a similar community-and-credits role and is the right place to look for a structured cohort experience rather than a one-off credit grant.

= Eligibility

TRC is open to researchers globally. Applicants must commit to publishing results openly and to including a TRC acknowledgment line in any resulting paper, blog post, or technical report. Individuals at accredited academic institutions are the primary audience, but independent researchers and industry researchers can also apply, with a stated preference for academic and open-research settings. There is no requirement that the applicant be a faculty member; graduate students apply on their own behalf and are reviewed on the merits of the project description.

Google Research Credits are more conventionally institutional. The applicant must hold an academic affiliation, and the credits are issued against an institutional billing account rather than a personal one. Industry and non-profit researchers can apply through separate tracks but face additional review.

= Things to know

Preemption is the central operational fact of TRC. The TPUs granted are preemptible, which means Google's scheduler can reclaim them at any time when paid customers need the capacity. Code that does not checkpoint frequently will lose work. Best practice is to checkpoint at least every 15-30 minutes and to design training scripts so that resuming from the latest checkpoint is automatic on restart.

JAX and TensorFlow are first-class on TPU. PyTorch on TPU works through the PyTorch/XLA bridge and has improved substantially since 2023, but it still has rough edges around dynamic shapes, custom CUDA kernels (which obviously do not run), and certain operator coverage. A PyTorch-native researcher should budget one to two weeks of learning curve to get a non-trivial training loop running on a v4-8 slice.

There is no persistent local disk on a TPU VM in the way a researcher would expect from a GPU instance. Datasets and checkpoints live in Google Cloud Storage buckets, which incur their own charges. A small Google Research Credit grant is a clean way to cover the GCS bill for a TRC project. Egress to non-Google destinations is also billed and is the most common surprise on the first month's invoice.

Multi-host pod-slice programming is nontrivial. Once a slice exceeds a single host (32 chips for v4, sometimes earlier on other generations), the training script must coordinate across multiple TPU VMs over the ICI fabric, and the JAX or PyTorch/XLA distributed launcher requires care. Single-host slices (v4-8, v5p-8, v6e-8) are dramatically easier to use and are the right starting point.

TRC grants are renewable. The renewal application is a short form that summarizes what was done with the previous grant and what is planned next. Acknowledgment of TRC in a published paper is the strongest possible renewal credential.

= Strategic fit

TRC is the single easiest path to free frontier-scale compute that exists for an unaffiliated graduate student. There is no PI requirement, no institutional sub-agreement, no proposal cycle, and no XSEDE-style allocation review. The application is a paragraph and the answer arrives in days. For a student whose project ports cleanly to JAX, or who is willing to invest a learning week into PyTorch/XLA, TRC is essentially free training capacity at a scale that would cost thousands of dollars per month on commercial cloud.

The natural pairing is TRC for the TPU-friendly training runs, NAIRR or ACCESS for the GPU-side ablations, sweeps, and inference benchmarks that need CUDA-only kernels, and a small Google Research Credit balance to cover the GCS bill that TRC does not. A student running this stack can comfortably sustain a research program comparable in compute footprint to a well-funded industry lab, at zero personal cost, for the duration of a PhD.

The case against TRC is narrow. Projects that depend on _CUDA-only_ libraries (FlashAttention custom kernels, certain Triton-only paths, NVIDIA-specific profiling tooling), projects that require persistent local NVMe scratch, and projects whose training loops use heavy dynamic control flow that XLA cannot trace cleanly will spend more time on the porting effort than the free compute is worth. For everything else, TRC is the recommended first stop.

= Summary table

#table(
  columns: 5,
  align: (left, center, center, center, center),
  table.header[Resource][Typical size][H200-hr equivalent][Approval time][Effort to adopt],
  [TRC v4-8, 30 days], [4 chips], [\~800 (\~560 effective)], [days to 2 weeks], [Medium (XLA)],
  [TRC v4-32, 30 days], [16 chips], [\~3{,}200 (\~2{,}240 effective)], [1-3 weeks], [Medium-High (multi-host)],
  [TRC v5p-8, 30 days], [4 chips], [\~1{,}340 (\~940 effective)], [2-4 weeks], [Medium],
  [TRC v6e Trillium], [rare for first-time], [tens of thousands], [4-8 weeks], [High],
  [Research Credits \$5k], [\$5{,}000], [\~480 H200-hr (on-dem)], [4-6 weeks], [Low],
  [Research Credits \$20k], [\$20{,}000 (rare)], [\~1{,}900 H200-hr (on-dem)], [6-8 weeks], [Low],
)

#h200-note

= Sources

- Google TPU Research Cloud program site, application form, and acknowledgment policy, https://sites.research.google/trc/about/
- Google Cloud TPU v4 system architecture and per-chip specs, https://cloud.google.com/tpu/docs/system-architecture-tpu-vm
- Google Cloud TPU v5e and v5p product pages, https://cloud.google.com/tpu/docs/v5e and https://cloud.google.com/tpu/docs/v5p
- Google Cloud Trillium (TPU v6e) announcement and specs, https://cloud.google.com/blog/products/compute/introducing-trillium-6th-gen-tpus
- Google Cloud Research Credits and Research Innovators program, https://cloud.google.com/edu/researchers and https://rs.withgoogle.com/innovators
- PyTorch/XLA documentation for TPU users, https://pytorch.org/xla/
- NVIDIA H200 SXM datasheet (FP16/BF16 dense 989 TFLOPS, 141 GB HBM3e, 4.8 TB/s), https://www.nvidia.com/en-us/data-center/h200/

#v(1em)
#text(size: 9pt, fill: black70, style: "italic")[TPU specifications and TRC eligibility verified April 2026; TRC slice availability rotates and the most current generation eligibility should be confirmed on the application form at submission time.]
