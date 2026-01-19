#!/usr/bin/env python3
"""
Headline Length Checker for Daily Gamecock Marketing Flyers

Simulates word-wrap to detect headlines that will span 3+ lines.
The template is designed for 2-line headlines only.

Usage: python3 check_headlines.py [file.tex ...]
       If no files specified, checks all Marketing_*.tex files.
"""

import re
import sys
import glob

# Proportional character widths for serif fonts like TeX Gyre Pagella (Palatino).
# Values are relative to lowercase 'm' = 1.0, derived from averaged AFM metrics
# across multiple serif fonts. Narrower letters (i, l, t, f, j, 1, punctuation)
# have smaller values; wider letters (m, w, W, M, capitals) have larger values.
# Source: https://pschanely.github.io/2022/04/11/relative-per-character-widths.html
CHAR_WIDTHS = {
    # Lowercase letters
    'a': 0.619, 'b': 0.655, 'c': 0.585, 'd': 0.655, 'e': 0.619,
    'f': 0.381, 'g': 0.655, 'h': 0.655, 'i': 0.312, 'j': 0.312,
    'k': 0.621, 'l': 0.312, 'm': 1.0,   'n': 0.655, 'o': 0.655,
    'p': 0.655, 'q': 0.655, 'r': 0.414, 's': 0.55,  't': 0.346,
    'u': 0.655, 'v': 0.621, 'w': 0.897, 'x': 0.621, 'y': 0.621,
    'z': 0.585,
    # Uppercase letters
    'A': 0.864, 'B': 0.829, 'C': 0.862, 'D': 0.897, 'E': 0.793,
    'F': 0.724, 'G': 0.931, 'H': 0.897, 'I': 0.381, 'J': 0.55,
    'K': 0.864, 'L': 0.726, 'M': 1.071, 'N': 0.897, 'O': 0.931,
    'P': 0.758, 'Q': 0.931, 'R': 0.862, 'S': 0.758, 'T': 0.759,
    'U': 0.897, 'V': 0.864, 'W': 1.173, 'X': 0.864, 'Y': 0.864,
    'Z': 0.759,
    # Numbers (uniform width in most fonts)
    '0': 0.655, '1': 0.655, '2': 0.655, '3': 0.655, '4': 0.655,
    '5': 0.655, '6': 0.655, '7': 0.655, '8': 0.655, '9': 0.655,
    # Punctuation and special characters
    ' ': 0.328,  # Space
    '.': 0.328, ',': 0.328, ':': 0.328, ';': 0.328,
    '!': 0.381, '?': 0.619,
    "'": 0.347, '"': 0.5,
    '-': 0.4,   '$': 0.655, '%': 0.9, '&': 0.8,
}
# Default width for characters not in the table
DEFAULT_CHAR_WIDTH = 0.6

# Line width threshold calibrated for 44pt TeX Gyre Pagella on letter paper
# with 0.9in margins. Set conservatively to catch borderline cases - better
# to flag a headline that fits than miss one that doesn't.
LINE_WIDTH_THRESHOLD = 14.5


def get_text_width(text):
    """Calculate proportional width of text using character width table."""
    return sum(CHAR_WIDTHS.get(c, DEFAULT_CHAR_WIDTH) for c in text)

def extract_flyers(filepath):
    """Extract all headlines and subheads from MakeFlyer commands."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Pattern to match \MakeFlyer{headline}{subhead}
    pattern = r'\\MakeFlyer\s*\n?\s*\{([^}]+)\}\s*\n?\s*\{([^}]+)\}'
    matches = re.findall(pattern, content)

    return matches

def clean_latex(text):
    """Remove LaTeX commands for length calculation."""
    clean = text.strip()
    clean = re.sub(r'\\textit\{([^}]*)\}', r'\1', clean)
    clean = re.sub(r'\\textbf\{([^}]*)\}', r'\1', clean)
    clean = re.sub(r'\\\$', '$', clean)  # escaped dollar signs
    clean = re.sub(r'\\%', '%', clean)   # escaped percent
    clean = re.sub(r'\\&', '&', clean)   # escaped ampersand
    return clean

def simulate_word_wrap(text, line_width=LINE_WIDTH_THRESHOLD):
    """
    Simulate word-wrap using proportional character widths.
    Words don't break mid-word, just like in the actual PDF.
    """
    words = text.split()
    lines = []
    current_line = ""
    current_width = 0.0

    for word in words:
        word_width = get_text_width(word)
        space_width = CHAR_WIDTHS.get(' ', DEFAULT_CHAR_WIDTH)

        # Check if adding this word would exceed line width
        test_width = current_width + (space_width if current_line else 0) + word_width

        if test_width <= line_width:
            current_line = current_line + (" " if current_line else "") + word
            current_width = test_width
        else:
            # Start new line
            if current_line:
                lines.append(current_line)
            current_line = word
            current_width = word_width

    # Don't forget the last line
    if current_line:
        lines.append(current_line)

    return lines

def check_headline(headline, max_lines=2):
    """Check if headline exceeds max lines when word-wrapped."""
    clean = clean_latex(headline)
    lines = simulate_word_wrap(clean)
    return lines, len(lines) > max_lines

def main():
    # Get files to check
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        files = sorted(glob.glob('Marketing_*.tex'))

    if not files:
        print("No .tex files found!")
        sys.exit(1)

    warnings = []
    total_flyers = 0

    for filepath in files:
        flyers = extract_flyers(filepath)

        for headline, subhead in flyers:
            total_flyers += 1
            lines, too_long = check_headline(headline)

            if too_long:
                warnings.append({
                    'file': filepath,
                    'headline': headline.strip(),
                    'lines': lines,
                    'line_count': len(lines)
                })

    # Print results
    print(f"\n{'='*70}")
    print(f"HEADLINE LENGTH CHECK - Daily Gamecock Flyers")
    print(f"{'='*70}")
    print(f"Files checked: {len(files)}")
    print(f"Total flyers: {total_flyers}")
    print(f"Max lines allowed: 2")
    print(f"Line width threshold: {LINE_WIDTH_THRESHOLD} (proportional units)")
    print(f"{'='*70}\n")

    if warnings:
        print(f"WARNING: {len(warnings)} headlines wrap to 3+ lines:\n")

        for i, w in enumerate(warnings, 1):
            print(f"{i}. [{w['file']}] ({w['line_count']} lines)")
            print(f"   \"{w['headline']}\"")
            print(f"   Wrapped preview:")
            for j, line in enumerate(w['lines'], 1):
                print(f"      Line {j}: \"{line}\"")
            print()

        print(f"{'='*70}")
        print(f"SUMMARY: {len(warnings)} headlines need shortening")
        print(f"{'='*70}")
        sys.exit(1)
    else:
        print("All headlines fit within 2 lines!")
        print(f"{'='*70}")
        sys.exit(0)

if __name__ == '__main__':
    main()
