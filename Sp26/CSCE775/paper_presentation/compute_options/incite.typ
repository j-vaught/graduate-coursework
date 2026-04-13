#import "_style.typ": *
#show: report-setup.with(title: "DOE INCITE", program: "DOE INCITE")
#title-block(program: "DOE INCITE", tagline: "Leadership-class allocations on Frontier, Aurora, and Polaris — competitive and large")

= Program Overview

The Innovative and Novel Computational Impact on Theory and Experiment (INCITE) program is the U.S. Department of Energy's flagship leadership-computing allocation program. It is jointly managed by the Argonne Leadership Computing Facility (ALCF) and the Oak Ridge Leadership Computing Facility (OLCF), and it awards roughly 60% of the available compute time at each facility every year. Allocations run for one calendar year, with renewals possible for up to three years upon strong progress reports.

INCITE selects projects on the basis of \textit{high-impact computational science}. Historically the portfolio has been dominated by physics, chemistry, materials science, climate, and combustion. Since 2023, however, AI/ML has become an explicitly accepted class under the ML4Science track, with growing emphasis on foundation-model training, scientific surrogates, and large-scale neural simulation. INCITE now routinely funds multi-million GPU-hour campaigns for transformer pre-training and protein/materials models.

= Hardware Specifications

The three current INCITE-eligible systems span three different accelerator vendors, which is both the program's strength and its principal porting burden.

#table(
  columns: (auto, auto, auto, auto, auto, auto, auto),
  table.header[System][Accelerator][VRAM/accel][FP16/BF16 TFLOPS][Mem BW (TB/s)][Interconnect][CPUs/node],
  [Frontier (OLCF)], [AMD MI250X (8 GCDs/node)], [128 GB HBM2e], [~383 (per GCD)], [3.2], [HPE Slingshot-11], [1× AMD EPYC 64c],
  [Aurora (ALCF)], [Intel Data Center GPU Max 1550 (PVC, 6/node)], [128 GB HBM2e], [~839 (BF16 dense)], [~3.3], [HPE Slingshot-11], [2× Intel Xeon Max 52c],
  [Polaris (ALCF)], [NVIDIA A100 40GB (4/node)], [40 GB HBM2], [312], [1.56], [HPE Slingshot-11], [1× AMD EPYC 32c],
)

Frontier's MI250X is logically programmed as eight GPUs per node because each package exposes two Graphics Compute Dies (GCDs) over Infinity Fabric. Aurora's Ponte Vecchio (PVC) is the highest dense BF16 throughput per accelerator in the fleet but ships with the least mature ML stack. Polaris is the smallest of the three and the most familiar from a software standpoint because it is pure CUDA on A100.

= Allocation Sizes and H200-Hour Equivalents

Typical INCITE awards land between 100k and 1M+ node-hours per year, with the very largest projects exceeding 2M node-hours on Frontier. The table below converts representative awards into H200-SXM equivalent hours using dense FP16/BF16 tensor throughput.

#table(
  columns: (auto, auto, auto, auto, auto),
  table.header[System][Award (node-hr)][Accels/node][FP16 TFLOPS/accel][H200-hr equivalent],
  [Frontier], [500,000], [8 GCDs], [383], [~1.55 M],
  [Aurora], [250,000], [6 PVC], [839], [~1.27 M],
  [Polaris], [100,000], [4 A100], [312], [~126 k],
)

Worked math. Frontier: $500{,}000 times 8 times 383 / 989 approx 1{,}549{,}000$ H200-hours. Aurora: $250{,}000 times 6 times 839 / 989 approx 1{,}272{,}000$ H200-hours. Polaris: $100{,}000 times 4 times 312 / 989 approx 126{,}000$ H200-hours. Even a modest INCITE award on Frontier dwarfs a typical NAIRR or ACCESS allocation by one to two orders of magnitude in raw FP16 throughput.

= Approval Timeline

The annual Call for Proposals opens in mid-April and closes in mid-to-late June. Submissions are reviewed through the summer by domain panels (physics, chemistry, biology, ML, etc.) and in parallel by an ALCF/OLCF operational feasibility panel that scores computational readiness. Awards are announced in early-to-mid November, and allocations begin January 1 of the following calendar year.

A complete proposal is roughly 15 pages of science narrative plus a separate computational readiness assessment, a data management plan, and PI/team biosketches. Readiness scoring is rigorous. Projects that have not previously demonstrated scaling on the target system are routinely down-rated regardless of scientific merit.

= Eligibility

INCITE is open to researchers worldwide. There is no requirement that the PI hold DOE funding, and academic, industry, and national-laboratory PIs are all eligible. PIs are typically senior — full or associate professors, staff scientists, or principal investigators of established research groups. Graduate students are not realistic PIs but routinely appear as co-investigators or named team members, and are typically the people doing the day-to-day work on the allocation. Foreign PIs are permitted, but the proposing institution must handle U.S. export-control compliance for the target facility.

= Things to Know

Before an INCITE proposal is competitive, the team almost always needs a Director's Discretionary (DD) pilot allocation on the target machine. DD allocations are small (tens of thousands of node-hours), short, and used to demonstrate that the code actually scales on Frontier, Aurora, or Polaris. The readiness panel reads DD performance reports closely.

Cross-platform porting is the dominant non-science cost. Frontier requires AMD ROCm and HIP. Aurora requires Intel oneAPI, SYCL, and the Level Zero runtime. PyTorch and JAX support on MI250X and PVC has improved substantially through 2024-2026 but remains thinner and less well-trodden than CUDA on A100/H100/H200. Expect non-trivial debugging of mixed-precision kernels, distributed collectives, and FlashAttention variants on the non-NVIDIA systems.

Once an award is in place, queue priority is high and turnarounds are excellent. Data egress, however, is manual and goes through Globus. Classified, ITAR, or otherwise restricted work is not permitted on INCITE resources.

= Strategic Fit for AI/ML Graduate Work

It is essentially impossible for a graduate student to lead an INCITE proposal. The realistic path is to join an existing INCITE project led by an advisor or collaborator. When that fits, the H200-equivalent scale is enormous — comfortably in the millions of hours, which is one to two orders of magnitude larger than what NAIRR or ACCESS typically deliver to a single project.

For PyTorch and JAX workloads, target Polaris first. Pure CUDA on A100 means existing training pipelines, FlashAttention, DeepSpeed, and FSDP work with minimal porting. Frontier yields the largest absolute throughput but only if the team is willing to invest in ROCm. Aurora is attractive on paper for BF16 throughput but should be approached only with strong oneAPI/SYCL support already in place.

= Summary

#table(
  columns: (auto, auto, auto, auto),
  table.header[System][Typical award (node-hr)][H200-hr equivalent][Readiness effort],
  [Frontier], [500k–2M], [~1.55M–6.2M], [High (ROCm/HIP port)],
  [Aurora], [250k–1M], [~1.27M–5.1M], [Very high (oneAPI/SYCL)],
  [Polaris], [100k–500k], [~126k–630k], [Low (pure CUDA)],
)

#h200-note

= Sources

Verified against the INCITE program documentation at \texttt{doeleadershipcomputing.org}, ALCF system documentation at \texttt{alcf.anl.gov} (Aurora and Polaris machine pages), and OLCF system documentation at \texttt{olcf.ornl.gov} (Frontier user guide), 2024–2026. Reference H200 SXM specifications drawn from NVIDIA H200 datasheet (989 TFLOPS dense FP16/BF16, 141 GB HBM3e, 4.8 TB/s).
