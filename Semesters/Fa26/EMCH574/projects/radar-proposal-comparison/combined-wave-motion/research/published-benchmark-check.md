# Published benchmark check

## Recommended paper-grounded additions

The strongest immediately reproducible benchmark is pulse-time georeferencing from Lund et al. (2018), *Arctic Sea Ice Drift Measured by Shipboard Marine Radar*, Journal of Geophysical Research: Oceans, DOI 10.1029/2018JC013769. The method maps each pulse using the antenna look direction and transceiver position at that pulse time, interpolating 5 Hz ship navigation to the radar's 3 kHz pulse repetition frequency. The paper explicitly neglects heave, pitch, and roll and explains that the resulting mapping error is generally below its 7.5 m range resolution. These details appear on page 5 of the published PDF. The reproducible comparison is therefore a horizontal pulse-time transform versus a pose-held-fixed transform, with the same interpolation and Cartesian grid. It supplies a published baseline and a direct test of when vertical motion exceeds the stated resolution argument. It does not supply a small-target detection model.

Use the ray transform in the same form as the proposal,

\[
\mathbf{x}_i=\mathbf{p}(t_i)+\mathbf{R}(t_i)\left[\rho_i\cos\epsilon\begin{pmatrix}\cos\alpha_i\\\sin\alpha_i\\0\end{pmatrix}+\rho_i\sin\epsilon\begin{pmatrix}0\\0\\1\end{pmatrix}\right],
\]

with \(\epsilon=0\) for the horizontal published baseline and a known-plane inverse only in the controlled synthetic test. Do not claim that Lund et al. validated pitch or roll correction. Their reported inputs are a 5 Hz navigation stream, 3 kHz pulse timing, a 7.5 m grid, and a 4 km maximum range in the cited experiment. The 0.25 s scan interval in the current illustration is a prescribed course parameter, not a paper value.

Burnett, Schoellig, and Barfoot (2021), *Do We Need to Compensate for Motion Distortion and Doppler Effects in Spinning Radar Navigation?*, IEEE Robotics and Automation Letters 6(2), 771–778, DOI 10.1109/LRA.2021.3052439, supplies a second benchmark for scan-time distortion. Its paper-level model treats a spinning scan as time-varying sensor motion and compares motion-compensated registration with a single-time scan assumption. The reproducible mathematical core is the same acquisition-time rigid transform above, evaluated at each azimuth, followed by scan-to-scan registration. The paper reports a 9.4% reduction in translational drift from motion compensation in odometry and, in a separate high-speed localization experiment, reductions of 41.7% for motion compensation, 67.7% for Doppler compensation, and 81.2% combined. Those percentages are paper-specific outcomes and must not be transferred to the maritime target problem. The paper's automotive operating conditions and Doppler treatment are a sensitivity benchmark, not a sea-clutter validation.

Wijaya and van Groesen (2016), *Determination of the Significant Wave Height from Shadowing in Synthetic Radar Images*, Ocean Engineering 114, 204–215, DOI 10.1016/j.oceaneng.2016.01.011, provides the defensible wave-shadowing benchmark. Its central observable is a visibility function that varies with normalized radar height over significant wave height and normalized horizontal distance. The authors construct visibility databases with synthetic seas and Monte Carlo realizations, then compare measured shadowing curves with the database. The paper abstract and the published chapter's pages 204–215 establish these dimensionless inputs and the visibility objective. Reproduce that visibility calculation as a wave-only propagation benchmark before coupling it to a moving target. Do not reinterpret its sea-surface visibility or reported significant-wave-height retrieval as a small-target detection probability.

## What a real radar record can test

An IPIX-like coherent record can support target-bin return distributions, clutter distributions, temporal persistence, outage windows, and threshold calibration when target-bin metadata and acquisition timing are available. It can test whether a proposed detector behaves consistently across range and clutter conditions. It cannot provide continuous wave phase, target heave, or independent target position truth from radar intensity alone. Consecutive misses at a labeled target bin are dropout proxies. They are suitable for an exploratory association between available environmental summaries and outages, not for a claim that a particular wave phase caused a miss.

The measured plot should therefore show target-bin amplitude or power, neighboring clutter statistics, detector decisions, and outage duration against acquisition time. A separate panel may show the available sea-state summary, but it must not be labeled instantaneous wave elevation. Any phase-conditioned result requires synchronized local wave measurements, vessel pose, target position, and pulse timing. Public records can validate processing behavior and the forecast protocol; they cannot validate the full coupled mechanical and electromagnetic mechanism.

## Benchmark contract

Keep the current prescribed illustration as a controlled stress case. Add the Lund pulse-time transform and the Burnett scan-time comparison as geometry and acquisition baselines. Add the Wijaya visibility curve as a shadowing-only propagation check. Then evaluate all forecast feature ablations on common returns with one frozen operational correction method and identical target truth. Report illumination availability, received target power, detector performance, and conditional position error as separate quantities. The published baselines constrain what the implementation can claim, while the synchronized acquisition contract determines what a later physical validation can establish.

## Primary sources

Lund et al. PDF. https://faculty.washington.edu/jmt3rd/Publications/Lund_2018JC013769.pdf

Burnett et al. PDF. https://www.dynsyslab.org/wp-content/papercite-data/pdf/burnett-ral21.pdf

Wijaya and van Groesen record. https://doi.org/10.1016/j.oceaneng.2016.01.011
