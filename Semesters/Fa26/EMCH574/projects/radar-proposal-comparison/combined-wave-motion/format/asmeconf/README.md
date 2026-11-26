# ASME conference LaTeX files

This directory contains the `asmeconf` LaTeX class and bibliography style from CTAN, version 1.47 dated 2026-10-31. The class is the LaTeX template linked from ASME's conference author-template page. It is maintained by John H. Lienhard and is not itself an ASME publication. Copyright and licensing notices are retained in both source files.

Sources:

- https://ctan.org/pkg/asmeconf
- https://mirrors.ctan.org/macros/latex/contrib/asmeconf/asmeconf.cls
- https://mirrors.ctan.org/macros/latex/contrib/asmeconf/asmeconf.bst

ASME's current conference-specific header and sample paper are published at https://idetc.secure-platform.com/a/page/Help/author_resources/conference-specific-templates. The governing layout requirements are at https://www.asme.org/publications-submissions/proceedings/formatting-the-paper. ASME lists `asmeconf` as its courtesy LaTeX template at https://www.asme.org/publications-submissions/proceedings/author-guidelines/elements-of-a-paper/author-templates.

Use `\\documentclass{asmeconf}` and `\\bibliographystyle{asmeconf}`. The class supplies the conference page layout, two-column body, margins, and the Times-like and Arial-like font families used by the author template. It loads the mathematics and citation support. Add only project-specific packages such as `graphicx` and `booktabs`; leave the class's column and spacing settings at their defaults.

For IDETC-CIE 2027, use the conference-specific header `Proceedings of the ASME 2027 International Design Engineering Technical Conferences and Computers and Information in Engineering Conference`, `IDETC/CIE2027`, `August 1--4, 2027`, and `Philadelphia, PA`. Keep `\\PaperNo{}` empty until ASME assigns a number; do not use a made-up number or placeholder. The class option `nofoot` keeps the page number while suppressing the ASME copyright footer in a review draft. Remove `nofoot` only when preparing the publication version under ASME's final instructions.

On a configured COMECH or COCESR host, build with `./build-manuscript.sh`. The script places compiled output in `build/asme/` and uses the class and bibliography files in this directory.

The class requires a current, complete TeX installation. Figure generation, simulation, and PDF compilation for this project are run on the configured COMECH or COCESR hosts.
