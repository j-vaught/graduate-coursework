"""Convert a single chapter PDF to markdown using marker-pdf, then split into sections."""

import argparse
import json
import os
import re
import subprocess
import shutil


BASE = "/Volumes/MacShare/graduate-coursework/Sp26/EMCH792/textbook_output"
STRUCTURE_PATH = os.path.join(BASE, "structure.json")
PDF_DIR = os.path.join(BASE, "pdf")
MD_DIR = os.path.join(BASE, "markdown")


def run_marker(pdf_path, output_dir):
    """Run marker on a PDF and return the markdown content."""
    os.makedirs(output_dir, exist_ok=True)
    # marker outputs to a directory named after the PDF
    cmd = [
        "marker_single", pdf_path, output_dir,
        "--langs", "English",
    ]
    env = os.environ.copy()
    env["HF_HOME"] = os.path.join(BASE, ".hf_cache")
    env["TORCH_HOME"] = os.path.join(BASE, ".torch_cache")
    subprocess.run(cmd, check=True, env=env)

    # marker creates a subdirectory with the PDF stem name
    stem = os.path.splitext(os.path.basename(pdf_path))[0]
    md_file = os.path.join(output_dir, stem, stem + ".md")
    if not os.path.exists(md_file):
        # Try finding any .md file in output
        for root, dirs, files in os.walk(output_dir):
            for f in files:
                if f.endswith('.md'):
                    md_file = os.path.join(root, f)
                    break

    with open(md_file, 'r') as f:
        return f.read()


def split_chapter_md(md_content, chapter_info, output_dir):
    """Split a full chapter markdown into per-section files."""
    os.makedirs(output_dir, exist_ok=True)

    # Write full chapter
    ch_num = chapter_info["number"]
    full_path = os.path.join(output_dir, f"ch{ch_num:02d}_full.md")
    with open(full_path, 'w') as f:
        f.write(md_content)

    # Split by section headers
    sections = chapter_info.get("sections", [])
    if not sections:
        return

    # Try to find section boundaries in the markdown
    for i, sec in enumerate(sections):
        sec_num = sec["number"]
        sec_title = sec["title"]
        # Build regex to find section header
        # Match patterns like "## 1.1 Matrix Algebra" or "# 1.1 Matrix Algebra"
        escaped_num = re.escape(sec_num)
        pattern = rf'^#+\s*{escaped_num}\s+'

        # Find start position
        match = re.search(pattern, md_content, re.MULTILINE)
        if not match:
            # Try without markdown heading markers
            pattern2 = rf'^{escaped_num}\s+{re.escape(sec_title[:20])}'
            match = re.search(pattern2, md_content, re.MULTILINE | re.IGNORECASE)

        if match:
            start_pos = match.start()
        else:
            continue

        # Find end: start of next section or end of content
        if i + 1 < len(sections):
            next_num = sections[i + 1]["number"]
            escaped_next = re.escape(next_num)
            next_pattern = rf'^#+\s*{escaped_next}\s+'
            next_match = re.search(next_pattern, md_content[start_pos + 1:], re.MULTILINE)
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


def convert_appendix(pdf_path, letter, output_dir):
    """Convert an appendix PDF to markdown."""
    os.makedirs(output_dir, exist_ok=True)
    tmp_dir = os.path.join(BASE, ".tmp_marker")
    md_content = run_marker(pdf_path, tmp_dir)
    out_path = os.path.join(output_dir, f"appendix_{letter.lower()}.md")
    with open(out_path, 'w') as f:
        f.write(md_content)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    return out_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", type=int, help="Chapter number to convert")
    parser.add_argument("--appendix", type=str, help="Appendix letter to convert")
    args = parser.parse_args()

    with open(STRUCTURE_PATH) as f:
        structure = json.load(f)

    if args.chapter:
        ch = next(c for c in structure["chapters"] if c["number"] == args.chapter)
        pdf_path = os.path.join(PDF_DIR, ch["folder"], f"ch{ch['number']:02d}_full.pdf")
        tmp_dir = os.path.join(BASE, f".tmp_marker_ch{ch['number']:02d}")

        print(f"Converting Chapter {ch['number']}: {ch['title']}")
        md_content = run_marker(pdf_path, tmp_dir)

        md_out = os.path.join(MD_DIR, ch["folder"])
        split_chapter_md(md_content, ch, md_out)

        shutil.rmtree(tmp_dir, ignore_errors=True)
        print(f"Done: Chapter {ch['number']}")

    elif args.appendix:
        letter = args.appendix.upper()
        ap = next(a for a in structure["appendices"] if a["letter"] == letter)
        pdf_path = os.path.join(PDF_DIR, f"appendix_{letter.lower()}.pdf")

        print(f"Converting Appendix {letter}: {ap['title']}")
        convert_appendix(pdf_path, letter, MD_DIR)
        print(f"Done: Appendix {letter}")


if __name__ == '__main__':
    main()
