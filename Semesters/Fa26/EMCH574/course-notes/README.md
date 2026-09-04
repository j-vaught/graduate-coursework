# EMCH 574 typed course notes

This directory is the working area for converting the 265-page EMCH 574 course-notes PDF into a fully typed LaTeX document. The source of record remains [`../lectures/EMCH574_CourseNotes_20260826.pdf`](../lectures/EMCH574_CourseNotes_20260826.pdf). It must not be edited or replaced during the conversion.

All prose, headings, equations, tables, definitions, examples, and figure labels in the finished notes will be native LaTeX. Figures will be recreated with the existing Typst, CeTZ, and Lilaq system whenever the recreation is faithful and visually polished. A tightly cropped image from the original notes may be used when a recreation cannot confidently meet that standard. Page screenshots containing prose or equations are not acceptable substitutes for typed content.

The visual identity will retain the current deep-teal and garnet-rose scheme from the EMCH 574 figure library. The canonical colors are deep teal `#005F73` and garnet rose `#8B3A4A`. New Typst figures will import the existing public facade at [`../homework/typst-figures/styles/figure.typ`](../homework/typst-figures/styles/figure.typ) so typography, dimensions, line weights, arrows, mechanics components, control-diagram styles, and plot themes remain consistent.

The full workflow and acceptance criteria are recorded in [`CONVERSION_PLAN.md`](CONVERSION_PLAN.md). No course content has been converted yet.

## Directory roles

The `inventory` directory will hold the page-by-page source map and chapter crosswalk. The `latex` directory will hold the document entry point, preamble, and typed chapter sources. The `figures/typst` directory will hold authored Typst sources, while `figures/generated` will hold their compiled PDF or PNG assets. The `figures/original-crops` directory is reserved for approved figure-only crops from the source PDF. The `references` directory will hold the centralized `references.bib` file. The `qa` directory will hold conversion checklists, comparison records, and rendered review material that should remain under version control.
