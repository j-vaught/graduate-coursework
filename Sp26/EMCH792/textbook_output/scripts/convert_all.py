"""Convert all chapter and appendix PDFs to markdown using marker-pdf 0.2.x."""

import json
import os
import re
import shutil
import subprocess
import sys

BASE = "/Volumes/MacShare/graduate-coursework/Sp26/EMCH792/textbook_output"
STRUCTURE_PATH = os.path.join(BASE, "structure.json")
PDF_DIR = os.path.join(BASE, "pdf")
MD_DIR = os.path.join(BASE, "markdown")
VENV_BIN = os.path.join(BASE, ".venv", "bin")


def run_marker(pdf_path, output_dir):
    """Run marker_single on a PDF and return the markdown file path."""
    os.makedirs(output_dir, exist_ok=True)
    env = os.environ.copy()
    env["HF_HOME"] = os.path.join(BASE, ".hf_cache")
    env["TORCH_HOME"] = os.path.join(BASE, ".torch_cache")
    env["PATH"] = VENV_BIN + ":" + env.get("PATH", "")

    marker_bin = os.path.join(VENV_BIN, "marker_single")
    # marker 0.2.x API: marker_single <input_pdf> <output_dir> --langs English
    cmd = [marker_bin, pdf_path, output_dir, "--langs", "English"]
    print(f"  Running marker on {os.path.basename(pdf_path)}...")
    sys.stdout.flush()
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"  STDERR: {result.stderr[:1000]}", file=sys.stderr)
        sys.stderr.flush()
        return None

    # marker 0.2.x outputs to output_dir/<pdf_stem>/<pdf_stem>.md
    stem = os.path.splitext(os.path.basename(pdf_path))[0]
    md_file = os.path.join(output_dir, stem, stem + ".md")
    if os.path.exists(md_file):
        return md_file

    # Fallback: find any .md file
    for root, dirs, files in os.walk(output_dir):
        for f in files:
            if f.endswith('.md'):
                return os.path.join(root, f)

    print(f"  No markdown output found in {output_dir}")
    print(f"  STDOUT: {result.stdout[:500]}")
    return None


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

        pattern = rf'^#+\s*{escaped_num}\s+'
        match = re.search(pattern, md_content, re.MULTILINE)

        if not match:
            title_words = sec["title"].split()[:3]
            if title_words:
                title_pat = r'[\s_]*'.join(re.escape(w) for w in title_words)
                match = re.search(rf'^#+\s*.*{title_pat}', md_content, re.MULTILINE | re.IGNORECASE)

        if not match:
            continue

        start_pos = match.start()

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

    for ch in structure["chapters"]:
        ch_num = ch["number"]
        pdf_path = os.path.join(PDF_DIR, ch["folder"], f"ch{ch_num:02d}_full.pdf")
        md_out_dir = os.path.join(MD_DIR, ch["folder"])

        full_md_path = os.path.join(md_out_dir, f"ch{ch_num:02d}_full.md")
        if os.path.exists(full_md_path):
            print(f"Chapter {ch_num} already converted, skipping.")
            continue

        print(f"\n=== Converting Chapter {ch_num}: {ch['title']} ===")
        sys.stdout.flush()
        tmp_dir = os.path.join(BASE, f".tmp_marker_ch{ch_num:02d}")
        md_file = run_marker(pdf_path, tmp_dir)

        if md_file:
            with open(md_file, 'r') as f:
                md_content = f.read()
            split_chapter_md(md_content, ch, md_out_dir)
        else:
            print(f"  FAILED: no markdown output for chapter {ch_num}")

        shutil.rmtree(tmp_dir, ignore_errors=True)

    for ap in structure["appendices"]:
        letter = ap["letter"]
        pdf_path = os.path.join(PDF_DIR, f"appendix_{letter.lower()}.pdf")
        md_path = os.path.join(MD_DIR, f"appendix_{letter.lower()}.md")

        if os.path.exists(md_path):
            print(f"Appendix {letter} already converted, skipping.")
            continue

        print(f"\n=== Converting Appendix {letter}: {ap['title']} ===")
        sys.stdout.flush()
        tmp_dir = os.path.join(BASE, f".tmp_marker_app{letter.lower()}")
        md_file = run_marker(pdf_path, tmp_dir)

        if md_file:
            os.makedirs(MD_DIR, exist_ok=True)
            shutil.copy2(md_file, md_path)
            print(f"  Wrote {md_path}")
        else:
            print(f"  FAILED: no markdown output for appendix {letter}")

        shutil.rmtree(tmp_dir, ignore_errors=True)

    print("\n=== All conversions complete ===")
    sys.stdout.flush()


if __name__ == '__main__':
    main()
