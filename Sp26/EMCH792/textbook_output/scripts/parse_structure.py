"""Parse the textbook PDF TOC and section headers to build structure.json."""

import json
import re
import fitz

PDF_PATH = "/Volumes/MacShare/graduate-coursework/Sp26/EMCH792/Optimal State Estimation textbook.pdf"
OUTPUT_PATH = "/Volumes/MacShare/graduate-coursework/Sp26/EMCH792/textbook_output/structure.json"


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')


def find_sections_in_pages(doc, ch_num, start_pg, end_pg):
    """Scan pages for section headers. Handles both single-line and split headers."""
    sections = []
    num_pattern = re.compile(rf'^{ch_num}\.(\d+)$')
    combined_pattern = re.compile(rf'^{ch_num}\.(\d+)\s+(.+)')

    for pg_idx in range(start_pg, end_pg + 1):
        page = doc[pg_idx]
        blocks = page.get_text("dict")["blocks"]

        # Collect all Arial-Bold text spans with their y-positions
        bold_items = []  # (y, x, text)
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                spans = line["spans"]
                if not spans:
                    continue
                is_arial_bold = any("Arial" in s["font"] and "Bold" in s["font"] for s in spans)
                if not is_arial_bold:
                    continue
                text = "".join(s["text"] for s in spans).strip()
                if not text:
                    continue
                y = round(line["bbox"][1], 0)
                x = line["bbox"][0]
                size = max(s["size"] for s in spans)
                # Only consider text with size >= 9 (skip page headers which are ~6-7)
                if size >= 9:
                    bold_items.append((y, x, text, size))

        # Group by y-coordinate (same line, tolerance ±3px)
        by_y = {}
        for y, x, text, size in bold_items:
            matched_y = None
            for existing_y in by_y:
                if abs(y - existing_y) <= 3:
                    matched_y = existing_y
                    break
            if matched_y is not None:
                by_y[matched_y].append((x, text, size))
            else:
                by_y[y] = [(x, text, size)]

        for y in sorted(by_y.keys()):
            items = sorted(by_y[y], key=lambda t: t[0])  # sort by x
            combined_text = " ".join(t[1] for t in items)

            # Try combined match: "1.2 LINEAR SYSTEMS"
            m = combined_pattern.match(combined_text)
            if m:
                sec_num = f"{ch_num}.{m.group(1)}"
                sec_title = m.group(2).strip()
                # Filter out subsection numbers (e.g. 1.1.1)
                if re.match(r'^\d+\.\d+\.\d+', combined_text):
                    continue
                # Filter out exercise problems (title starts lowercase or is a sentence)
                first_word = sec_title.split()[0] if sec_title else ""
                if first_word and first_word[0].islower():
                    continue
                if len(sec_title) > 80:
                    continue
                # Filter exercise problems (title is a sentence starting with a verb)
                exercise_starts = ['Consider', 'Show', 'Find', 'Prove', 'Solve',
                                   'Derive', 'Verify', 'Compute', 'Calculate', 'Let',
                                   'Suppose', 'Given', 'Use', 'Write', 'Determine']
                if first_word in exercise_starts:
                    continue
                sections.append({
                    "number": sec_num,
                    "title": sec_title,
                    "slug": slugify(sec_title),
                    "start": pg_idx,
                    "end": None,
                })
                continue

            # Try standalone number with title on same y
            if len(items) >= 2:
                first_text = items[0][1]
                m2 = num_pattern.match(first_text)
                if m2:
                    title_text = " ".join(t[1] for t in items[1:]).strip()
                    if not title_text or re.match(r'^\d', title_text):
                        continue
                    first_word = title_text.split()[0] if title_text else ""
                    if first_word and first_word[0].islower():
                        continue
                    if len(title_text) > 80:
                        continue
                    exercise_starts = ['Consider', 'Show', 'Find', 'Prove', 'Solve',
                                       'Derive', 'Verify', 'Compute', 'Calculate', 'Let',
                                       'Suppose', 'Given', 'Use', 'Write', 'Determine']
                    if first_word in exercise_starts:
                        continue
                    sec_num = f"{ch_num}.{m2.group(1)}"
                    sections.append({
                        "number": sec_num,
                        "title": title_text,
                        "slug": slugify(title_text),
                        "start": pg_idx,
                        "end": None,
                    })

    # Deduplicate by section number
    seen = set()
    unique = []
    for sec in sections:
        if sec["number"] not in seen:
            seen.add(sec["number"])
            unique.append(sec)
    sections = unique

    # Fill end pages
    for j, sec in enumerate(sections):
        if j + 1 < len(sections):
            sec["end"] = sections[j + 1]["start"] - 1
        else:
            sec["end"] = end_pg
    for sec in sections:
        if sec["end"] < sec["start"]:
            sec["end"] = sec["start"]

    return sections


def main():
    doc = fitz.open(PDF_PATH)
    total_pages = len(doc)
    print(f"Opened PDF: {total_pages} pages")

    toc = doc.get_toc()

    structure = {
        "total_pages": total_pages,
        "front_matter": None,
        "chapters": [],
        "appendices": [],
        "back_matter": None,
    }

    chapters_raw = []
    for level, title, page in toc:
        pg = page - 1
        if level == 2 and pg > 20:
            ch_match = re.match(r'^(\d+)\s+(.+)', title.strip())
            if ch_match:
                chapters_raw.append((int(ch_match.group(1)), ch_match.group(2).strip(), pg))

    appendices_raw = []
    back_refs = []
    for level, title, page in toc:
        pg = page - 1
        if level == 1:
            app_match = re.match(r'Appendix\s+([A-C]):\s*(.*)', title.strip())
            if app_match:
                appendices_raw.append((app_match.group(1), app_match.group(2).strip(), pg))
            elif 'reference' in title.lower():
                back_refs.append(("references", pg))
            elif 'index' in title.lower():
                back_refs.append(("index", pg))

    # Front matter
    parts = []
    for level, title, page in toc:
        pg = page - 1
        if level == 1 and pg > 20 and 'PART' in title:
            parts.append(pg)
    first_content = min([pg for _, _, pg in chapters_raw] + parts) if chapters_raw else 0
    structure["front_matter"] = {"start": 0, "end": first_content - 1}

    # Chapters
    for i, (ch_num, ch_title, start_pg) in enumerate(chapters_raw):
        if i + 1 < len(chapters_raw):
            end_pg = chapters_raw[i + 1][2] - 1
        else:
            ends = [pg for _, _, pg in appendices_raw] + [pg for _, pg in back_refs]
            end_pg = min(ends) - 1 if ends else total_pages - 1

        slug = slugify(ch_title)
        folder = f"ch{ch_num:02d}_{slug}"

        print(f"  Scanning Ch {ch_num} (pp {start_pg+1}-{end_pg+1}) for sections...")
        sections = find_sections_in_pages(doc, ch_num, start_pg, end_pg)

        structure["chapters"].append({
            "number": ch_num,
            "title": ch_title,
            "folder": folder,
            "start": start_pg,
            "end": end_pg,
            "sections": sections,
        })

    # Appendices
    for i, (letter, title, start_pg) in enumerate(appendices_raw):
        if i + 1 < len(appendices_raw):
            end_pg = appendices_raw[i + 1][2] - 1
        else:
            ends = [pg for _, pg in back_refs]
            end_pg = min(ends) - 1 if ends else total_pages - 1
        structure["appendices"].append({
            "letter": letter,
            "title": title,
            "start": start_pg,
            "end": end_pg,
        })

    # Back matter
    if back_refs:
        structure["back_matter"] = {
            "start": min(pg for _, pg in back_refs),
            "end": total_pages - 1,
        }

    doc.close()

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(structure, f, indent=2)

    print(f"\nWrote {OUTPUT_PATH}")
    print(f"  {len(structure['chapters'])} chapters, {len(structure['appendices'])} appendices")
    for ch in structure['chapters']:
        secs = [s['number'] + ' ' + s['title'] for s in ch['sections']]
        print(f"  Ch {ch['number']:2d}: {ch['title']} (pp {ch['start']+1}-{ch['end']+1}, {len(ch['sections'])} sections)")
        for s in ch['sections']:
            print(f"         {s['number']} {s['title']} (pp {s['start']+1}-{s['end']+1})")
    for ap in structure['appendices']:
        print(f"  App {ap['letter']}: {ap['title']} (pp {ap['start']+1}-{ap['end']+1})")
    if structure['back_matter']:
        bm = structure['back_matter']
        print(f"  Back matter: pp {bm['start']+1}-{bm['end']+1}")


if __name__ == '__main__':
    main()
