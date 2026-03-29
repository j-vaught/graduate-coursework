= V3: VLM-Guided Segmentation <sec:v3>

@sec:v1 and @sec:v2 documented two attempts to train a compact RL policy that reproduces expert interactive segmentation behavior: a single-mask agent and a sub-mask decomposition agent. Both converged reliably under behavioral cloning but destabilized under RL fine-tuning, and neither discovered the decomposition strategies that oracle analysis confirmed to be valuable. V3 abandons the learned policy paradigm entirely. In its place, a vision-language model --- Qwen3-VL-8B-Instruct @bai2025qwen25vl --- acts as the policy backbone, zero-shot, using the same action space as V2 but reasoning about it via chain-of-thought visual analysis rather than learned weights. The hypothesis motivating V3 is that visual reasoning capabilities acquired from pretraining transfer directly to interactive segmentation, making the exploration problem that defeated V1 and V2 irrelevant.

== Architecture and Visual State Rendering <sec:v3_arch>

A trained RL agent receives a flattened tensor state---DINOv2 patch features, SAM mask logits, and click maps---and must learn to infer spatial relationships, detect segmentation errors, and form corrective click strategies entirely from weight-level feature interactions. V3 instead renders the complete segmentation state as a human-interpretable multi-panel image and passes it to a model whose pretraining has instilled deep spatial and semantic understanding. The VLM receives the same information an expert would: a reference example, the current query scene, the mask-in-progress, and a visual error map. No learned parameters are updated.

The backbone is Qwen3-VL-8B-Instruct @bai2025qwen25vl, an 8B-parameter vision-language model pretrained on large-scale image-text corpora and instruction-tuned for multi-image reasoning. Its weights are frozen throughout all V3 experiments. The VLM receives multi-image inputs (up to four panels in a single context window), produces structured JSON action outputs, and---critically---emits chain-of-thought reasoning traces before the action token. These reasoning traces are not used by the harness but are logged for post-hoc analysis. The VLM has not been exposed to FSS-1000 data, SAM outputs, or any task-specific examples during inference. Every episode is a zero-shot interaction in the strict sense: no in-context demonstrations, no task-specific system prompt beyond the action-space description, and no gradient-based adaptation.

#figure(
  image("../figures/fig_vlm_agent.pdf", width: 100%),
  caption: [V3 VLM-guided architecture. A 4-panel visual state is rendered and sent to Qwen3-VL-8B, which reasons about what action to take. The action is executed on SAM, and the result is reviewed.],
) <fig:vlm_agent>

All spatial coordinates passed to and from the VLM use the same $37 times 37$ grid system established in V1. The grid matches DINOv2's ViT-L/14 output resolution and covers the full $518 times 518$ input image ($14$ px per cell). Rows and columns are zero-indexed with decimal precision permitted, so valid coordinates lie in $[0, 36] times [0, 36]$. Converting a grid coordinate $(r, c)$ to a pixel position within a rendered panel of size $P times P$ pixels uses

$ (x_"px", y_"px") = ((c + 0.5)/(37) dot P, (r + 0.5)/(37) dot P). $

The reverse mapping from panel pixel to grid coordinate divides by cell width and floors. All grid-to-panel conversions are exact (no rounding artifacts) because panel sizes are integer multiples chosen to avoid sub-pixel alignment issues.

The primary visual input at each decision step is a $2 times 2$ composite image with each panel rendered at $400 times 400$ pixels (total: $800 times 800$ pixels), hereafter referred to as the _4-panel composite_ (@fig:vlm_agent). Panel A (top-left) shows the support (reference) image with the ground-truth target object mask rendered as a garnet outline overlaid on the reference; this panel communicates _what_ the target class looks like and its typical shape, color, and extent. Panel B (top-right) shows the raw query image with no overlays, giving the VLM an unoccluded view of the scene in which the target must be located, free of any overlay bias from the current segmentation state. Panel C (bottom-left) shows the query image with the current predicted mask overlaid; when multiple sub-masks are active, each is drawn in a distinct color (sub-mask 1: garnet, sub-mask 2: Atlantic blue, sub-mask 3: Horseshoe green, sub-mask 4: Honeycomb gold), with all positive clicks in the current session drawn as filled green circles and all negative clicks as filled red circles, making it immediately visible which regions have been independently committed. Panel D (bottom-right) shows a pixel-level error heatmap computed against the ground-truth mask, in which true positive pixels (correctly included) are rendered green, false negative pixels (missed foreground) are rendered red, and false positive pixels (incorrectly included background) are rendered blue; background true negatives are rendered as the original image at 30% opacity. The heatmap provides a direct error signal in pixel space: red regions direct the VLM to add foreground coverage, while blue regions direct it to shrink the mask. During inference without ground truth, Panel D is replaced by SAM's raw confidence heatmap scaled to the same color encoding.

Before executing any click action, the harness renders a dedicated _verification image_: a two-panel, $800 times 400$ side-by-side view. The left panel shows the query image with a crosshair drawn at the proposed click location; the crosshair is garnet for positive clicks and blue for negative. The right panel shows Panel D (the error map) with an identically positioned yellow crosshair, allowing the VLM to verify that the proposed location falls on the intended error class. The VLM can #text(fill: rgb("#73000A"))[CONFIRM], #text(fill: rgb("#73000A"))[REPOSITION] (providing updated coordinates), or #text(fill: rgb("#73000A"))[CANCEL]. If repositioned, the harness re-renders the verification image at the new coordinates and proceeds to execution without re-triggering a second verification round.

When the VLM requests a #text(fill: rgb("#73000A"))[ZOOM] action---appropriate for small objects, thin structures, or high-precision placement needs---the harness renders a two-panel $800 times 400$ _zoom image_ centered on the requested coordinates. The crop radius is $6$ grid cells (approximately $84$ pixels in the original image), yielding a $12 times 12$ grid-cell region. Both the query image and the error map are cropped to this region and independently scaled to $400 times 400$, preserving relative spatial relationships. A $12 times 12$ white grid is overlaid on both panels to give the VLM explicit spatial reference within the zoomed view. The VLM responds with either a precise click coordinate (in the original $37 times 37$ grid system) or #text(fill: rgb("#73000A"))[CANCEL].

All system constants for V3 are summarized in @tab:v3_constants.

#figure(
  table(
    columns: 3,
    table.hline(),
    [*Constant*], [*Value*], [*Role*],
    table.hline(),
    [`MAX_STEPS`],    [12],   [Hard episode step limit],
    [`MAX_SUBMASKS`], [4],    [Maximum independent SAM sessions per episode],
    [`PANEL_SIZE`],   [400],  [Per-panel pixel dimension (px)],
    [`ZOOM_RADIUS`],  [6],    [Crop half-width in grid cells],
    [`GRID_DIM`],     [37],   [Coordinate grid dimension],
    [`STOP_THRESHOLD`], [0.85], [Minimum Dice required to offer STOP],
    table.hline(),
  ),
  caption: [V3 system constants.],
) <tab:v3_constants>

== Three-Phase Decision Loop <sec:v3_loop>

#figure(
  image("../figures/fig_vlm_episode.pdf", width: 100%),
  caption: [V3 three-phase decision loop. Phase 1 selects an action, Phase 2 verifies spatial placement, Phase 3 evaluates the result.],
) <fig:vlm_episode>

Each step of an episode runs up to three VLM forward passes, one per phase. Not every phase fires on every step: STOP and UNDO skip phases 2 and 3 entirely; ZOOM replaces the normal phase 2 verification with the zoom interaction.

=== Phase 1: Action Selection <sec:phase1>

The harness sends the 4-panel composite image and a status line to the VLM. The status line reports the current step, Dice score, click count, and number of active sub-masks in a fixed-format string:

#block(inset: (left: 2em))[`Step 4/12. Dice: 0.452. Clicks: 3. Submasks: 1.`]

When the stuck detector fires (@sec:stuck), the status line is replaced by a coaching prompt that lists previously attempted coordinates, catalogues consecutive failures, and suggests alternative strategies.

The VLM selects one action from the following set and must respond with a single JSON object:

```text
{"action": "POSITIVE_CLICK", "row": 22.5, "col": 18.0,
 "reasoning": "<chain-of-thought>"}
```

The available actions are summarized in @tab:v3_actions.

#figure(
  table(
    columns: 2,
    align: (left, left),
    table.hline(),
    [*Action*], [*Description*],
    table.hline(),
    [POSITIVE_CLICK$(r, c)$], [Place a foreground seed at grid position $(r, c)$. Expands the mask toward red (missed) regions in Panel D.],
    [NEGATIVE_CLICK$(r, c)$], [Place a background seed at $(r, c)$. Shrinks the mask away from blue (extra) regions in Panel D.],
    [NEW_SUBMASK$(r, c)$], [Finalize the current sub-mask, increment the sub-mask counter, and initialize a fresh SAM session with a first positive click at $(r, c)$. Used when SAM has committed to an incorrect hypothesis and further clicks degrade rather than improve the mask. Prohibited if `MAX_SUBMASKS` has been reached.],
    [ZOOM$(r, c)$], [Request a zoomed two-panel view centered on $(r, c)$ before committing. The step counter is not incremented; the zoom response either places a click or cancels.],
    [STOP], [Accept the current union mask as the final prediction. Only offered by the harness when Dice $>= 0.85$.],
    table.hline(),
  ),
  caption: [V3 action space.],
) <tab:v3_actions>

The first action in every episode must be POSITIVE_CLICK (no mask exists to evaluate before the first click; STOP/UNDO are undefined).

=== Phase 1a: Zoom (Optional) <sec:phase1a>

If the VLM issues ZOOM$(r, c)$ in Phase 1, the harness immediately renders the zoom image described in @sec:v3_arch and sends it in a separate VLM call. The prompt asks the VLM to either place a click (returning new $(r', c')$ within the original coordinate system) or cancel. The zoom response bypasses the normal Phase 2 verification flow: if a click coordinate is returned, it is executed directly; if CANCEL is returned, the step is skipped and control returns to Phase 1 on the next step. No step credit is consumed on a zoom-cancel.

=== Phase 1b: Verification <sec:phase1b>

For all click actions that proceed from Phase 1 (or Phase 1a with a click response), the harness renders the two-panel verification image and sends it to the VLM with the prompt:

#block(inset: (left: 2em))[
  _"The crosshair shows where a POSITIVE click will land at (22.5, 18.0). Left: query image. Right: error map. Is this the right spot? CONFIRM / REPOSITION / CANCEL"_
]

The VLM can respond with one of three verdicts. CONFIRM executes the click immediately at the proposed coordinates. REPOSITION$(r', c')$ causes the harness to re-render the verification image at the new coordinates and execute without offering a further verification round. CANCEL abandons the click entirely, making no SAM call and returning control to Phase 1.

=== Phase 2: Execute and Review <sec:phase2>

After executing the click, the harness calls SAM with the updated click history and renders a two-panel _review image_: the updated Panel C (mask overlay) on the left with the new Dice printed, and the updated Panel D (error map) on the right with the Dice delta ($+Delta$ or $-Delta$) printed. The VLM is presented with one of two prompts depending on whether Dice has crossed the 0.85 threshold. When Dice $>= 0.85$ the STOP option is available and the prompt offers UNDO (revert), STOP (finalize), or CONTINUE (keep going). When Dice $< 0.85$ the STOP option is withheld and the prompt offers only UNDO or CONTINUE, with an explicit message that Dice has not yet reached the quality threshold.

The VLM's response determines the harness's behavior. UNDO causes the harness to remove the most recent click from the current sub-mask's click history, replay all remaining clicks through SAM from scratch to rebuild consistent logit state, and increment the undo counter; undo cannot cross sub-mask boundaries. STOP causes the harness to finalize the union of all sub-masks as the episode prediction and terminate the episode immediately. CONTINUE causes the harness to return to Phase 1 on the next step.

The three-phase loop deliberately decomposes an inherently multi-hypothetical task into calls that each involve only concrete visual evidence. Phase 1 sees the actual current state. Phase 1b sees the actual proposed point rendered on the actual image. Phase 2 sees the actual result. A single-call design would require the VLM to simultaneously reason about what action to take, whether the spatial placement is correct, and whether the predicted outcome justifies the action---three hypothetical futures stacked in one prompt. VLMs, like human experts, reason most reliably when given specific visual evidence rather than being asked to simulate unobserved outcomes. Phase separation also enables _error containment_: a bad click proposed in Phase 1 can be caught in Phase 1b before execution; a bad click that slips through can be caught in Phase 2 via undo. This redundancy is a key driver of V3's click efficiency---bad clicks rarely persist.

The harness implements a 5-stage robust parsing pipeline to handle VLM outputs that deviate from strict JSON. Stage 1 performs think-tag stripping, removing `<think>...</think>` blocks that Qwen3 emits before the answer token and passing the remaining text to the next stage. Stage 2 attempts a direct parse via `json.loads()` on the stripped output. Stage 3 performs markdown fence extraction, pulling the content of the first fenced code block (json or plain) and retrying `json.loads()`. Stage 4 applies brace extraction, using a greedy regex to find the outermost `{...}` substring before retrying `json.loads()`. Stage 5 performs field-level regex matching, extracting `action`, `row`, `col`, `verdict`, and `decision` fields individually using separate named-group patterns and constructing a synthetic dict from whatever fields are recoverable. If no field can be recovered at any stage, a default fallback treats the response as STOP, terminating the episode safely.

Coordinate validation clamps all $(r, c)$ to $[0, 36]$ after parsing. Missing or non-numeric coordinates on a click action trigger the default STOP fallback. In practice, stages 1--3 handle over 95% of outputs; stage 5 fires only on malformed or truncated responses.

== Prompt Engineering Iterations <sec:v3_prompts>

V3's final performance of 0.853 mean Dice was reached through four major prompt engineering iterations. Each iteration was evaluated on a fixed 5-image evaluation set (unless noted) from FSS-1000, using Qwen3-VL-8B-Instruct with a consistent hardware and temperature configuration ($T = 0$, greedy decoding). @tab:vlm_iters summarizes the complete progression.

#figure(
  table(
    columns: 5,
    table.hline(),
    [*Version*], [*$N$*], [*Mean Dice*], [*Mean Clicks*], [*Key Change*],
    table.hline(),
    [v1],     [5],  [0.476],         [6.6],        [Baseline: 4-panel composite, 3 actions (POS/NEG/STOP), single-call.],
    [v2],     [5],  [0.598],         [5.8],        [Added error heatmap (Panel D), NEW_SUBMASK, UNDO; introduced explicit verify phase.],
    [v2_r2],  [10], [0.616],         [6.7],        [Expanded to 10-image eval set; minor prompt wording.],
    [v3],     [5],  [0.623],         [9.2],        [Added ZOOM, nudge-based repositioning (8 directions, $plus.minus 3$ cells), 3-phase full loop.],
    [v4],     [5],  [*0.853*],       [*1.4*],      [Post-click review (Phase 2), STOP gated at 0.85, free repositioning, stuck detection.],
    [v4_r2],  [10], [0.724],         [1.1],        [Broader 10-image eval with harder object classes.],
    table.hline(),
  ),
  caption: [Prompt iteration results on FSS-1000 evaluation set. All runs use Qwen3-VL-8B-Instruct, zero-shot. Key changes column describes the primary modification from the previous version.],
) <tab:vlm_iters>

The initial v1 system used the 4-panel composite with a minimal prompt describing the three available actions (POSITIVE_CLICK, NEGATIVE_CLICK, STOP) and a brief instruction to place clicks on the target object. No verification step existed; clicks were executed immediately on VLM output. Performance was 0.476 mean Dice at 6.6 clicks. Post-hoc analysis of failure trajectories revealed two primary error patterns: (a) coordinate boundary errors, where the VLM placed clicks at the edge of the visible area rather than on the object, due to ambiguity in the grid-to-image mapping; and (b) premature stopping, where the VLM issued STOP after one or two clicks without observing the mask state, even when Dice was below 0.3.

The most impactful single change across all iterations (v2) was replacing Panel D with an explicit error heatmap. Prior to v2, Panel D showed either a SAM confidence map or was absent. Adding pixel-level green/red/blue error encoding gave the VLM a direct spatial error signal rather than requiring it to compare the mask overlay (Panel C) against its memory of the reference (Panel A) to infer errors. Performance improved from 0.476 to 0.598 Dice. Two new actions---NEW_SUBMASK and UNDO---were also introduced in v2 alongside a verify phase (the first form of Phase 1b), which required the VLM to confirm its chosen location before execution. Click count dropped from 6.6 to 5.8, indicating the verify phase already reduced wasted clicks.

V3 introduced two spatial precision mechanisms. First, the ZOOM action allowed the VLM to request a magnified view before committing a click, useful for objects whose fine-grained structure (e.g., thin edges, small holes) was not reliably discernible at the $37 times 37$ grid resolution. Second, the verify phase's repositioning was structured as a nudge system: the VLM could select from 8 cardinal and diagonal directions with magnitudes of 1 or 3 cells rather than specifying arbitrary coordinates, reducing coordinate error from free-form decimal entry. Performance improved modestly to 0.623 Dice, but click count _increased_ to 9.2. Post-hoc analysis showed the VLM was using the zoom and nudge mechanisms heavily---often issuing multiple zooms and repositioning attempts per click---which consumed step budget without proportionate Dice improvement. The verify phase's nudge structure also limited repositioning to a fixed grid, occasionally forcing suboptimal placements when the ideal location was not reachable from the proposed origin by any nudge vector.

The critical insight motivating v4 was that click _degradation_ was the primary performance bottleneck, not click _placement_. In v3 trajectories, approximately 30% of executed clicks reduced Dice, and the system had no mechanism to undo them. These degrading clicks compounded: a corrupted mask state in step $t$ made step $t+1$ harder, often triggering additional degrading clicks in a downward spiral that matched the PPO collapse pattern observed in V1 and V2.

V4's Phase 2 post-click review directly addresses this. After every executed click, the VLM sees the actual result and decides whether to accept, undo, or finalize. The empirical effect was immediate and large: $0.598 arrow.r 0.853$ Dice, and clicks dropped from 5.8 to 1.4. The click reduction is explained by two mechanisms: (a) the VLM identifies that one well-placed click is sufficient and issues STOP as soon as Dice $>= 0.85$, terminating episodes that would previously have continued under random click pressure; and (b) degrading clicks are undone immediately, keeping the mask state clean throughout the episode. Additionally, v4 replaced the nudge-based repositioning system with free-form decimal coordinate input, removing the nudge grid constraint that had limited v3's placement precision.

The STOP gating mechanism---withholding the STOP option below Dice $= 0.85$---was introduced in v4 after observing that the VLM would otherwise stop prematurely at Dice scores below 0.10. This is a harness-level constraint, not a learned behavior, and is transparent to the VLM in the sense that the prompt simply omits STOP when quality is insufficient.

== Stuck Detection and Coaching <sec:stuck>

In approximately 15% of v4 episodes, the VLM enters a local failure mode characterized by repeated attempts at similar coordinates that consistently degrade the mask and are subsequently undone. This behavior---which we call a _stuck loop_---arises when the VLM has formed an incorrect spatial model of the object location and cannot correct it through normal Phase 1 reasoning alone, because each subsequent 4-panel composite shows the same (unchanged) state and reinforces the same (incorrect) coordinate hypothesis.

The harness monitors three scalar counters that are reset at the start of each episode and updated each step. The counter `consecutive_undos` records the number of consecutive steps ending in Phase 2 UNDO. The counter `consecutive_fails` records the number of consecutive steps in which the executed click reduced Dice and was undone. A rolling buffer `tried_coords` stores the $(r, c)$ coordinates of the last 5 executed clicks.

The stuck detector fires when any of the following conditions holds:

$ &"consecutive_undos" >= 2, \
  &"consecutive_fails" >= 2, \
  &"step" >= 4 "AND" "Dice" < 0.10. $

The first condition catches oscillating behavior (try, undo, try, undo). The second catches systematic placement in a wrong region. The third catches early episodes where the VLM has not yet located the object after multiple steps---typically caused by the object being present in an unusual location or occupying a small fraction of the image.

When the stuck detector fires, the harness replaces the normal Phase 1 status line with a multi-part coaching prompt structured around four elements. First, an acknowledgment of failure state: "You have undone the last $k$ clicks in a row. The mask has not improved." Second, an enumeration of failed coordinates: the contents of `tried_coords` rendered as a comma-separated list, "Previously tried: $(r_1, c_1), (r_2, c_2), dots$ Avoid clicking near these locations." Third, a root-cause hypothesis in which the prompt identifies the most likely failure mode based on the current Dice and Panel D appearance, diagnosing one of coordinate fixation (repeated attempts at the same location), background confusion (blue regions in Panel D dominating), or object not found (green regions absent, indicating the mask has missed the object entirely). Fourth, strategy suggestions providing explicit action recommendations keyed to the diagnosed root cause: coordinate fixation triggers a suggestion to use ZOOM and look for the object in a different quadrant; background confusion triggers a suggestion to add NEGATIVE_CLICKs in the blue regions; object not found triggers a recommendation to start a NEW_SUBMASK and scan Panel B quadrant-by-quadrant for the target shape seen in Panel A.

The coaching prompt is presented on every step while the stuck condition persists; it does not fire once and then reset. The condition clears when the VLM executes a click that is accepted (not undone) in Phase 2, at which point both `consecutive_undos` and `consecutive_fails` are set to zero.

Episodes that triggered the stuck detector without coaching typically ended with the VLM exhausting its step budget at low Dice ($< 0.20$) due to continued coordinate fixation. With coaching, the same episodes show the VLM switching strategy---issuing ZOOM or NEW_SUBMASK---within one or two steps of the coaching prompt, and the majority eventually reach Dice $> 0.50$. Stuck detection was not active in v1--v3 and accounts for a portion of the improvement seen between v3 (0.623 Dice) and v4 (0.853 Dice) that is independent of the post-click review mechanism.

@tab:v3_summary consolidates the key architectural and behavioral properties of the V3 system against V1 and V2.

#figure(
  table(
    columns: 4,
    table.hline(),
    [*Property*], [*V1*], [*V2*], [*V3*],
    table.hline(),
    [Policy mechanism],           [Learned (BC+PPO)],    [Learned (BC+GRPO/PPO)],   [Zero-shot VLM reasoning],
    [Parameters (task-specific)], [27M],                 [37M],                     [0],
    [Action space size],          [3],                   [5],                       [5 (+ZOOM)],
    [Post-action undo],           [No],                  [No],                      [Yes (Phase 2)],
    [Sub-mask decomposition],     [No],                  [Yes (never used)],        [Yes (spontaneous)],
    [Stuck recovery],             [No],                  [No],                      [Yes (coaching)],
    [Best mean Dice],             [0.49],                [0.61],                    [*0.85*],
    [Mean clicks at best Dice],   [10.0],                [6.0],                     [*1.4*],
    [Training stability],         [Collapses],           [GRPO stable/PPO collapses], [N/A],
    table.hline(),
  ),
  caption: [System property comparison across all three paradigms.],
) <tab:v3_summary>

== Development Timeline

#figure(
  table(
    columns: (5.5em, 1fr),
    table.hline(),
    [*Date*], [*Milestone*],
    table.hline(),
    [Mar 12], [Grounded SAM2 baseline and VLM mask-judging framework (Qwen 3.5 VL) implemented for cross-architecture comparison.],
    [Mar 23], [VLM pilot v1: baseline single-prompt approach with Qwen3-VL-8B. Result: 0.476 Dice, 6.6 clicks. Dominant failure: coordinate inconsistency.],
    [Mar 23], [VLM pilot v2: error heatmap emphasis (Panel D), click verification phase, NEW_SUBMASK and UNDO actions. Result: 0.598 Dice, 5.8 clicks.],
    [Mar 23], [VLM pilot v3: nudge-based verification (8 directions), ZOOM action for small objects. Result: 0.623 Dice, 9.2 clicks. Modest gain, more clicks.],
    [Mar 23], [VLM pilot v4: post-click review with UNDO/STOP/CONTINUE, free repositioning, stuck detection with coaching prompts. Result: 0.853 Dice, 1.4 clicks.],
    [Mar 23], [15-class cross-architecture ablation: V1 0.411, V2 0.610, V3 0.776 mean Dice. V3 confirmed as best approach with 1.3 clicks.],
    [Mar 23], [All branches merged into vaught_rev3. V3 VLM proposal document and architectural diagrams finalized.],
    table.hline(),
  ),
  caption: [V3 development timeline (March 12--23, 2026).],
) <tab:v3_timeline>
