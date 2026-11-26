# ASME conference LaTeX files

This directory contains the `asmeconf` LaTeX class and bibliography style from CTAN, version 1.47 dated 2026-10-31. The class is the LaTeX template linked from ASME's conference author-template page. It is maintained by John H. Lienhard and is not itself an ASME publication. Copyright and licensing notices are retained in both source files.

Sources:

- https://ctan.org/pkg/asmeconf
- https://mirrors.ctan.org/macros/latex/contrib/asmeconf/asmeconf.cls
- https://mirrors.ctan.org/macros/latex/contrib/asmeconf/asmeconf.bst

Use `\\documentclass{asmeconf}` and `\\bibliographystyle{asmeconf}`. The class sets ASME conference layout, fonts, and heading styles. It loads the mathematics and citation support. Add only project-specific packages such as `graphicx` and `booktabs`.

For IDETC-CIE 2027, use the conference-specific header `Proceedings of the ASME 2027 International Design Engineering Technical Conferences and Computers and Information in Engineering Conference`, `IDETC/CIE2027`, `August 1--4, 2027`, and `Philadelphia, PA`. Keep `\\PaperNo{}` empty until ASME assigns a number; do not use a made-up number or a placeholder in a circulated draft. Use the class option `nofoot` for drafts so the PDF does not imply that ASME has accepted or copyrighted the paper. Confirm the portal's current conference header before final submission.

On a configured COMECH or COCESR host, build with `./build-manuscript.sh`. The script places compiled output in `build/asme/` and uses the class and bibliography files in this directory.

The class requires a current, complete TeX installation. Figure generation, simulation, and PDF compilation for this project are run on the configured COMECH or COCESR hosts.
