# Fresh review of the 12-page manuscript

All four independent reviewers evaluated the manuscript at revision `3ceec5f` before the experiments below. These are simulated conference reviews. The question was whether the results offered enough new engineering knowledge and practical benefit for an IDETC vibrations paper.

| Reviewer | Decision on the 12-page draft | Decisive observation |
|---|---|---|
| Claude Opus, xhigh | Reject | Established component methods, selected maximum gains, and comparisons with an unnecessarily stale baseline obscured the contribution. |
| Antigravity Hydrogen 4, xhigh, local session | Reject | The hull and propagation assumptions lacked enough experimental support for target-specific design gains. |
| Sol xhigh, vibrations | Accept | Shared-wave interventions separated mechanisms, and nonlinear damping changed the engineering conclusion. The abstract needed the exact-measurement assumption and clock conditions. |
| Sol xhigh, methods | Reject | The missing stand-alone leveling arm prevented a hardware versus software decision. Field precision and the applicable page limit also mattered. |

## What the revision established

The simulation now crosses both pointing policies with both registration times. Separate hardware and software gains substantially overlapped. Comparing the two stand-alone interventions changed the preference in five of 111 conditions. A separate product-of-marginals estimate agreed with the true joint rate in 100 cells and overstated the registration gain by as much as 9.11 percentage points. The paper reports the denominator and the size of the error in both directions.

The noisy timing comparison replays every original grid cell at 50, 100, 200, and 625 ms pose ages against exact timing. Stand-alone hardware and phase-matched results appear beside realistic-baseline sensitivities. Additional experiments test directional wave spreading, alternative crest propagation, an orbiting target and held fixes, and dwell-dependent clock selection. None established a general advantage over a fixed 48 rpm clock.

Two inland-water recordings contribute 96,000 original spokes, synchronized navigation, and 8,712 matched persistent returns. Absolute errors are available only for the synthetic targets replayed along measured vessel trajectories. The actual returns support a repeatability comparison. Independent shore-based IPIX data illustrate how the number of measured windows close to a threshold bounds the largest possible gain from a given increase in return margin.

The revised abstract emphasizes overlap, grid-wide timing results, and field repeatability. Related work now places the paired comparison beside published spinning-radar motion correction, platform-sway registration, and vertical-motion studies. The figure shows the pitch sign and forward antenna lever. The manuscript uses the ASME conference class and the more restrictive [10-page technical paper guidance](https://www.asme.org/publications-submissions/proceedings/author-guidelines/paper-and-presentation-types).

## Evidence still needed

A transferable claim about absolute buoy accuracy or real stabilization gain requires independent buoy trajectories and synchronized, calibrated echo and clutter margins during controlled pointing changes. Neither public dataset supplies that combination. The field clips cannot test X-band sea-crest diffraction or the gain of a stabilized antenna. The simulations identify when an intervention can matter and which measurement would distinguish the mechanisms aboard a particular vessel.

## Second assessment

Both Sol reviewers independently read the integrated revision and recommended acceptance as a diagnostic design study. The methods reviewer changed from reject to accept because the four-arm comparison demonstrates a consequence for retrofit choice and the field claims now match the observations. The vibrations reviewer retained accept and verified the headline numbers against the CSVs. The external reviewers' decisions above apply to the 12-page draft.
