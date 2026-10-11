# Simulator report production contract

Write an engineering report grounded in the current `blueboat_sim/` implementation. Use `J.C. Vaught` as author. Never claim a supplied controller, estimator, image renderer, processor emulator, field validation, or features absent from code. Do not mention prohibited assistant/provider names. Do not modify simulator code, existing report, bibliography, shared style, or other agents' files. Do not commit independently. All agents share the checkout; do not revert others' edits.

## Writing

Use Typst chapter files with one level-1 chapter heading and useful level-2 subsections. Start each subsection with a short connecting paragraph and use nested bullets up to three levels to explain purpose, mechanism, and practical consequences. Include equations with defined variables and units. Do not use colons before explanatory prose. Keep captions one sentence. Distinguish manufacturer values, configuration choices, numerical approximations, and engineering assumptions. No repetitive disclaimers. Write concrete worked examples and interpretation, not only a list of features. Target roughly 3 useful pages per small chapter, allowing 4 when needed.

## Figure language

Use the NEW `simulator_report/style.typ`, not previous coursework/house style files. All figures are authored in Typst with CeTZ 0.4.2 or Lilaq 0.6.0. Data may be generated in Python and retained under `simulator_report/data/`. No matplotlib, TikZ, raster drawing, or image generation. Square corners, high contrast, filled stealth arrows. White background. Diagram process nodes use navy/teal ink and pale teal fill; unimplemented boundaries use neutral dashed strokes with explicit labels. Ground-truth and measured/controller information paths must be distinct. Graphs use standard plotting colors and line patterns with explicit units. Legends are square. Font Times New Roman, body 10.5 pt, figure text 9 pt. Keep a full-width diagram under 16 cm. For CeTZ canvases use length 0.8cm, content no smaller than 8.5 pt, and explicit line breaks. Do not route connectors through labels. Label what arrows carry.

## Shared APIs

Import `../style.typ` from chapter files and figure files (both reside one level below it). Exports are `cetz`, `lq`, `ink`, `teal`, `pale`, `slate`, `ochre`, `arrow`, `node`, `plot-panel`, `data-table`, `note`, `line-colors`. `plot-panel` takes title, xlabel, ylabel, and an array of dictionaries `(x: array, y: array, label: content)`; optional dictionary `dash`. Named options xlim, ylim, height, width. Figure modules export named functions; chapters import them from `../figures/NAME.typ`. Chapters are included by the root report, so do not set global page/text settings or bibliography. Labels must be unique with your chapter prefix. Cite existing keys from `../../references.bib` when relevant. Do not create external citations for claims already established by the implementation. Root assembler manages bibliography.

Each figure can be previewed with a temporary wrapper in project `build/` and `typst compile --root . build/WRAPPER.typ build/WRAPPER.pdf`. Only the root will deliver the combined PDF. Report files remain editable and reproducible.
