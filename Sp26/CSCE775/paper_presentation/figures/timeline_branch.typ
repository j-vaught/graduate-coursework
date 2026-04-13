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

#cetz.canvas(length: 1cm, {
  import cetz.draw: *

  // ── helpers ──────────────────────────────────────────────────────────
  let modeldot(pos, c) = circle(
    pos, radius: 0.09,
    fill: c,
    stroke: (paint: c.darken(50%), thickness: 0.4pt),
  )
  let bigdot(pos, c) = circle(
    pos, radius: 0.135,
    fill: c,
    stroke: (paint: c.darken(50%), thickness: 0.8pt),
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

  // dot + label in one call (label pos may differ from dot pos)
  let milestone(dot_pos, label_pos, dir, bold_txt, small_txt, c) = {
    modeldot(dot_pos, c)
    ml(label_pos, dir, bold_txt, small_txt)
  }

  let branchline(x1, x2, y, c, arrow: false) = {
    let s = (paint: c, thickness: 2.5pt, cap: "round")
    if arrow {
      line((x1, y), (x2, y), stroke: s, mark: (end: "stealth", fill: c, scale: 1.5))
    } else {
      line((x1, y), (x2, y), stroke: s)
    }
  }

  let fadeline(x1, x2, y, c) = {
    line((x1, y), (x2, y),
      stroke: (paint: c.transparentize(60%), thickness: 2pt, cap: "round", dash: "densely-dashed"))
  }

  let branchlabel(pos, c, body) = {
    content(pos, anchor: "east",
      align(right, par(leading: 0.25em, text(size: 11pt, weight: "bold", fill: c)[#body])))
  }

  let fork(from, to, c, thick: 2pt) = {
    let dx = to.at(0) - from.at(0)
    let c1 = (from.at(0) + dx * 0.5, from.at(1))
    let c2 = (to.at(0) - dx * 0.5, to.at(1))
    bezier(from, to, c1, c2,
      stroke: (paint: c, thickness: thick, cap: "round"))
  }

  let dashed_fork(from, to, c, arrow: true) = {
    let dx = to.at(0) - from.at(0)
    let c1 = (from.at(0) + dx * 0.5, from.at(1))
    let c2 = (to.at(0) - dx * 0.5, to.at(1))
    if arrow {
      bezier(from, to, c1, c2,
        stroke: (paint: c.transparentize(40%), thickness: 1.5pt, dash: "densely-dashed"),
        mark: (end: "stealth", fill: c.transparentize(40%)))
    } else {
      bezier(from, to, c1, c2,
        stroke: (paint: c.transparentize(40%), thickness: 1.5pt, dash: "densely-dashed"))
    }
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
    line((x, -15), (x, 14), stroke: (paint: bk10, thickness: 0.4pt))
    content((x, 14.5), text(size: 7pt, weight: "bold", fill: bk50)[#yr])
  }

  // ═════════════════════════════════════════════════════════════════════
  // 1. EVOLUTIONARY COMPUTATION  (y=12)
  // ═════════════════════════════════════════════════════════════════════
  branchlabel((-0.8, 12), garnet)[Evolutionary \ Computation]
  branchline(0, 34, 12, garnet) 
  //what we need is liek an X or temrination here. 

  milestone((2.4, 12),  (2.4, 12),  "above", "Fogel",            "Evol. Prog. '66",      garnet)
  milestone((4.2, 12),  (4.2, 12),  "below", "Rechenberg",       "Evol. Strat. '73",     garnet)
  milestone((4.7, 12),  (5.2, 12),  "above", "Holland",          "Genetic Alg. '75",     garnet)
  milestone((8.3, 12),  (8.3, 12),  "above", "Goldberg",         "GA Textbook '89",      garnet)
  milestone((9.1, 12),  (9.1, 12),  "below", "Koza",             "Genetic Prog. '92",    garnet)
  milestone((10.3, 12), (10.3, 12), "above", "Hansen",           "CMA-ES '96",           garnet)
  milestone((10.5, 12), (10.8, 12), "below", "Storn & Price",    "Diff. Evol. '97",      garnet)
  milestone((12.1, 12), (12.1, 12), "above", "Deb",              "NSGA-II '02",          garnet)
  milestone((13.6, 12), (13.6, 12), "below", "Zhang & Li",       "MOEA/D '07",           garnet)
  milestone((16.8, 12), (16.8, 12), "above", "Mouret",           "MAP-Elites '15",       garnet)
  milestone((23.9, 12), (23.9, 12), "below", "Real et al.",      "Evo. NAS '17-07",      garnet)
  milestone((28.8, 12), (28.8, 12), "below", "Ecoffet et al.",   "Go-Explore '19-01",    garnet)
  milestone((30.0, 12), (30.0, 12), "above", "Real et al.",      "AmoebaNet '19-02",     garnet)
  milestone((32.8, 12), (32.8, 12), "below", "Real",             "AutoML-Zero '20",      garnet)

  // ═════════════════════════════════════════════════════════════════════
  // 2. NEUROEVOLUTION / ES  (y=8.5)
  // ═════════════════════════════════════════════════════════════════════
  branchlabel((-0.8, 8.5), rose)[Neuroevolution]
  fork((9.3, 12), (12.2, 8.5), rose)
  forkannot((10.8, 10.2), rose)[evolve networks]
  branchline(12.2, 26, 8.5, rose)

  milestone((12.2, 8.5), (12.2, 8.5), "above", "NEAT",              "Stanley '02",     rose)
  milestone((14.2, 8.5), (14.2, 8.5), "below", "HyperNEAT",         "Stanley '09",     rose)
  milestone((14.9, 8.5), (15.5, 8.5), "above", "Novelty Search",    "Lehman '11",      rose)
  milestone((22.8, 8.5), (22.8, 8.5), "above", "OpenAI ES",         "Salimans '17",    rose)
  milestone((25.2, 8.5), (25.2, 8.5), "below", "Deep Neuroevol.",   "Such/Uber '17",   rose)
  milestone((24.9, 8.5), (24.9, 8.5), "above", "PBT",              "Jaderberg '17",    rose)

  // ═════════════════════════════════════════════════════════════════════
  // 3. RL FOUNDATIONS  (y=5, absorbed into Deep RL)
  // ═════════════════════════════════════════════════════════════════════
  branchlabel((-0.8, 5), congaree)[RL \ Foundations]
  branchline(0, 13, 5, congaree)
  fork((13, 5), (16.3, 1.5), congaree)
  mergeannot((14.6, 3.2))[deep function \ approximation]

  milestone((0.1, 5),  (0.1, 5),  "above", "Bellman",       "Dyn. Prog. '57",      congaree)
  milestone((8.1, 5),  (8.1, 5),  "below", "Sutton",        "TD Learning '88",     congaree)
  milestone((8.3, 5),  (8.8, 5),  "above", "Watkins",       "Q-Learning '89",      congaree)
  milestone((9.1, 5),  (9.6, 5),  "below", "Williams",      "REINFORCE '92",       congaree)
  milestone((11.4, 5), (11.4, 5), "above", "Sutton et al.", "Policy Grad. '99",    congaree)



  // ═════════════════════════════════════════════════════════════════════
  // 4. DEEP RL  (y=1.5, DOMINANT)
  // ═════════════════════════════════════════════════════════════════════
  branchlabel((-0.8, 1.5), atlantic)[Deep RL]
  branchline(16.3, 55, 1.5, atlantic, arrow: true)

  milestone((16.3, 1.5), (16.3, 1.5), "below", "DQN",            "Mnih '15-02",         atlantic)
  milestone((17.6, 1.5), (17.6, 1.5), "above", "TRPO",           "Schulman '15-07",     atlantic)
  milestone((18.1, 1.5), (18.1, 1.3), "below", "DDPG",           "Lillicrap '15-09",    atlantic)
  milestone((19.1, 1.5), (19.1, 1.5), "above", "AlphaGo",           "Silver '16-01",    atlantic)
  milestone((19.4, 1.5), (19.4, 1.5), "below", "A3C",            "Mnih '16-02",         atlantic)
  milestone((23.9, 1.5), (23.9, 1.5), "above", "PPO",           "Schulman '17-07",      atlantic)
  milestone((25.4, 1.5), (25.4, 1.5), "above", "SAC",            "Haarnoja '18-01",     atlantic)
  milestone((25.7, 1.5), (25.7, 1.5), "below", "TD3",            "Fujimoto '18-02",     atlantic)
  milestone((31.7, 1.5), (31.7, 1.5), "above", "MuZero",         "Schrittwieser '19-11",atlantic)
  milestone((37.2, 1.5), (37.2, 1.5), "below", "Decision Trans.","Chen '21-06",         atlantic)
  milestone((42.8, 1.5), (42.8, 1.5), "above", "DreamerV3",      "Hafner '23-01",       atlantic)

  // ═════════════════════════════════════════════════════════════════════
  // 5. RL FOR LLMs  (y=-2)
  // ═════════════════════════════════════════════════════════════════════
  branchlabel((-0.8, -2), garnet)[RL for LLMs]

  branchline(23.6, 55, -2, garnet, arrow: true)

  milestone((23.6, -2), (23.6, -2), "below", "RLHF",              "Christiano '17-06",       garnet)
  milestone((31.1, -2), (31.1, -2), "above", "Ziegler et al.",    "RLHF for Text '19-09",    garnet)
  milestone((34.6, -2), (34.6, -2), "below", "Stiennon et al.",   "Summarize w/ HF '20-09",  garnet)
  milestone((39.8, -2), (39.8, -2), "above", "InstructGPT",       "Ouyang '22-03",           garnet)
  milestone((42.5, -2), (42.5, -2), "below", "Constitutional AI", "Bai '22-12",              garnet)
  milestone((43.9, -2), (43.9, -2), "above", "DPO",               "Rafailov '23-05",         garnet)
  milestone((46.5, -2), (46.5, -2), "below", "GRPO",              "Shao '24-02",             garnet)
  milestone((49.8, -2), (49.8, -2), "above", "DeepSeek-R1",              "'25-01",           garnet)


  // ═════════════════════════════════════════════════════════════════════
  // 6. META-LEARNING / AutoRL  (y=-5.5)
  // ═════════════════════════════════════════════════════════════════════
  branchlabel((-0.8, -5.5), horseshoe)[Meta-Learning \ & AutoRL]
  branchline(20.5, 53.5, -5.5, horseshoe)

  milestone((20.5, -5.5), (20.5, -5.5), "below", "Learn to Learn",      "Andrychowicz '16-06", horseshoe)
  milestone((21.8, -5.5), (21.8, -5.5), "above", "RL^2",                "Duan '16-11",         horseshoe)
  milestone((22.8, -5.5), (22.8, -5.5), "below", "MAML",                "Finn '17-03",         horseshoe)
  milestone((25.7, -5.5), (25.7, -5.5), "above", "Evolved Pol. Grad.",  "Houthooft '18-02",    horseshoe)
  milestone((34.0, -5.5), (34.0, -5.5), "below", "LPG",                 "Oh '20-07",           horseshoe)
  milestone((35.8, -5.5), (35.8, -5.5), "above", "Evolving RL Alg.",    "Co-Reyes '21-01",     horseshoe)
  milestone((41.9, -5.5), (41.9, -5.5), "below", "Lu et al.",        "Disc. Pol. Opt. '22-10", horseshoe)
  milestone((45.4, -5.5), (45.4, -5.5), "above", "Maheshwari",          "GROOVE '23-10",       horseshoe)
  milestone((53, -5.5), (53, -5.5), "below", "DiscoRL",          "Oh '25-12 (Nature)",         horseshoe)
  

  // ═════════════════════════════════════════════════════════════════════
  // 7. LLM & CODE GENERATION  (y=-9)
  // ═════════════════════════════════════════════════════════════════════
  branchlabel((-0.8, -9), honeycomb)[LLM & \ Code Gen.]
  branchline(23.6, 41, -9, honeycomb)

  milestone((23.6, -9), (23.6, -9), "above", "Transformer", "Vaswani '17-06",     honeycomb)
  milestone((33.4, -9), (33.4, -9), "below", "GPT-3",       "Brown '20-05",       honeycomb)
  milestone((37.5, -9), (37.5, -9), "above", "Codex",       "Chen '21-07",        honeycomb)
  milestone((39.5, -9), (39.5, -9), "above", "AlphaCode",   "Li '22-02",          honeycomb)

  // ═════════════════════════════════════════════════════════════════════
  // 8. LLM-GUIDED EVOLUTION  (y=-12.5)
  // ═════════════════════════════════════════════════════════════════════
  branchlabel((-0.8, -12.5), atlantic)[LLM-Guided \ Evolution]

  fork((39.65, -9), (40.7, -12.5), atlantic)
  forkannot((40.2, -10.8), atlantic)[LLM + evolution]

  branchline(40.7, 57, -12.5, atlantic, arrow: true)

  milestone((40.7, -12.5), (40.7, -12.5), "below", "ELM",        "Lehman '22-06",       atlantic)
  milestone((45.4, -12.5), (45.4, -12.5), "below", "Eureka",     "Ma '23-10",           atlantic)
  milestone((46.2, -12.5), (46.2, -12.5), "above", "FunSearch",  "Romera-P. '24-01",    atlantic)
  milestone((47.7, -12.5), (47.7, -12.5), "below", "REvolve",    "Hazra '24-06",        atlantic)
  milestone((50.6, -12.5), (50.6, -12.5), "above", "EvoTune",    "Surina '25-04",       atlantic)
  milestone((51.2, -12.5), (51.2, -12.5), "below", "AlphaEvolve","Novikov '25-06",      atlantic)
  milestone((53.5, -12.5), (53.5, -12.5), "above", "AlphaEvolve", "MARL '26-02",        atlantic)
  milestone((53.8, -12.5), (53.8, -12.5), "below", "Evolving RL via LLMs", "GECCO '26-03",        atlantic)

})
