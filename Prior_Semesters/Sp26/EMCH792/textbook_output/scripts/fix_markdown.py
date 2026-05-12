"""Post-process markdown files: add YAML front matter and clean up artifacts."""

import json
import os
import re
import glob

BASE = "/Volumes/MacShare/graduate-coursework/Sp26/EMCH792/textbook_output"
STRUCTURE_PATH = os.path.join(BASE, "structure.json")
MD_DIR = os.path.join(BASE, "markdown")


def add_front_matter(filepath, metadata):
    """Prepend YAML front matter to a markdown file."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Skip if already has front matter
    if content.startswith('---'):
        return

    yaml_lines = ['---']
    for k, v in metadata.items():
        if isinstance(v, str) and (':' in v or '"' in v):
            yaml_lines.append(f'{k}: "{v}"')
        else:
            yaml_lines.append(f'{k}: {v}')
    yaml_lines.append('---')
    yaml_lines.append('')

    with open(filepath, 'w') as f:
        f.write('\n'.join(yaml_lines) + content)


def cleanup_content(filepath):
    """Clean up common marker artifacts."""
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # Fix double-escaped LaTeX
    content = content.replace('\\\\(', '\\(').replace('\\\\)', '\\)')
    content = content.replace('\\\\[', '\\[').replace('\\\\]', '\\]')

    # Remove excessive blank lines (more than 2 consecutive)
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    # Fix common OCR artifacts
    content = content.replace('ﬁ', 'fi').replace('ﬂ', 'fl')

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)


def main():
    with open(STRUCTURE_PATH) as f:
        structure = json.load(f)

    count = 0

    # Process chapters
    for ch in structure["chapters"]:
        ch_dir = os.path.join(MD_DIR, ch["folder"])
        if not os.path.isdir(ch_dir):
            continue

        # Full chapter file
        full_md = os.path.join(ch_dir, f"ch{ch['number']:02d}_full.md")
        if os.path.exists(full_md):
            cleanup_content(full_md)
            add_front_matter(full_md, {
                "type": "chapter",
                "chapter": ch["number"],
                "title": ch["title"],
            })
            count += 1

        # Section files
        for sec in ch["sections"]:
            sec_md = os.path.join(ch_dir, f"s{sec['number']}_{sec['slug']}.md")
            if os.path.exists(sec_md):
                cleanup_content(sec_md)
                add_front_matter(sec_md, {
                    "type": "section",
                    "chapter": ch["number"],
                    "section": sec["number"],
                    "title": sec["title"],
                })
                count += 1

    # Process appendices
    for ap in structure["appendices"]:
        ap_md = os.path.join(MD_DIR, f"appendix_{ap['letter'].lower()}.md")
        if os.path.exists(ap_md):
            cleanup_content(ap_md)
            add_front_matter(ap_md, {
                "type": "appendix",
                "letter": ap["letter"],
                "title": ap["title"],
            })
            count += 1

    print(f"Post-processed {count} markdown files.")


if __name__ == '__main__':
    main()
