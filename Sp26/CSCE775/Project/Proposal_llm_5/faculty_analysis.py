import os
import re
import json
from collections import Counter, defaultdict

FACULTY_DIR = "uofsc_cs_faculty"
FACULTY_FILES = [f for f in os.listdir(FACULTY_DIR) if f.endswith(".md") and f != "faculty_list.md"]

def parse_faculty_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    name = content.split("\n")[0].replace("# ", "").split(" - ")[0].strip()
    
    # Extract Title
    title_match = re.search(r"\*\*Title:\*\* (.*)", content)
    title = title_match.group(1).strip() if title_match else "N/A"
    
    # Extract Education (PhD Institution)
    edu_match = re.search(r"Ph\.D\..*? ([A-Z][a-zA-Z\s,]+(?:University|School|Institute|College)[a-zA-Z\s,]*)", content, re.IGNORECASE)
    phd_inst = edu_match.group(1).strip() if edu_match else "Unknown"
    
    # Extract Research Areas
    research_match = re.search(r"\*\*Research Areas:\*\* (.*)", content)
    research_areas = [area.strip() for area in research_match.group(1).split(",")] if research_match else []
    
    # Extract Publications
    pubs = []
    # Match numbered publications: 1. Title. *Journal*, Year.
    pub_pattern = re.compile(r"\d+\.\s+(.*?)\.\s+\*(.*?)\*,\s+(?:.*,\s+)?(\d{4})")
    for match in pub_pattern.finditer(content):
        title_text, venue, year = match.groups()
        pubs.append({
            "title": title_text,
            "venue": venue,
            "year": int(year)
        })
    
    return {
        "name": name,
        "title": title,
        "phd_inst": phd_inst,
        "research_areas": research_areas,
        "publications": pubs
    }

def run_analysis():
    data = []
    for filename in FACULTY_FILES:
        data.append(parse_faculty_file(os.path.join(FACULTY_DIR, filename)))

    # 1. Collaboration Graph
    # We look for faculty names in other faculty's publication titles or (implicitly) by comparing titles
    collabs = defaultdict(int)
    faculty_names = [d["name"] for d in data]
    
    # Map of Title -> List of Faculty who authored it
    pub_map = defaultdict(list)
    for faculty in data:
        for pub in faculty["publications"]:
            pub_map[pub["title"].lower()].append(faculty["name"])
    
    for authors in pub_map.values():
        if len(authors) > 1:
            for i in range(len(authors)):
                for j in range(i + 1, len(authors)):
                    pair = tuple(sorted([authors[i], authors[j]]))
                    collabs[pair] += 1

    # 2. Research Pulse (Keyword Comparison)
    keywords_old = []
    keywords_new = []
    pulse_keywords = ["ai", "learning", "network", "system", "data", "software", "security", "wireless", "medical", "robot", "llm", "neurosymbolic", "causal", "vision"]
    
    for faculty in data:
        for pub in faculty["publications"]:
            words = pub["title"].lower().split()
            if 2010 <= pub["year"] <= 2015:
                keywords_old.extend([w for w in words if any(k in w for k in pulse_keywords)])
            elif 2024 <= pub["year"] <= 2026:
                keywords_new.extend([w for w in words if any(k in w for k in pulse_keywords)])

    # 3. Academic Lineage
    lineage = Counter([d["phd_inst"] for d in data])

    # 4. LLM Adoption Score
    llm_keywords = ["llm", "large language model", "transformer", "hallucination", "rag", "generative ai", "gpt"]
    llm_scores = {}
    for faculty in data:
        score = 0
        recent_pubs = [p for p in faculty["publications"] if p["year"] >= 2024]
        for pub in recent_pubs:
            if any(k in pub["title"].lower() for k in llm_keywords):
                score += 1
        llm_scores[faculty["name"]] = score

    # Generate Report
    print("## 1. Internal Collaboration Graph (Top Collaborators)")
    sorted_collabs = sorted(collabs.items(), key=lambda x: x[1], reverse=True)
    for pair, count in sorted_collabs[:10]:
        print(f"- {pair[0]} & {pair[1]}: {count} shared papers")

    print("\n## 2. Research Pulse (Keyword Frequency Shift)")
    old_count = Counter(keywords_old).most_common(10)
    new_count = Counter(keywords_new).most_common(10)
    print("### 2010-2015 Top Keywords:")
    print(", ".join([f"{k} ({v})" for k, v in old_count]))
    print("### 2024-2026 Top Keywords:")
    print(", ".join([f"{k} ({v})" for k, v in new_count]))

    print("\n## 3. Academic Lineage (Ph.D. Origins)")
    for inst, count in lineage.most_common(10):
        print(f"- {inst}: {count} faculty")

    print("\n## 4. LLM Adoption Score (Top 2024-2026)")
    sorted_llm = sorted(llm_scores.items(), key=lambda x: x[1], reverse=True)
    for name, score in sorted_llm[:10]:
        if score > 0:
            print(f"- {name}: {score} LLM-related publications")

if __name__ == "__main__":
    run_analysis()
