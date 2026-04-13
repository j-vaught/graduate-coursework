// Research Genealogy — Branch Timeline (Typst / CeTZ port of timeline_branch.tex)
#import "@preview/cetz:0.4.2"

#set page(width: auto, height: auto, margin: 14pt)
#set text(font: "Helvetica")

#let garnet    = rgb("#73000A")
#let rose      = rgb("#CC2E40")
#let atlantic  = rgb("#466A9F")
#let congaree  = rgb("#1F414D")
#let horseshoe = rgb("#65780B")
#let honeycomb = rgb("#A49137")
#let warmgrey  = rgb("#676156")
#let bk90      = rgb("#363636")
#let bk70      = rgb("#5C5C5C")
#let bk50      = rgb("#A2A2A2")
#let bk30      = rgb("#C7C7C7")
#let bk10      = rgb("#ECECEC")

// ── layout knobs ────────────────────────────────────────────────────────
// Change `spacing` to expand/compress the whole chart vertically.
#let spacing = 3.5
#let y_top   = 12
#let y_ec    = y_top - 0 * spacing   // Evolutionary Computation
#let y_neuro = y_top - 1 * spacing   // Neuroevolution
#let y_rlf   = y_top - 2 * spacing   // RL Foundations
#let y_deep  = y_top - 3 * spacing   // Deep RL
#let y_llmrl = y_top - 4 * spacing   // RL for LLMs
#let y_meta  = y_top - 5 * spacing   // Meta-Learning & AutoRL
#let y_code  = y_top - 6 * spacing   // LLM & Code Gen.
#let y_llme  = y_top - 7 * spacing   // LLM-Guided Evolution

// grid extends slightly past the outermost branches
#let grid_top = y_ec   + 0.6 * spacing
#let grid_bot = y_llme - 0.7 * spacing

#cetz.canvas(length: 1cm, {
  import cetz.draw: *

  // ── helpers ──────────────────────────────────────────────────────────
  let modeldot(pos, c) = circle(
    pos, radius: 0.09,
    fill: c,
    stroke: (paint: c.darken(50%), thickness: 0.4pt),
  )

  // milestone label (bold line + scriptsize line) — centered
  let ml(pos, dir, bold_txt, small_txt, c: bk70) = {
    let anchor = if dir == "above" { "south" } else { "north" }
    let dy     = if dir == "above" { 0.18 }      else { -0.18 }
    content(
      (pos.at(0), pos.at(1) + dy),
      anchor: anchor,
      align(center, par(leading: 0.25em,
        text(size: 7pt, fill: c)[
          *#bold_txt* \
          #text(size: 5.5pt)[#small_txt]
        ]
      ))
    )
  }

  let milestone(dot_pos, label_pos, dir, bold_txt, small_txt, c) = {
    modeldot(dot_pos, c)
    ml(label_pos, dir, bold_txt, small_txt)
  }

  let branchlabel(pos, c, body) = {
    content(pos, anchor: "east",
      align(right, par(leading: 0.25em, text(size: 11pt, weight: "bold", fill: c)[#body])))
  }

  // ── branch: label + line + one of three terminations ───────────────
  //   end: "arrow"     → arrowhead at x_end
  //   end: "terminate" → ✕ at x_end (branch dies)
  //   end: "fade"      → abrupt stop at x_end (for merging into other branches)
  let branch(yv, x_start, x_end, c, label, end: "arrow") = {
    branchlabel((-0.8, yv), c, label)
    let stroke_main = (paint: c, thickness: 2.5pt, cap: "round")
    if end == "arrow" {
      line((x_start, yv), (x_end, yv),
        stroke: stroke_main,
        mark: (end: "stealth", fill: c, scale: 1.5))
    } else if end == "terminate" {
      line((x_start, yv), (x_end, yv), stroke: stroke_main)
      let r = 0.315
      let x_stroke = (paint: garnet, thickness: 4.2pt, cap: "round")
      line((x_end - r, yv - r), (x_end + r, yv + r), stroke: x_stroke)
      line((x_end - r, yv + r), (x_end + r, yv - r), stroke: x_stroke)
    } else if end == "fade" {
      line((x_start, yv), (x_end, yv), stroke: stroke_main)
    }
  }

  let fork(from, to, c, thick: 2pt) = {
    let dx = to.at(0) - from.at(0)
    let c1 = (from.at(0) + dx * 0.5, from.at(1))
    let c2 = (to.at(0) - dx * 0.5, to.at(1))
    bezier(from, to, c1, c2,
      stroke: (paint: c, thickness: thick, cap: "round"))
  }

  let mergeannot(pos, body) = content(pos,
    box(fill: white, inset: 2pt,
      align(center, par(leading: 0.3em, text(size: 6pt, style: "italic", fill: bk50)[#body]))))

  let forkannot(pos, c, body) = content(pos,
    box(fill: white, inset: 1pt,
      align(center, text(size: 6pt, style: "italic", fill: c)[#body])))

  // ── year grid (drawn first so it sits behind branches) ───────────────
  let years = (
    (0.1, "1957"), (2.4, "1966"), (4.7, "1975"), (9.1, "1992"),
    (11.4, "1999"), (12.2, "2002"), (16.3, "2015"), (19.1, "2016"),
    (22.8, "2017"), (25.4, "2018"), (31.7, "2019"), (32.8, "2020"),
    (37.2, "2021"), (39.5, "2022"), (42.8, "2023"), (46.2, "2024"),
    (49.8, "2025"), (53.8, "2026"),
  )
  for (x, yr) in years {
    line((x, grid_bot), (x, grid_top), stroke: (paint: bk10, thickness: 0.4pt))
    content((x, grid_top + 0.5), text(size: 7pt, weight: "bold", fill: bk50)[#yr])
  }

  // ═════════════════════════════════════════════════════════════════════
  // 1. EVOLUTIONARY COMPUTATION
  // ═════════════════════════════════════════════════════════════════════
  branch(y_ec, 0, 34, garnet, [Evolutionary \ Computation], end: "terminate")

  milestone((2.4,  y_ec), (2.4,  y_ec), "above", "Fogel",         "Evol. Prog. '66",   garnet)
  milestone((4.2,  y_ec), (4.2,  y_ec), "below", "Rechenberg",    "Evol. Strat. '73",  garnet)
  milestone((4.7,  y_ec), (5.2,  y_ec), "above", "Holland",       "Genetic Alg. '75",  garnet)
  milestone((8.3,  y_ec), (8.3,  y_ec), "above", "Goldberg",      "GA Textbook '89",   garnet)
  milestone((9.1,  y_ec), (9.1,  y_ec), "below", "Koza",          "Genetic Prog. '92", garnet)
  milestone((10.3, y_ec), (10.3, y_ec), "above", "Hansen",        "CMA-ES '96",        garnet)
  milestone((10.5, y_ec), (10.8, y_ec), "below", "Storn & Price", "Diff. Evol. '97",   garnet)
  milestone((12.1, y_ec), (12.1, y_ec), "above", "Deb",           "NSGA-II '02",       garnet)
  milestone((13.6, y_ec), (13.6, y_ec), "below", "Zhang & Li",    "MOEA/D '07",        garnet)
  milestone((16.8, y_ec), (16.8, y_ec), "above", "Mouret",        "MAP-Elites '15",    garnet)
  milestone((23.9, y_ec), (23.9, y_ec), "below", "Real et al.",   "Evo. NAS '17-07",   garnet)
  milestone((28.8, y_ec), (28.8, y_ec), "below", "Ecoffet et al.","Go-Explore '19-01", garnet)
  milestone((30.0, y_ec), (30.0, y_ec), "above", "Real et al.",   "AmoebaNet '19-02",  garnet)
  milestone((32.8, y_ec), (32.8, y_ec), "below", "Real",          "AutoML-Zero '20",   garnet)

  // ═════════════════════════════════════════════════════════════════════
  // 2. NEUROEVOLUTION / ES
  // ═════════════════════════════════════════════════════════════════════
  branch(y_neuro, 12.2, 28, rose, [Neuroevolution], end: "terminate")
  fork((9.3, y_ec), (12.2, y_neuro), rose)
  forkannot((10.8, (y_ec + y_neuro) / 2 + 0.4), rose)[evolve networks]

  milestone((12.2, y_neuro), (12.2, y_neuro), "above", "NEAT",            "Stanley '02",    rose)
  milestone((14.2, y_neuro), (14.2, y_neuro), "below", "HyperNEAT",       "Stanley '09",    rose)
  milestone((14.9, y_neuro), (15.5, y_neuro), "above", "Novelty Search",  "Lehman '11",     rose)
  milestone((22.8, y_neuro), (22.8, y_neuro), "above", "OpenAI ES",       "Salimans '17",   rose)
  milestone((25.2, y_neuro), (25.2, y_neuro), "below", "Deep Neuroevol.", "Such/Uber '17",  rose)
  milestone((24.9, y_neuro), (24.9, y_neuro), "above", "PBT",             "Jaderberg '17",  rose)

  // ═════════════════════════════════════════════════════════════════════
  // 3. RL FOUNDATIONS
  // ═════════════════════════════════════════════════════════════════════
  branch(y_rlf, 0, 13, congaree, [RL \ Foundations], end: "fade")
  fork((13, y_rlf), (16.3, y_deep), congaree)
  mergeannot((14.6, (y_rlf + y_deep) / 2 - 0.1))[deep function \ approximation]

  milestone((0.1,  y_rlf), (0.1,  y_rlf), "above", "Bellman",       "Dyn. Prog. '57",   congaree)
  milestone((8.1,  y_rlf), (8.1,  y_rlf), "below", "Sutton",        "TD Learning '88",  congaree)
  milestone((8.3,  y_rlf), (8.8,  y_rlf), "above", "Watkins",       "Q-Learning '89",   congaree)
  milestone((9.1,  y_rlf), (9.6,  y_rlf), "below", "Williams",      "REINFORCE '92",    congaree)
  milestone((11.4, y_rlf), (11.4, y_rlf), "above", "Sutton et al.", "Policy Grad. '99", congaree)

  // ═════════════════════════════════════════════════════════════════════
  // 4. DEEP RL
  // ═════════════════════════════════════════════════════════════════════
  branch(y_deep, 16.3, 55, atlantic, [Deep RL], end: "arrow")

  milestone((16.3, y_deep), (16.3, y_deep), "below", "DQN",             "Mnih '15-02",          atlantic)
  milestone((17.6, y_deep), (17.6, y_deep), "above", "TRPO",            "Schulman '15-07",      atlantic)
  milestone((18.1, y_deep), (18.1, y_deep - 0.2), "below", "DDPG",      "Lillicrap '15-09",     atlantic)
  milestone((19.1, y_deep), (19.1, y_deep), "above", "AlphaGo",         "Silver '16-01",        atlantic)
  milestone((19.4, y_deep), (19.4, y_deep), "below", "A3C",             "Mnih '16-02",          atlantic)
  milestone((23.9, y_deep), (23.9, y_deep), "above", "PPO",             "Schulman '17-07",      atlantic)
  milestone((25.4, y_deep), (25.4, y_deep), "above", "SAC",             "Haarnoja '18-01",      atlantic)
  milestone((25.7, y_deep), (25.7, y_deep), "below", "TD3",             "Fujimoto '18-02",      atlantic)
  milestone((31.7, y_deep), (31.7, y_deep), "above", "MuZero",          "Schrittwieser '19-11", atlantic)
  milestone((37.2, y_deep), (37.2, y_deep), "below", "Decision Trans.", "Chen '21-06",          atlantic)
  milestone((42.8, y_deep), (42.8, y_deep), "above", "DreamerV3",       "Hafner '23-01",        atlantic)

  // ═════════════════════════════════════════════════════════════════════
  // 5. RL FOR LLMs
  // ═════════════════════════════════════════════════════════════════════
  branch(y_llmrl, 23.6, 55, garnet, [RL for LLMs], end: "arrow")

  milestone((23.6, y_llmrl), (23.6, y_llmrl), "below", "RLHF",              "Christiano '17-06",      garnet)
  milestone((31.1, y_llmrl), (31.1, y_llmrl), "above", "Ziegler et al.",    "RLHF for Text '19-09",   garnet)
  milestone((34.6, y_llmrl), (34.6, y_llmrl), "below", "Stiennon et al.",   "Summarize w/ HF '20-09", garnet)
  milestone((39.8, y_llmrl), (39.8, y_llmrl), "above", "InstructGPT",       "Ouyang '22-03",          garnet)
  milestone((42.5, y_llmrl), (42.5, y_llmrl), "below", "Constitutional AI", "Bai '22-12",             garnet)
  milestone((43.9, y_llmrl), (43.9, y_llmrl), "above", "DPO",               "Rafailov '23-05",        garnet)
  milestone((46.5, y_llmrl), (46.5, y_llmrl), "below", "GRPO",              "Shao '24-02",            garnet)
  milestone((49.8, y_llmrl), (49.8, y_llmrl), "above", "DeepSeek-R1",       "'25-01",                 garnet)

  // ═════════════════════════════════════════════════════════════════════
  // 6. META-LEARNING / AutoRL
  // ═════════════════════════════════════════════════════════════════════
  branch(y_meta, 20.5, 53.5, horseshoe, [Meta-Learning \ & AutoRL], end: "fade")

  milestone((20.5, y_meta), (20.5, y_meta), "below", "Learn to Learn",     "Andrychowicz '16-06",    horseshoe)
  milestone((21.8, y_meta), (21.8, y_meta), "above", "RL^2",               "Duan '16-11",            horseshoe)
  milestone((22.8, y_meta), (22.8, y_meta), "below", "MAML",               "Finn '17-03",            horseshoe)
  milestone((25.7, y_meta), (25.7, y_meta), "above", "Evolved Pol. Grad.", "Houthooft '18-02",       horseshoe)
  milestone((34.0, y_meta), (34.0, y_meta), "below", "LPG",                "Oh '20-07",              horseshoe)
  milestone((35.8, y_meta), (35.8, y_meta), "above", "Evolving RL Alg.",   "Co-Reyes '21-01",        horseshoe)
  milestone((41.9, y_meta), (41.9, y_meta), "below", "Lu et al.",          "Disc. Pol. Opt. '22-10", horseshoe)
  milestone((45.4, y_meta), (45.4, y_meta), "above", "Maheshwari",         "GROOVE '23-10",          horseshoe)
  milestone((53.0, y_meta), (53.0, y_meta), "below", "DiscoRL",            "Oh '25-12 (Nature)",     horseshoe)

  // ═════════════════════════════════════════════════════════════════════
  // 7. LLM & CODE GENERATION
  // ═════════════════════════════════════════════════════════════════════
  branch(y_code, 23.6, 41, honeycomb, [LLM & \ Code Gen.], end: "fade")

  milestone((23.6, y_code), (23.6, y_code), "above", "Transformer", "Vaswani '17-06", honeycomb)
  milestone((33.4, y_code), (33.4, y_code), "below", "GPT-3",       "Brown '20-05",   honeycomb)
  milestone((37.5, y_code), (37.5, y_code), "above", "Codex",       "Chen '21-07",    honeycomb)
  milestone((39.5, y_code), (39.5, y_code), "above", "AlphaCode",   "Li '22-02",      honeycomb)

  // ═════════════════════════════════════════════════════════════════════
  // 8. LLM-GUIDED EVOLUTION
  // ═════════════════════════════════════════════════════════════════════
  branch(y_llme, 40.7, 57, atlantic, [LLM-Guided \ Evolution], end: "arrow")
  fork((39.65, y_code), (40.7, y_llme), atlantic)
  forkannot((40.2, (y_code + y_llme) / 2 + 0.5), atlantic)[LLM + evolution]

  milestone((40.7, y_llme), (40.7, y_llme), "below", "ELM",         "Lehman '22-06",    atlantic)
  milestone((45.4, y_llme), (45.4, y_llme), "below", "Eureka",      "Ma '23-10",        atlantic)
  milestone((46.2, y_llme), (46.2, y_llme), "above", "FunSearch",   "Romera-P. '24-01", atlantic)
  milestone((47.7, y_llme), (47.7, y_llme), "below", "REvolve",     "Hazra '24-06",     atlantic)
  milestone((50.6, y_llme), (50.6, y_llme), "above", "EvoTune",     "Surina '25-04",    atlantic)
  milestone((51.2, y_llme), (51.2, y_llme), "below", "AlphaEvolve", "Novikov '25-06",   atlantic)
  milestone((53.5, y_llme), (53.5, y_llme), "above", "AlphaEvolve", "MARL '26-02",      atlantic)
  milestone((53.8, y_llme), (53.8, y_llme), "below", "Evolving RL via LLMs", "GECCO '26-03", atlantic)
})
