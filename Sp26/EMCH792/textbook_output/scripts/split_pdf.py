"""Split the textbook PDF into per-chapter and per-section PDFs."""

import json
import os
import fitz

PDF_PATH = "/Volumes/MacShare/graduate-coursework/Sp26/EMCH792/Optimal State Estimation textbook.pdf"
STRUCTURE_PATH = "/Volumes/MacShare/graduate-coursework/Sp26/EMCH792/textbook_output/structure.json"
PDF_OUT = "/Volumes/MacShare/graduate-coursework/Sp26/EMCH792/textbook_output/pdf"


def extract_pages(doc, start, end, output_path):
    """Extract pages [start, end] (0-indexed) to a new PDF."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    new_doc = fitz.open()
    new_doc.insert_pdf(doc, from_page=start, to_page=end)
    new_doc.save(output_path)
    new_doc.close()
    print(f"  -> {output_path} ({end - start + 1} pages)")


def main():
    with open(STRUCTURE_PATH) as f:
        structure = json.load(f)

    doc = fitz.open(PDF_PATH)

    # Front matter
    fm = structure.get("front_matter")
    if fm and fm["start"] is not None:
        extract_pages(doc, fm["start"], fm["end"], os.path.join(PDF_OUT, "00_front_matter.pdf"))

    # Chapters
    for ch in structure["chapters"]:
        folder = os.path.join(PDF_OUT, ch["folder"])
        # Full chapter
        extract_pages(doc, ch["start"], ch["end"],
                       os.path.join(folder, f"ch{ch['number']:02d}_full.pdf"))
        # Sections
        for sec in ch["sections"]:
            sec_num = sec["number"].replace(".", "_")
            fname = f"s{sec['number']}_{sec['slug']}.pdf"
            extract_pages(doc, sec["start"], sec["end"],
                           os.path.join(folder, fname))

    # Appendices
    for ap in structure["appendices"]:
        extract_pages(doc, ap["start"], ap["end"],
                       os.path.join(PDF_OUT, f"appendix_{ap['letter'].lower()}.pdf"))

    # Back matter
    bm = structure.get("back_matter")
    if bm:
        extract_pages(doc, bm["start"], bm["end"],
                       os.path.join(PDF_OUT, "back_matter.pdf"))

    doc.close()
    print("Done splitting PDF.")


if __name__ == '__main__':
    main()
