#!/usr/bin/env python3
"""Download and convert web sources to markdown with YAML front-matter."""

import os
import re
import sys
import time
import datetime
import requests
import html2text
from bs4 import BeautifulSoup
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

def sanitize_filename(title, url):
    """Create a safe filename from title or URL."""
    name = title if title else urlparse(url).path.split("/")[-1]
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s]+', '_', name.strip())
    name = name[:80]
    if not name:
        name = re.sub(r'[^\w]', '_', urlparse(url).netloc + urlparse(url).path)[:80]
    return name


def extract_title(soup):
    """Extract page title from HTML."""
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"].strip()
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)
    return ""


def download_source(url, output_dir, prefix=""):
    """Download a URL and save as markdown or PDF."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
        resp.raise_for_status()
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}")
        return None

    content_type = resp.headers.get("Content-Type", "")
    date_accessed = datetime.date.today().isoformat()

    # Handle PDFs
    if "application/pdf" in content_type or url.lower().endswith(".pdf"):
        soup = BeautifulSoup("", "html.parser")
        title = urlparse(url).path.split("/")[-1].replace(".pdf", "")
        fname = sanitize_filename(title, url) + ".pdf"
        fpath = os.path.join(output_dir, prefix + fname)
        with open(fpath, "wb") as f:
            f.write(resp.content)
        print(f"  PDF saved: {fpath}")
        return {"url": url, "file": prefix + fname, "title": title, "type": "pdf"}

    # Handle HTML
    soup = BeautifulSoup(resp.text, "html.parser")
    title = extract_title(soup)

    # Remove nav, footer, ads, scripts
    for tag in soup.find_all(["nav", "footer", "script", "style", "aside",
                               "iframe", "noscript"]):
        tag.decompose()
    for cls in ["ad", "advertisement", "sidebar", "menu", "nav", "footer",
                "cookie", "popup", "modal", "social-share"]:
        for el in soup.find_all(class_=re.compile(cls, re.I)):
            el.decompose()

    # Find main content
    main = (soup.find("article") or soup.find("main") or
            soup.find("div", class_=re.compile("content|article|post", re.I)) or
            soup.find("body"))

    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.body_width = 0
    md_content = h.handle(str(main)) if main else h.handle(resp.text)

    # Build front-matter
    front_matter = f"""---
url: {url}
title: "{title.replace('"', "'")}"
date_accessed: {date_accessed}
---

"""
    fname = sanitize_filename(title, url) + ".md"
    fpath = os.path.join(output_dir, prefix + fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(front_matter + md_content)
    print(f"  Saved: {fpath}")
    return {"url": url, "file": prefix + fname, "title": title, "type": "md"}


def download_batch(urls, output_dir, prefix=""):
    """Download a list of URLs, return results."""
    results = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url}")
        r = download_source(url, output_dir, prefix)
        if r:
            results.append(r)
        time.sleep(1)  # polite delay
    return results


# Cited sources from the article
CITED_URLS = [
    "https://www.dailygamecock.com/article/2024/09/column-opinion-the-uncensored-america-should-not-be-taken-seriously-opinion-dunn",
    "https://www.wistv.com/2024/09/13/usc-student-government-denies-funding-scheduled-roast-vice-president-kamala-harris/",
    "https://www.dailygamecock.com/article/2024/10/uncensored-america-sues-usc-days-after-student-senate-grants-funding-for-roast-elam-news",
    "https://www.thefire.org/news/kamala-harris-comedy-roast-denied-funding-university-south-carolina-student-senate",
    "https://pen.org/report/americas-censored-campuses-25-web-of-control/",
    "https://www.insidehighered.com/news/faculty-issues/curriculum/2026/01/15/report-state-lawmakers-enacted-21-censorship-bills-2025",
    "https://pen.org/book-bans/pen-america-index-of-school-book-bans-2024-2025/",
    "https://www.ala.org/bbooks/book-ban-data",
    "https://en.wikipedia.org/wiki/Professor_Watchlist",
    "https://www.thefire.org/news/dual-purpose-tpusa-watchlist-warrants-two-toned-response",
    "https://www.insidehighered.com/news/2017/12/19/arizona-state-student-events-official-assaulted-political-group",
    "https://www.chronicle.com/article/charlie-kirks-watch-list-made-some-professors-lives-a-living-hell",
    "https://www.theguardian.com/us-news/2017/feb/21/milo-yiannopoulos-resigns-breitbart-pedophilia-comments",
    "https://www.bbc.com/news/world-us-canada-38837142",
    "https://www.washingtonpost.com/news/grade-point/wp/2017/02/01/protests-at-uc-berkeley-prompted-by-milo-yiannopoulos/",
    "https://www.dailygamecock.com/article/2024/10/guest-column-free-speech-events-deserve-funding-opinion-connors",
    "https://www.wltx.com/article/news/local/controversial-event-usc/101-2c3eebfb-b310-4f96-bf66-6d098dc6b1f3",
    "https://www.techdirt.com/2019/07/11/splc-asks-court-to-toss-proud-boy-founders-defamation-lawsuit-asking-wheres-lie/",
    "https://www.postandcourier.com/politics/sc-gop-delegation-tells-usc-clemson-to-eradicate-critical-race-theory/article_85e96e5e-d53f-11eb-9e0b-7f0e925f3c53.html",
    "https://www.scstatehouse.gov/sess126_2025-2026/bills/3184.htm",
    "https://www.scstatehouse.gov/sess126_2025-2026/bills/368.htm",
    "https://www.scstatehouse.gov/sess126_2025-2026/bills/4749.htm",
    "https://www.postandcourier.com/education-lab/usc-doj-charlie-kirk-outdoor-event-controversial/article_c1d6ca0b-1173-403d-bd16-6f8fec66f748.html",
    "https://abcnews4.com/news/state/assistant-ag-demands-usc-continue-outdoor-debates-september-2025-columbia",
    "https://www.dailygamecock.com/article/2024/09/over-1000-students-attend-blatt-bonanza-during-controversial-campus-event-news-grady",
    "https://wach.com/news/local/usc-students-seek-safe-space-at-usc-event-during-controversial-political-roast",
    "https://www.statehousereport.com/2024/09/06/more-news-usc-gets-high-marks-for-free-speech-as-controversy-roils-campus/",
    "https://www.thefire.org/news/tale-two-universities-why-south-carolina-soared-and-harvard-didnt-fires-free-speech-rankings",
]


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))

    mode = sys.argv[1] if len(sys.argv) > 1 else "cited"

    if mode == "cited":
        out = os.path.join(base, "cited")
        os.makedirs(out, exist_ok=True)
        results = download_batch(CITED_URLS, out)
        print(f"\nDownloaded {len(results)}/{len(CITED_URLS)} cited sources.")

    elif mode == "additional":
        # Read URLs from stdin, one per line
        out = os.path.join(base, "additional")
        os.makedirs(out, exist_ok=True)
        urls = [line.strip() for line in sys.stdin if line.strip()]
        results = download_batch(urls, out)
        print(f"\nDownloaded {len(results)}/{len(urls)} additional sources.")

    elif mode == "single":
        # Download a single URL: python download_sources.py single <url> <output_dir>
        url = sys.argv[2]
        out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(base, "additional")
        os.makedirs(out, exist_ok=True)
        r = download_source(url, out)
        if r:
            print(f"Downloaded: {r['file']}")
