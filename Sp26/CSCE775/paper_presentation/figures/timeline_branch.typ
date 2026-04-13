// Research Genealogy — Branch Timeline (data-driven Typst/CeTZ version)
#import "@preview/cetz:0.4.2"

#set page(width: auto, height: auto, margin: 14pt)
#set text(font: "Helvetica")

// ── palette ─────────────────────────────────────────────────────────────
#let garnet    = rgb("#73000A")
#let rose      = rgb("#CC2E40")
#let atlantic  = rgb("#466A9F")
#let congaree  = rgb("#1F414D")
#let horseshoe = rgb("#65780B")
#let honeycomb = rgb("#A49137")
#let bk50      = rgb("#A2A2A2")
#let bk70      = rgb("#5C5C5C")
#let bk10      = rgb("#ECECEC")

// ── layout knobs ────────────────────────────────────────────────────────
// vertical spacing between branch lanes
#let spacing = 3.5
// year-width model: width(year) = year_base_w + count(year) * year_per_item
// empty years collapse to year_base_w; dense years expand automatically.
#let year_base_w   = 0.0
#let year_per_item = 0.9

// branch y-coordinates (derived from spacing — change `spacing` to reflow)
#let y_top   = 12
#let y_ec    = y_top - 0 * spacing
#let y_neuro = y_top - 1 * spacing
#let y_rlf   = y_top - 2 * spacing
#let y_deep  = y_top - 3 * spacing
#let y_llmrl = y_top - 4 * spacing
#let y_llme  = y_top - 5 * spacing
#let y_code  = y_top - 6 * spacing
#let y_meta  = y_top - 7 * spacing
#let grid_top = y_ec   + 0.6 * spacing
#let grid_bot = y_meta - 0.7 * spacing

// ── branches ────────────────────────────────────────────────────────────
// start/end are (year, month) tuples; month ∈ [0,12]; year may exceed the
// data's max (extrapolates using last year's width — handy for arrows).
// end_style: "arrow" | "terminate" | "fade".
#let branches = (
  ec:    (y: y_ec,    color: garnet,    label: [Evolutionary \ Computation],
          start: (1957, 0),  end: (2027, 3),  end_style: "arrow"),
  neuro: (y: y_neuro, color: rose,      label: [Neuroevolution],
          start: (2002, 0),  end: (2020, 0),  end_style: "fade"),
  rlf:   (y: y_rlf,   color: congaree,  label: [RL \ Foundations],
          start: (1957, 0),  end: (2002, 0),  end_style: "fade"),
  deep:  (y: y_deep,  color: atlantic,  label: [Deep RL],
          start: (2015, 2),  end: (2027, 3),  end_style: "arrow"),
  llmrl: (y: y_llmrl, color: garnet,    label: [RL for LLMs],
          start: (2017, 6),  end: (2027, 3),  end_style: "arrow"),
  meta:  (y: y_meta,  color: horseshoe, label: [Meta-Learning \ & AutoRL],
          start: (2016, 6),  end: (2027, 3),  end_style: "arrow"),
  code:  (y: y_code,  color: honeycomb, label: [LLM & \ Code Gen.],
          start: (2017, 6),  end: (2027, 3),  end_style: "arrow"),
  llme:  (y: y_llme,  color: atlantic,  label: [LLM-Guided \ Evolution],
          start: (2022, 6),  end: (2027, 3),  end_style: "arrow"),
)

// ── milestones ──────────────────────────────────────────────────────────
// Each item lives on one branch. Month only controls ORDER within its year;
// actual x is computed by evenly spreading items across that year's slot.
#let items = (
  // Evolutionary Computation
  (branch: "ec", year: 1966, month: 0,  dir: "above", bold: "Fogel",          small: "Evol. Prog. '66"),
  (branch: "ec", year: 1973, month: 0,  dir: "below", bold: "Rechenberg",     small: "Evol. Strat. '73"),
  (branch: "ec", year: 1975, month: 0,  dir: "above", bold: "Holland",        small: "Genetic Alg. '75"),
  (branch: "ec", year: 1989, month: 0,  dir: "above", bold: "Goldberg",       small: "GA Textbook '89"),
  (branch: "ec", year: 1992, month: 0,  dir: "below", bold: "Koza",           small: "Genetic Prog. '92"),
  (branch: "ec", year: 1995, month: 0,  dir: "above", bold: "Kennedy & Eberhart", small: "PSO '95"),
  (branch: "ec", year: 1996, month: 0,  dir: "above", bold: "Hansen",         small: "CMA-ES '96"),
  (branch: "ec", year: 1997, month: 0,  dir: "below", bold: "Storn & Price",  small: "Diff. Evol. '97"),
  (branch: "ec", year: 2002, month: 0,  dir: "above", bold: "Deb",            small: "NSGA-II '02"),
  (branch: "ec", year: 2007, month: 0,  dir: "below", bold: "Zhang & Li",     small: "MOEA/D '07"),
  (branch: "ec", year: 2015, month: 0,  dir: "above", bold: "Mouret",         small: "MAP-Elites '15"),
  (branch: "ec", year: 2017, month: 7,  dir: "below", bold: "Real et al.",    small: "Evo. NAS '17-07"),
  (branch: "ec", year: 2019, month: 1,  dir: "below", bold: "Wang et al.",    small: "POET '19-01"),
  (branch: "ec", year: 2019, month: 2,  dir: "above", bold: "Ecoffet et al.", small: "Go-Explore '19-02"),
  (branch: "ec", year: 2019, month: 3,  dir: "below", bold: "Real et al.",    small: "AmoebaNet '19-03"),
  (branch: "ec", year: 2020, month: 0,  dir: "below", bold: "Real",           small: "AutoML-Zero '20"),
  (branch: "ec", year: 2021, month: 6,  dir: "above", bold: "Fontaine",       small: "DQD '21-06"),
  (branch: "ec", year: 2022, month: 2,  dir: "above", bold: "Pierrot et al.", small: "QD-PG '22-02"),
  (branch: "ec", year: 2022, month: 4,  dir: "below", bold: "Lim et al.",     small: "QDax '22-04"),
  (branch: "ec", year: 2022, month: 12, dir: "above", bold: "Lange",          small: "evosax '22-12"),
  (branch: "ec", year: 2023, month: 7,  dir: "below", bold: "Fontaine",       small: "CMA-MAE '23-07"),
  (branch: "ec", year: 2023, month: 10, dir: "above", bold: "Lim et al.",     small: "QD w/ AI Feedback '23-10"),
  (branch: "ec", year: 2024, month: 3,  dir: "above", bold: "Akiba et al.",   small: "Evol. Model Merging '24-03"),
  (branch: "ec", year: 2024, month: 8,  dir: "below", bold: "Lu et al.",      small: "AI Scientist '24-08"),
  (branch: "ec", year: 2025, month: 2,  dir: "above", bold: "Sakana",         small: "AI CUDA Engineer '25-02"),
  // Neuroevolution
  (branch: "neuro", year: 2002, month: 0,  dir: "above", bold: "NEAT",            small: "Stanley '02"),
  (branch: "neuro", year: 2009, month: 0,  dir: "below", bold: "HyperNEAT",       small: "Stanley '09"),
  (branch: "neuro", year: 2011, month: 0,  dir: "above", bold: "Novelty Search",  small: "Lehman '11"),
  (branch: "neuro", year: 2017, month: 3,  dir: "above", bold: "OpenAI ES",       small: "Salimans '17"),
  (branch: "neuro", year: 2017, month: 6,  dir: "below", bold: "Deep Neuroevol.", small: "Such/Uber '17"),
  (branch: "neuro", year: 2017, month: 9,  dir: "above", bold: "PBT",             small: "Jaderberg '17"),
  // RL Foundations
  (branch: "rlf", year: 1957, month: 0, dir: "above", bold: "Bellman",        small: "Dyn. Prog. '57"),
  (branch: "rlf", year: 1988, month: 0, dir: "below", bold: "Sutton",         small: "TD Learning '88"),
  (branch: "rlf", year: 1989, month: 0, dir: "above", bold: "Watkins",        small: "Q-Learning '89"),
  (branch: "rlf", year: 1992, month: 0, dir: "below", bold: "Williams",       small: "REINFORCE '92"),
  (branch: "rlf", year: 1999, month: 0, dir: "above", bold: "Sutton et al.", small: "Policy Grad. '99"),
  // Deep RL
  (branch: "deep", year: 2015, month: 2,  dir: "below", bold: "DQN",             small: "Mnih '15-02"),
  (branch: "deep", year: 2015, month: 7,  dir: "above", bold: "TRPO",            small: "Schulman '15-07"),
  (branch: "deep", year: 2015, month: 9,  dir: "below", bold: "DDPG",            small: "Lillicrap '15-09"),
  (branch: "deep", year: 2016, month: 1,  dir: "above", bold: "AlphaGo",         small: "Silver '16-01"),
  (branch: "deep", year: 2016, month: 2,  dir: "below", bold: "A3C",             small: "Mnih '16-02"),
  (branch: "deep", year: 2017, month: 7,  dir: "above", bold: "PPO",             small: "Schulman '17-07"),
  (branch: "deep", year: 2017, month: 12, dir: "below", bold: "AlphaZero",       small: "Silver '17-12"),
  (branch: "deep", year: 2018, month: 1,  dir: "above", bold: "SAC",             small: "Haarnoja '18-01"),
  (branch: "deep", year: 2018, month: 2,  dir: "below", bold: "IMPALA",          small: "Espeholt '18-02"),
  (branch: "deep", year: 2018, month: 3,  dir: "above", bold: "TD3",             small: "Fujimoto '18-03"),
  (branch: "deep", year: 2019, month: 10, dir: "below", bold: "AlphaStar",       small: "Vinyals '19-10"),
  (branch: "deep", year: 2019, month: 11, dir: "above", bold: "MuZero",          small: "Schrittwieser '19-11"),
  (branch: "deep", year: 2020, month: 3,  dir: "below", bold: "Agent57",         small: "Badia '20-03"),
  (branch: "deep", year: 2020, month: 6,  dir: "above", bold: "CQL",             small: "Kumar '20-06"),
  (branch: "deep", year: 2021, month: 6,  dir: "below", bold: "Decision Trans.", small: "Chen '21-06"),
  (branch: "deep", year: 2022, month: 5,  dir: "above", bold: "Gato",            small: "Reed '22-05"),
  (branch: "deep", year: 2023, month: 1,  dir: "above", bold: "DreamerV3",       small: "Hafner '23-01"),
  (branch: "deep", year: 2023, month: 3,  dir: "below", bold: "Diffusion Policy", small: "Chi '23-03"),
  (branch: "deep", year: 2023, month: 6,  dir: "below", bold: "AlphaDev",        small: "Mankowitz '23-06"),
  (branch: "deep", year: 2023, month: 10, dir: "above", bold: "TD-MPC2",         small: "Hansen '23-10"),
  (branch: "deep", year: 2024, month: 2,  dir: "above", bold: "Genie",           small: "Bruce '24-02"),
  (branch: "deep", year: 2024, month: 3,  dir: "below", bold: "SIMA",            small: "DeepMind '24-03"),
  (branch: "deep", year: 2024, month: 6,  dir: "above", bold: "OpenVLA",         small: "Kim '24-06"),
  (branch: "deep", year: 2024, month: 10, dir: "below", bold: "π0",              small: "Physical Intel. '24-10"),
  (branch: "deep", year: 2025, month: 3,  dir: "above", bold: "Gemini Robotics", small: "DeepMind '25-03"),
  // RL for LLMs
  (branch: "llmrl", year: 2017, month: 6,  dir: "below", bold: "RLHF",              small: "Christiano '17-06"),
  (branch: "llmrl", year: 2019, month: 9,  dir: "above", bold: "Ziegler et al.",    small: "RLHF for Text '19-09"),
  (branch: "llmrl", year: 2020, month: 9,  dir: "below", bold: "Stiennon et al.",   small: "Summarize w/ HF '20-09"),
  (branch: "llmrl", year: 2022, month: 3,  dir: "above", bold: "InstructGPT",       small: "Ouyang '22-03"),
  (branch: "llmrl", year: 2022, month: 12, dir: "below", bold: "Constitutional AI", small: "Bai '22-12"),
  (branch: "llmrl", year: 2023, month: 5,  dir: "above", bold: "DPO",               small: "Rafailov '23-05"),
  (branch: "llmrl", year: 2023, month: 9,  dir: "below", bold: "RLAIF",             small: "Lee '23-09"),
  (branch: "llmrl", year: 2024, month: 2,  dir: "below", bold: "GRPO",              small: "Shao '24-02"),
  (branch: "llmrl", year: 2024, month: 9,  dir: "above", bold: "o1",                small: "OpenAI '24-09"),
  (branch: "llmrl", year: 2025, month: 1,  dir: "above", bold: "DeepSeek-R1",       small: "'25-01"),
  // Meta-Learning
  (branch: "meta", year: 2016, month: 6,  dir: "below", bold: "Learn to Learn",     small: "Andrychowicz '16-06"),
  (branch: "meta", year: 2016, month: 11, dir: "above", bold: "RL^2",               small: "Duan '16-11"),
  (branch: "meta", year: 2017, month: 3,  dir: "below", bold: "MAML",               small: "Finn '17-03"),
  (branch: "meta", year: 2018, month: 2,  dir: "above", bold: "Evolved Pol. Grad.", small: "Houthooft '18-02"),
  (branch: "meta", year: 2018, month: 3,  dir: "below", bold: "Reptile",            small: "Nichol '18-03"),
  (branch: "meta", year: 2020, month: 7,  dir: "below", bold: "LPG",                small: "Oh '20-07"),
  (branch: "meta", year: 2021, month: 1,  dir: "above", bold: "Evolving RL Alg.",   small: "Co-Reyes '21-01"),
  (branch: "meta", year: 2022, month: 10, dir: "below", bold: "Lu et al.",          small: "Disc. Pol. Opt. '22-10"),
  (branch: "meta", year: 2023, month: 10, dir: "above", bold: "Maheshwari",         small: "GROOVE '23-10"),
  (branch: "meta", year: 2025, month: 12, dir: "below", bold: "DiscoRL",            small: "Oh '25-12 (Nature)"),
  // LLM & Code Gen
  (branch: "code", year: 2017, month: 6,  dir: "above", bold: "Transformer",   small: "Vaswani '17-06"),
  (branch: "code", year: 2019, month: 2,  dir: "below", bold: "GPT-2",         small: "Radford '19-02"),
  (branch: "code", year: 2020, month: 5,  dir: "below", bold: "GPT-3",         small: "Brown '20-05"),
  (branch: "code", year: 2021, month: 7,  dir: "above", bold: "Codex",         small: "Chen '21-07"),
  (branch: "code", year: 2022, month: 2,  dir: "above", bold: "AlphaCode",     small: "Li '22-02"),
  (branch: "code", year: 2022, month: 11, dir: "below", bold: "ChatGPT",       small: "OpenAI '22-11"),
  (branch: "code", year: 2023, month: 2,  dir: "above", bold: "Cursor",        small: "Anysphere '23-02"),
  (branch: "code", year: 2023, month: 3,  dir: "below", bold: "GPT-4",         small: "OpenAI '23-03"),
  (branch: "code", year: 2023, month: 5,  dir: "above", bold: "StarCoder",     small: "BigCode '23-05"),
  (branch: "code", year: 2023, month: 6,  dir: "below", bold: "Aider",         small: "Gauthier '23-06"),
  (branch: "code", year: 2023, month: 8,  dir: "above", bold: "Code Llama",    small: "Rozière '23-08"),
  (branch: "code", year: 2023, month: 10, dir: "below", bold: "SWE-bench",     small: "Jimenez '23-10"),
  (branch: "code", year: 2023, month: 12, dir: "above", bold: "AlphaCode 2",   small: "DeepMind '23-12"),
  (branch: "code", year: 2024, month: 1,  dir: "below", bold: "DeepSeek-Coder", small: "Guo '24-01"),
  (branch: "code", year: 2024, month: 3,  dir: "above", bold: "Devin",         small: "Cognition '24-03"),
  (branch: "code", year: 2024, month: 4,  dir: "below", bold: "SWE-agent",     small: "Yang '24-04"),
  (branch: "code", year: 2024, month: 5,  dir: "above", bold: "OpenHands",     small: "All Hands AI '24-05"),
  (branch: "code", year: 2024, month: 7,  dir: "below", bold: "Cline",         small: "Rizwan '24-07"),
  (branch: "code", year: 2024, month: 9,  dir: "above", bold: "Replit Agent",  small: "Replit '24-09"),
  (branch: "code", year: 2024, month: 11, dir: "above", bold: "Qwen2.5-Coder", small: "Alibaba '24-11"),
  (branch: "code", year: 2024, month: 12, dir: "below", bold: "DeepSeek-V3",   small: "DeepSeek '24-12"),
  (branch: "code", year: 2025, month: 2,  dir: "below", bold: "Claude Code",   small: "Anthropic '25-02"),
  (branch: "code", year: 2025, month: 4,  dir: "below", bold: "Codex CLI",     small: "OpenAI '25-04"),
  (branch: "code", year: 2025, month: 4,  dir: "above", bold: "Gemini 2.5 Pro", small: "Google '25-04"),
  (branch: "code", year: 2025, month: 6,  dir: "above", bold: "Gemini CLI",    small: "Google '25-06"),
  (branch: "code", year: 2025, month: 7,  dir: "below", bold: "Qwen Code",     small: "Alibaba '25-07"),
  (branch: "code", year: 2025, month: 8,  dir: "above", bold: "GPT-5",         small: "OpenAI '25-08"),
  // LLM-Guided Evolution
  (branch: "llme", year: 2022, month: 6,  dir: "below", bold: "ELM",                  small: "Lehman '22-06"),
  (branch: "llme", year: 2023, month: 3,  dir: "above", bold: "Reflexion",            small: "Shinn '23-03"),
  (branch: "llme", year: 2023, month: 5,  dir: "below", bold: "Voyager",              small: "Wang '23-05"),
  (branch: "llme", year: 2023, month: 9,  dir: "above", bold: "PromptBreeder",        small: "Fernando '23-09"),
  (branch: "llme", year: 2023, month: 10, dir: "below", bold: "Eureka",               small: "Ma '23-10"),
  (branch: "llme", year: 2024, month: 1,  dir: "above", bold: "FunSearch",            small: "Romera-P. '24-01"),
  (branch: "llme", year: 2024, month: 6,  dir: "below", bold: "REvolve",              small: "Hazra '24-06"),
  (branch: "llme", year: 2025, month: 4,  dir: "above", bold: "EvoTune",              small: "Surina '25-04"),
  (branch: "llme", year: 2025, month: 6,  dir: "below", bold: "AlphaEvolve",          small: "Novikov '25-06"),
  (branch: "llme", year: 2026, month: 2,  dir: "above", bold: "AlphaEvolve",          small: "MARL '26-02"),
  (branch: "llme", year: 2026, month: 3,  dir: "below", bold: "Evolving RL via LLMs", small: "GECCO '26-03"),
)

// ── cross-branch forks ──────────────────────────────────────────────────
// (from_branch, from_year, from_month) → (to_branch, to_year, to_month)
// Default color = destination branch color.
#let forks = (
  (from: ("ec",   1999, 0),  to: ("neuro", 2002, 0),  annot: [evolve networks]),
  (from: ("rlf",  2002, 0),  to: ("deep",  2015, 2),  annot: [deep function \ approximation]),
  (from: ("code", 2022, 3),  to: ("llme",  2022, 6),  annot: [LLM + evolution]),
  (from: ("deep", 2017, 7),  to: ("llmrl", 2022, 3),  annot: [PPO → RLHF]),
  (from: ("code", 2020, 5),  to: ("llmrl", 2022, 3),  annot: [LLM substrate]),
  (from: ("meta", 2021, 1),  to: ("llme",  2026, 3),  annot: [evolve RL algs.]),
  (from: ("llmrl",2024, 2),  to: ("llme",  2025, 4),  annot: [RL-tuned LLMs]),
  (from: ("neuro",2017, 3),  to: ("deep",  2017, 7),  annot: [ES vs. PG]),
  (from: ("deep", 2016, 2),  to: ("meta",  2016, 11), annot: [deep PG → RL²]),
)

// ── derive year widths + cumulative offsets from item counts ────────────
#let layout = {
  let counts = (:)
  for it in items {
    let k = str(it.year)
    counts.insert(k, counts.at(k, default: 0) + 1)
  }
  let all_years = items.map(x => x.year)
  let min_y = calc.min(..all_years)
  let max_y = calc.max(..all_years)
  let widths  = (:)
  let offsets = (:)
  let cum = 0.0
  for y in range(min_y, max_y + 1) {
    let k = str(y)
    let c = counts.at(k, default: 0)
    let w = year_base_w + c * year_per_item
    widths.insert(k, w)
    offsets.insert(k, cum)
    cum += w
  }
  (
    counts:    counts,
    widths:    widths,
    offsets:   offsets,
    min_year:  min_y,
    max_year:  max_y,
    total_w:   cum,
  )
}

// x for (year, month). month ∈ [0,12] is a linear fraction of year width.
// year > max_year extrapolates using the last year's width (for arrow tails).
#let yx(year, month) = {
  let k = str(year)
  if k in layout.offsets {
    layout.offsets.at(k) + (month / 12.0) * layout.widths.at(k)
  } else if year > layout.max_year {
    let last_k = str(layout.max_year)
    let last_end = layout.offsets.at(last_k) + layout.widths.at(last_k)
    let w = layout.widths.at(last_k)
    last_end + (year - layout.max_year - 1) * w + (month / 12.0) * w
  } else {
    0
  }
}

// per-item x coordinate: spread items evenly within their year, ordered by month
#let item_xs = {
  let by_year = (:)
  for i in range(items.len()) {
    let it = items.at(i)
    let k = str(it.year)
    let arr = by_year.at(k, default: ())
    arr.push((i, it.month))
    by_year.insert(k, arr)
  }
  let ranks = (:)
  for (k, arr) in by_year.pairs() {
    let sorted = arr.sorted(key: p => p.at(1))
    for r in range(sorted.len()) {
      ranks.insert(str(sorted.at(r).at(0)), r)
    }
  }
  let xs = ()
  for i in range(items.len()) {
    let it = items.at(i)
    let k = str(it.year)
    let n = layout.counts.at(k)
    let r = ranks.at(str(i))
    xs.push(layout.offsets.at(k) + (r + 0.5) / n * layout.widths.at(k))
  }
  xs
}

#cetz.canvas(length: 1cm, {
  import cetz.draw: *

  // ── drawing primitives ─────────────────────────────────────────────
  let modeldot(pos, c) = circle(
    pos, radius: 0.09,
    fill: c,
    stroke: (paint: c.darken(50%), thickness: 0.4pt),
  )
  let ml(pos, dir, bold_txt, small_txt) = {
    let anchor = if dir == "above" { "south" } else { "north" }
    let dy     = if dir == "above" { 0.18 }      else { -0.18 }
    content(
      (pos.at(0), pos.at(1) + dy),
      anchor: anchor,
      align(center, par(leading: 0.25em,
        text(size: 7pt, fill: bk70)[
          *#bold_txt* \
          #text(size: 5.5pt)[#small_txt]
        ]
      ))
    )
  }
  let milestone(pos, dir, bold_txt, small_txt, c) = {
    modeldot(pos, c)
    ml(pos, dir, bold_txt, small_txt)
  }
  let branchlabel(pos, c, body) = {
    content(pos, anchor: "east",
      align(right, par(leading: 0.25em,
        text(size: 11pt, weight: "bold", fill: c)[#body])))
  }
  // branch line + label + one of three terminations
  let branch_draw(yv, x_start, x_end, c, label, end_style) = {
    branchlabel((-0.8, yv), c, label)
    let stroke_main = (paint: c, thickness: 2.5pt, cap: "round")
    if end_style == "arrow" {
      line((x_start, yv), (x_end, yv),
        stroke: stroke_main,
        mark: (end: "stealth", fill: c, scale: 1.5))
    } else if end_style == "terminate" {
      line((x_start, yv), (x_end, yv), stroke: stroke_main)
      let r = 0.252
      let xs = (paint: garnet, thickness: 3.36pt, cap: "round")
      line((x_end - r, yv - r), (x_end + r, yv + r), stroke: xs)
      line((x_end - r, yv + r), (x_end + r, yv - r), stroke: xs)
    } else if end_style == "fade" {
      line((x_start, yv), (x_end, yv), stroke: stroke_main)
    }
  }
  let bez(from, to, c, thick: 2pt) = {
    let dx = to.at(0) - from.at(0)
    let c1 = (from.at(0) + dx * 0.5, from.at(1))
    let c2 = (to.at(0) - dx * 0.5, to.at(1))
    bezier(from, to, c1, c2,
      stroke: (paint: c, thickness: thick, cap: "round"))
  }
  let forkannot(pos, c, body) = content(pos,
    box(fill: white, inset: 1pt,
      align(center, text(size: 6pt, style: "italic", fill: c)[#body])))

  // ── year grid: one tick + label per populated year ─────────────────
  for (k, _) in layout.counts.pairs() {
    let x = layout.offsets.at(k)
    line((x, grid_bot), (x, grid_top), stroke: (paint: bk10, thickness: 0.4pt))
    content((x, grid_top + 0.5),
      text(size: 7pt, weight: "bold", fill: bk50)[#k])
  }

  // ── branch lines (extended to cover their items if necessary) ──────
  for (key, b) in branches.pairs() {
    let x1 = yx(b.start.at(0), b.start.at(1))
    let x2 = yx(b.end.at(0), b.end.at(1))
    // extend to cover every item on this branch
    let own_xs = ()
    for i in range(items.len()) {
      if items.at(i).branch == key {
        own_xs.push(item_xs.at(i))
      }
    }
    if own_xs.len() > 0 {
      x1 = calc.min(x1, ..own_xs)
      x2 = calc.max(x2, ..own_xs)
    }
    branch_draw(b.y, x1, x2, b.color, b.label, b.end_style)
  }

  // ── cross-branch forks + annotations ───────────────────────────────
  for f in forks {
    let (fb, fy, fm) = f.from
    let (tb, ty, tm) = f.to
    let from_pt = (yx(fy, fm), branches.at(fb).y)
    let to_pt   = (yx(ty, tm), branches.at(tb).y)
    let c = branches.at(tb).color
    bez(from_pt, to_pt, c)
    let mx = (from_pt.at(0) + to_pt.at(0)) / 2
    let my = (from_pt.at(1) + to_pt.at(1)) / 2 + 0.4
    forkannot((mx, my), c, f.annot)
  }

  // ── milestones ──────────────────────────────────────────────────────
  for i in range(items.len()) {
    let it = items.at(i)
    let b = branches.at(it.branch)
    let x = item_xs.at(i)
    milestone((x, b.y), it.dir, it.bold, it.small, b.color)
  }
})
