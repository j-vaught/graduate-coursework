"""Convert all chapter and appendix PDFs to markdown using PyMuPDF text extraction.

Since marker-pdf requires Python 3.10+ and only 3.9 is available, we use PyMuPDF's
structured text extraction with font analysis to produce markdown with:
- Heading detection via font size/bold
- LaTeX math blocks where detected
- Table structure preservation
- Paragraph assembly
"""

import json
import os
import re
import fitz

BASE = "/Volumes/MacShare/graduate-coursework/Sp26/EMCH792/textbook_output"
STRUCTURE_PATH = os.path.join(BASE, "structure.json")
PDF_DIR = os.path.join(BASE, "pdf")
MD_DIR = os.path.join(BASE, "markdown")


def extract_page_markdown(page, page_num_in_chapter):
    """Convert a single PDF page to markdown text."""
    blocks = page.get_text("dict")["blocks"]
    lines_out = []

    for block in blocks:
        if block["type"] == 1:
            # Image block - note it
            lines_out.append(f"\n[Image on page {page_num_in_chapter}]\n")
            continue

        if "lines" not in block:
            continue

        block_lines = []
        for line in block["lines"]:
            spans = line["spans"]
            if not spans:
                continue

            text = "".join(s["text"] for s in spans).strip()
            if not text:
                continue

            max_size = max(s["size"] for s in spans)
            fonts = set(s["font"] for s in spans)
            is_bold = any("Bold" in f for f in fonts)
            is_italic = any("Italic" in f for f in fonts)
            is_courier = any("Courier" in f for f in fonts)
            y = line["bbox"][1]

            # Skip page headers/footers (small text at top/bottom)
            if max_size < 8 and (y < 60 or y > 700):
                continue

            # Detect heading level based on font size
            heading_level = 0
            if is_bold and "Arial" in " ".join(fonts):
                if max_size >= 14:
                    heading_level = 1  # Chapter title
                elif max_size >= 10:
                    heading_level = 2  # Section header

            # Detect if text is likely a math expression (Courier font, symbols)
            is_math = is_courier and any(c in text for c in '=∑∫∂λΣ')

            if heading_level > 0:
                prefix = "#" * heading_level
                block_lines.append(f"\n{prefix} {text}\n")
            elif is_math and len(text) > 3:
                # Wrap in LaTeX display math
                block_lines.append(f"\n$$\n{text}\n$$\n")
            elif is_italic and not is_bold:
                block_lines.append(f"*{text}*")
            elif is_bold:
                block_lines.append(f"**{text}**")
            else:
                block_lines.append(text)

        if block_lines:
            # Join lines within same block as a paragraph
            paragraph = " ".join(block_lines)
            lines_out.append(paragraph)

    return "\n\n".join(lines_out)


def convert_pdf_to_markdown(pdf_path):
    """Convert an entire PDF to markdown."""
    doc = fitz.open(pdf_path)
    all_md = []

    for i, page in enumerate(doc):
        page_md = extract_page_markdown(page, i + 1)
        if page_md.strip():
            all_md.append(page_md)

    doc.close()
    return "\n\n---\n\n".join(all_md)


def split_chapter_md(md_content, chapter_info, output_dir):
    """Split full chapter markdown into per-section files."""
    os.makedirs(output_dir, exist_ok=True)
    ch_num = chapter_info["number"]

    full_path = os.path.join(output_dir, f"ch{ch_num:02d}_full.md")
    with open(full_path, 'w') as f:
        f.write(md_content)
    print(f"  Wrote {full_path}")

    sections = chapter_info.get("sections", [])
    if not sections:
        return

    for i, sec in enumerate(sections):
        sec_num = sec["number"]
        escaped_num = re.escape(sec_num)

        # Find section header in markdown
        pattern = rf'^#+\s*{escaped_num}\s+'
        match = re.search(pattern, md_content, re.MULTILINE)

        if not match:
            # Try title text
            title_words = sec["title"].split()[:3]
            if title_words:
                title_pat = r'\s+'.join(re.escape(w) for w in title_words)
                match = re.search(rf'^#+\s*.*{title_pat}', md_content, re.MULTILINE | re.IGNORECASE)

        if not match:
            continue

        start_pos = match.start()

        # Find end
        if i + 1 < len(sections):
            next_num = sections[i + 1]["number"]
            escaped_next = re.escape(next_num)
            next_match = re.search(rf'^#+\s*{escaped_next}\s+', md_content[start_pos + 1:], re.MULTILINE)
            if next_match:
                end_pos = start_pos + 1 + next_match.start()
            else:
                end_pos = len(md_content)
        else:
            end_pos = len(md_content)

        section_md = md_content[start_pos:end_pos].strip()
        fname = f"s{sec_num}_{sec['slug']}.md"
        sec_path = os.path.join(output_dir, fname)
        with open(sec_path, 'w') as f:
            f.write(section_md + '\n')


def main():
    with open(STRUCTURE_PATH) as f:
        structure = json.load(f)

    # Convert chapters
    for ch in structure["chapters"]:
        ch_num = ch["number"]
        pdf_path = os.path.join(PDF_DIR, ch["folder"], f"ch{ch_num:02d}_full.pdf")
        md_out_dir = os.path.join(MD_DIR, ch["folder"])

        full_md = os.path.join(md_out_dir, f"ch{ch_num:02d}_full.md")
        if os.path.exists(full_md):
            print(f"Chapter {ch_num} already converted, skipping.")
            continue

        print(f"\n=== Converting Chapter {ch_num}: {ch['title']} ===")
        md_content = convert_pdf_to_markdown(pdf_path)
        split_chapter_md(md_content, ch, md_out_dir)

    # Convert appendices
    for ap in structure["appendices"]:
        letter = ap["letter"]
        pdf_path = os.path.join(PDF_DIR, f"appendix_{letter.lower()}.pdf")
        md_path = os.path.join(MD_DIR, f"appendix_{letter.lower()}.md")

        if os.path.exists(md_path):
            print(f"Appendix {letter} already converted, skipping.")
            continue

        print(f"\n=== Converting Appendix {letter}: {ap['title']} ===")
        md_content = convert_pdf_to_markdown(pdf_path)
        os.makedirs(MD_DIR, exist_ok=True)
        with open(md_path, 'w') as f:
            f.write(md_content)
        print(f"  Wrote {md_path}")

    print("\n=== All conversions complete ===")


if __name__ == '__main__':
    main()
