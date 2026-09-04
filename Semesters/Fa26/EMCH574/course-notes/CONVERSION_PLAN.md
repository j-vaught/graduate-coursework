# EMCH 574 course-notes conversion plan

## Goal and source policy

The goal is a polished, searchable, fully typed LaTeX edition of the EMCH 574 course notes. The original 265-page PDF is the source of record. Its printed page numbering, visual sequence, terminology, notation, examples, and figure relationships will be preserved even when its embedded text extraction is incomplete or inaccurate.

Typed content includes prose, headings, equations, derivations, definitions, lists, tables, captions, labels, and annotations that carry technical meaning. The only content permitted to remain rasterized is figure artwork that has been isolated from surrounding text. Any equations or explanatory text embedded in an accepted crop should be retyped as LaTeX whenever practical and placed as an overlay, caption, or adjacent explanation.

## Visual system

The notes will retain the existing figure system's deep teal `#005F73` and garnet rose `#8B3A4A` as the primary accent colors. Black, white, graphite, and restrained grey tones will support high contrast. Graphical elements will use square or mitered geometry rather than rounded panels. Document-level LaTeX colors will be defined once and matched numerically to the Typst palette.

All newly authored figures will use Typst. CeTZ 0.5.2 will handle engineering diagrams and mechanical schematics. Lilaq 0.6.0 will handle quantitative plots. Tiptoe 0.4.0 will supply compatible arrowheads. Figure sources will import the shared `figure.typ` facade from the existing EMCH 574 figure workshop rather than duplicating its styles.

## Inventory before transcription

The first conversion activity will be a page-by-page inventory. Each source page will receive a stable identifier, its visible page number, a provisional chapter or topic, its content type, its figure count, and a legibility assessment. The inventory will distinguish born-digital text, handwritten material, equations, tables, diagrams, plots, and decorative or repeated elements.

Chapter boundaries will be established from visual review rather than inferred solely from extracted text. A crosswalk will map every source page to exactly one LaTeX chapter file or to an explicitly documented front-matter or blank-page disposition. This crosswalk will be the completeness ledger for the project.

## LaTeX architecture

The document will use one root `main.tex` file, one shared preamble, and one chapter file per major topic. Reusable theorem-like environments, notation commands, units, vectors, matrices, derivatives, and vibration-specific symbols will be centralized instead of redefined chapter by chapter. Bibliographic data will be stored in `references/references.bib` using the required `LastName2024Topic` key convention.

The source will favor semantic LaTeX. Equations will use aligned mathematical environments, tables will use proper tabular structures, and definitions and examples will use named environments. Manual spacing and page-breaking commands will be limited to cases confirmed by rendered review. Source-page references will be retained in comments or the inventory rather than displayed in the finished notes unless they are pedagogically useful.

## Figure decision process

Each figure will first be classified as a quantitative plot, mechanical schematic, control-system diagram, general illustration, or source-only image. Quantitative plots and standard engineering schematics should normally be recreated in Typst by adapting the existing `ch01`, `ch02`, specimen, and homework examples.

A Typst recreation will be accepted only when its topology, geometry, plotted data, labels, units, arrows, sign conventions, relative positions, and pedagogical emphasis agree with the source. It must also remain legible at the final insertion size and fit the shared teal and garnet-rose visual language.

If the source geometry or data cannot be recovered confidently, the original figure will be cropped at sufficient resolution and retained as an image. The crop must exclude page text, handwritten derivations, headers, footers, and page numbers. Its caption and technical labels will be typed outside the image where feasible. This fallback is a deliberate quality decision, not a shortcut.

## Conversion sequence

Work will proceed by chapter-sized batches. A batch begins with the relevant inventory rows and low-resolution review renders. The text and mathematics are then transcribed into the chapter file. Figures are recreated or cropped under the decision process above. The batch is compiled, compared page by page with the source, corrected, and marked complete only after the crosswalk shows that every source element has a disposition.

The initial pass will prioritize semantic accuracy and completeness. A second pass will standardize notation, terminology, headings, captions, cross-references, and bibliography entries. A final design pass will tune page flow, whitespace, float placement, line breaks, and figure sizing without changing technical meaning.

## Quality assurance

Every chapter will receive both a content review and a visual review. Content review will check equations term by term, signs, subscripts, superscripts, vector notation, units, initial conditions, boundary conditions, and references between equations and figures. Visual review will compare rendered LaTeX pages with the original pages and inspect legibility, alignment, clipping, float placement, and figure scale.

The full document will be compiled from a clean checkout. The final PDF must have no missing references, undefined citations, overfull content that affects readability, rasterized body text, cropped labels, broken glyphs, or inconsistent page furniture. Search and copy tests will confirm that all nonfigure content is selectable text. A final inventory audit will require every one of the 265 source pages to be accounted for.

## Version-control checkpoints

The scaffold and plan form the first checkpoint. Later checkpoints should correspond to the completed inventory, the LaTeX document shell, each converted chapter batch, the notation and reference normalization pass, and final quality assurance. Generated course-note PDFs and approved figure outputs may be committed because they are deliverables, while temporary renderings and compilation intermediates should remain untracked.

## Current status

The workspace structure and conversion plan are established. No transcription, equation conversion, figure recreation, figure cropping, or LaTeX document construction has begun.
