# EMCH 574 course instructions

These instructions apply to EMCH 574 coursework in this directory. The established HW01 design controls this class's documents and figures. Its course palette overrides the general workspace plotting theme.

Use `homework/emch574-homework.sty` for homework documents and keep the HW01 title, headers, problem numbering, equations, tables, and MATLAB listing style. The document uses teal `#006D75` for headings, math, and links; charcoal `#363636` for dark neutral text; light gray `#ECECEC` for code backgrounds; and orange `#C65D00` for code strings.

Use the homework figure palette defined in `homework/typst-figures/styles/colors.typ`. Its primary plotted curve is teal `#005F73`, its second curve is orange `#D55E00`, and its dark curve is graphite `#25282A`. Keep a white background, readable gray guides, square edges, and strong contrast. MATLAB plots use the matching values in `homework/HW01/matlab/hw01_settings.m`. Do not substitute the general garnet plotting palette for this class.

Preserve an assignment's original problem images and include each supplied image beside its problem statement. Do not redraw, recolor, crop, or otherwise alter a problem image unless the image is incorrect for that problem. For HW02, use the image files extracted directly from the supplied DOCX; orient the two photographs in LaTeX while keeping their bytes unchanged. The user will decide when to convert those images later.

When a new analytical figure is needed, follow HW01's Typst, CeTZ, and Lilaq sources, the shared figure styles, and `PALETTE=homework`. Store editable figure sources in the homework's `figures/src/` and compiled PDFs in `figures/generated/`. MATLAB may make its interactive plots directly using the same palette. Keep figure labels, axes, units, event markers, and captions consistent with HW01.

Check each problem statement against the supplied assignment before changing a value, and preserve the original assignment file separately. Rebuild the PDF and inspect rendered pages after edits. Leave unrelated coursework and existing figures unchanged.
