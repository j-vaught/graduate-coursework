# Review and verification of the submission draft

The four reviewers first read the 12-page paper at revision `3ceec5f`. Opus, Hydrogen, and the methods reviewer voted reject. The vibrations reviewer voted accept. After the first revision, both Sol reviewers voted accept on the 10-page paper at `57ea52d`. The two external reviewers then independently read that same revision. Opus voted accept with edits, and Hydrogen voted reject. Both requested tests of surge phase, the field interpretation, and the scope of the headline result.

## Responses to substantive objections

| Objection | Evidence in the submission draft |
|---|---|
| The selected wave exaggerates the usual gain. | The full 111-cell comparison crosses pointing and pose age under common measurement errors. The largest absolute interaction is 0.47 points at 50 ms. The selected cell gives 4.54 points at 625 ms with those errors. The figure reports the selected cell against the cross-cell distribution. |
| The assumed motion phase and yaw could determine the answer. | The surge sign is reversed and removed in the same three waves. A clock based on actual target-bearing crossings reproduces the original forward interaction at zero yaw. Retaining a one-degree yaw oscillation reverses it. |
| The vibration model needs a measured-phase test. | Regular head-wave tank records constrain the amplitude and phase of heave and pitch. Replaying these responses in radar geometry gives complete retrofit overlap at one tolerance and no gain at a looser tolerance. The tank experiment measured motion only. |
| One target record and two short radar clips cannot support a design claim. | All 14 cataloged Dartmouth weak-target recordings bound threshold recovery over held-out windows. Across eight CANOE sessions, two-sided uncertainty intervals include zero, and the lag and range analyses expose where repeatability changes. These are different sensors and experiments. |
| Acquisition and mapping may be effectively independent. | The product approximation is tested against paired counts on each grid cell. With noise and a 625 ms pose age the absolute gain discrepancy reaches 2.84 points for the body-pointed case. At 50 ms it reaches 0.38 points. |
| The detector, propagation law, and dwell assumptions could reverse design choices. | Comparisons use direct rays, dominant- and multiple-crest diffraction, a bounded two-ray field model, and threshold perturbations. The scan selection test includes three dwell laws at both 5 and 10 dB. Its speed ranking changes with echo margin. |
| The replication package is difficult to locate. | The source, derived tables, original-record identifiers, figure sources, and build instructions are versioned together. A clean export reproduced all figure PDFs and rebuilt the 10-page article on COMECH. |

## Decisions on the frozen 10-page paper

| Reviewer | Decision on `434a8da` | Basis |
|---|---|---|
| Claude Opus xhigh | Accept, conditional on corrections | The four-arm evidence supports the contribution. The crest recursion produced degenerate all-missed cases, and the CANOE repeatability metric required a same-metric control. |
| Antigravity Hydrogen 4 xhigh, local session | Accept | The physical and empirical comparisons support a bounded design study. Suggested copy and packaging corrections. |
| Sol xhigh, methods | Accept | The four-arm, noisy latency, yaw, tank, and field estimates agreed with the data. |
| Sol xhigh, vibrations | Accept | The coupled mechanism, measured-response replay, and scope of the engineering claims were sufficient. |

The frozen review copy is `434a8da`, archived in Git under the tag [emch574-radar-replication-v1](https://github.com/j-vaught/graduate-coursework/tree/emch574-radar-replication-v1/Semesters/Fa26/EMCH574/projects/radar-proposal-comparison/combined-wave-motion). Absolute accuracy on a buoy and acquisition gain from a physical gimbal still require independently tracked buoy positions and calibrated power measurements aboard the same vessel.

## Corrections following the conditional decision

Unrestricted crest recursion generated no echoes in two small-wave conditions even though the primary crest had zero modeled loss. The paper now exposes those outcomes, prunes zero-loss branches, and compares unrestricted and three-edge constructions. Both corrected variants restored 6,144 echoes in each case. The capped three-edge calculation gave registration and subsequent leveling gains of 15.71 and 3.08 points in the largest original registration-gain wave. The 12-cell sparse check reports priority changes separately from all-missed ties.

The same-metric field control uses 38,436 matched pairs of virtual points with exact inputs. At 100 m the window-averaged 95th-percentile midpoint absolute error was 0.312 m, versus 0.186 m for repeat separation. Positions reconstructed with the correct timestamp gave numerical zero in both metrics. The revised text distinguishes this cancellation from absolute accuracy on actual returns, distinguishes physical crossing times from imposed delays, and reports the midpoint counts and timing gain alongside the yaw reversal. The irregular-wave comparison states its lower severity. The tank replay reports broadside, pitch/heave sign sensitivity, and its scale and roll assumptions.

The updated replication checkout is [emch574-radar-replication-v2](https://github.com/j-vaught/graduate-coursework/tree/emch574-radar-replication-v2/Semesters/Fa26/EMCH574/projects/radar-proposal-comparison/combined-wave-motion).
