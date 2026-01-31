#!/usr/bin/env python3
"""
Download YouTube transcripts for free speech research sources.
Uses yt-dlp to search YouTube and youtube-transcript-api to grab captions.
"""

import os
import re
import json
import subprocess
from youtube_transcript_api import YouTubeTranscriptApi

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "transcripts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Search queries mapped to filenames
SEARCHES = {
    # UC Berkeley / Milo 2017
    "milo yiannopoulos berkeley protest 2017 CNN": "berkeley_milo_cnn",
    "milo yiannopoulos UC berkeley protest NBC news": "berkeley_milo_nbc",
    "berkeley protest milo yiannopoulos 2017 full": "berkeley_milo_full",
    "milo yiannopoulos free speech week berkeley 2017": "berkeley_free_speech_week",

    # USC Uncensored America / Kamala roast
    "uncensored america USC roast kamala harris 2024": "usc_roast_kamala",
    "gavin mcinnes milo USC south carolina 2024": "usc_mcinnes_milo",
    "blatt bonanza USC south carolina 2024": "usc_blatt_bonanza",

    # Charlie Kirk USC
    "charlie kirk USC south carolina 2025": "usc_charlie_kirk",
    "charlie kirk american comeback tour USC": "usc_kirk_comeback",

    # Congressional hearing Dec 2023
    "congressional hearing antisemitism harvard penn MIT december 2023": "congress_antisemitism_hearing",
    "elise stefanik claudine gay genocide question": "stefanik_gay_exchange",
    "harvard MIT penn presidents congress hearing full": "congress_presidents_full",

    # TPUSA / Professor Watchlist
    "turning point USA professor watchlist controversy": "tpusa_professor_watchlist",
    "charlie kirk professor watchlist campus": "kirk_professor_watchlist",

    # Book banning
    "book banning schools 2024 documentary": "book_banning_documentary",
    "banned books school libraries PBS": "banned_books_pbs",
    "the librarians documentary book bans PBS": "librarians_documentary_pbs",

    # FIRE / Free speech
    "FIRE foundation individual rights expression campus free speech": "fire_campus_free_speech",
    "bodies upon the gears FIRE documentary free speech movement": "fire_bodies_gears",
    "silence U university killing free speech": "silence_u_documentary",

    # PEN America
    "PEN america censorship education schools": "pen_america_censorship",

    # General campus free speech
    "campus free speech crisis documentary 2024": "campus_free_speech_crisis",
    "no safe spaces documentary campus": "no_safe_spaces",
}


def search_youtube(query, max_results=3):
    """Use yt-dlp to search YouTube and return video IDs and titles."""
    try:
        cmd = [
            "python3", "-m", "yt_dlp",
            f"ytsearch{max_results}:{query}",
            "--get-id", "--get-title",
            "--no-download", "--no-warnings",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        lines = [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
        videos = []
        # Output alternates: title, id, title, id...
        for i in range(0, len(lines) - 1, 2):
            title = lines[i]
            vid_id = lines[i + 1]
            # Basic sanity check that vid_id looks like a YouTube ID
            if re.match(r'^[\w-]{11}$', vid_id):
                videos.append({"id": vid_id, "title": title})
            else:
                # Maybe title and id got swapped or extra line
                if re.match(r'^[\w-]{11}$', title):
                    videos.append({"id": title, "title": vid_id})
        return videos
    except Exception as e:
        print(f"  Search error: {e}")
        return []


def get_transcript(video_id):
    """Fetch transcript for a YouTube video."""
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
        lines = []
        for snippet in transcript:
            text = snippet.text.strip()
            if text:
                # Format timestamp
                start = snippet.start
                mins = int(start // 60)
                secs = int(start % 60)
                lines.append(f"[{mins:02d}:{secs:02d}] {text}")
        return "\n".join(lines)
    except Exception as e:
        return None


def save_transcript(filename, query, video, transcript_text):
    """Save transcript as markdown with metadata."""
    filepath = os.path.join(OUTPUT_DIR, f"{filename}.md")
    url = f"https://www.youtube.com/watch?v={video['id']}"
    with open(filepath, "w") as f:
        f.write(f"---\n")
        f.write(f"url: {url}\n")
        f.write(f"title: \"{video['title']}\"\n")
        f.write(f"video_id: {video['id']}\n")
        f.write(f"search_query: \"{query}\"\n")
        f.write(f"date_accessed: 2026-01-30\n")
        f.write(f"---\n\n")
        f.write(f"# {video['title']}\n\n")
        f.write(f"**URL:** {url}\n\n")
        f.write(f"## Transcript\n\n")
        f.write(f"```\n{transcript_text}\n```\n")
    return filepath


def main():
    results_log = []
    total = len(SEARCHES)

    for i, (query, filename) in enumerate(SEARCHES.items(), 1):
        print(f"\n[{i}/{total}] Searching: {query}")
        videos = search_youtube(query, max_results=3)

        if not videos:
            print(f"  No results found")
            results_log.append({"query": query, "filename": filename, "status": "no_results"})
            continue

        # Try each result until we get a transcript
        got_transcript = False
        for video in videos:
            print(f"  Trying: {video['title']} ({video['id']})")
            transcript = get_transcript(video['id'])
            if transcript:
                path = save_transcript(filename, query, video, transcript)
                print(f"  Saved: {path}")
                results_log.append({
                    "query": query, "filename": filename,
                    "status": "success", "video_id": video["id"],
                    "title": video["title"]
                })
                got_transcript = True
                break
            else:
                print(f"  No transcript available")

        if not got_transcript:
            # Save metadata even without transcript
            results_log.append({
                "query": query, "filename": filename,
                "status": "no_transcript",
                "videos_found": [v["title"] for v in videos]
            })

    # Write summary
    summary_path = os.path.join(OUTPUT_DIR, "_summary.json")
    with open(summary_path, "w") as f:
        json.dump(results_log, f, indent=2)

    # Print summary
    success = sum(1 for r in results_log if r["status"] == "success")
    no_transcript = sum(1 for r in results_log if r["status"] == "no_transcript")
    no_results = sum(1 for r in results_log if r["status"] == "no_results")
    print(f"\n{'='*60}")
    print(f"DONE: {success} transcripts downloaded, {no_transcript} no captions, {no_results} no results")
    print(f"Files saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
