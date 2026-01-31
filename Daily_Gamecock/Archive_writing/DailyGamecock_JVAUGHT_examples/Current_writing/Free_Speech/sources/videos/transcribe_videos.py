#!/usr/bin/env python3
"""Download YouTube audio and prepare for Whisper transcription."""

import os
import subprocess
import sys
from pathlib import Path

os.environ["PATH"] = "/Users/user/Library/Python/3.9/bin:" + os.environ.get("PATH", "")

VIDEOS = [
    ("An2BezIuAiI", "The fight against book bans by public school librarians", "banned_books_pbs"),
    ("QkbXrWlwCx8", "'The Librarians' documentary explores censorship", "librarians_documentary_pbs"),
    ("fNxjkNpljKs", "FIRE: Defending Free Speech on Campus", "fire_campus_free_speech"),
    ("QT2rwEkGFM4", "Bodies Upon the Gears: Birth of the Free Speech Movement (FULL)", "fire_bodies_gears"),
    ("x5uaVFfX3AQ", "Silence U: Is the University Killing Free Speech?", "silence_u_documentary"),
    ("qR71QIZbFII", "PEN America – Book Bans and Censorship", "pen_america_censorship"),
    ("0o602iSVBcg", "Where do libertarians stand on campus wars? (Reason)", "campus_free_speech_crisis"),
    ("9NhLxYUbY0I", "Defending the First Amendment - No Safe Spaces", "no_safe_spaces"),
]

AUDIO_DIR = Path(__file__).parent / "audio"


def download_audio():
    """Download audio from YouTube videos as 16kHz mono WAV for Whisper."""
    AUDIO_DIR.mkdir(exist_ok=True)

    for video_id, title, filename in VIDEOS:
        output_path = AUDIO_DIR / f"{filename}.wav"
        if output_path.exists():
            print(f"Skipping {filename} (already exists)")
            continue

        url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Downloading: {title}")

        cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "wav",
            "--postprocessor-args", "ffmpeg:-ar 16000 -ac 1",
            "-o", str(AUDIO_DIR / f"{filename}.%(ext)s"),
            url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ERROR: {result.stderr[:200]}")
        else:
            print(f"  Saved: {output_path}")


if __name__ == "__main__":
    download_audio()
