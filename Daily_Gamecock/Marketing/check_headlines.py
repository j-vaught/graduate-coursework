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

# Approximate characters per line at 44pt font on letter paper with 0.9in margins
# Calibrated against actual PDF output - word-wrap occurs around 25 chars
CHARS_PER_LINE = 25

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

def simulate_word_wrap(text, chars_per_line=CHARS_PER_LINE):
    """
    Simulate word-wrap and return number of lines.
    Words don't break mid-word, just like in the actual PDF.
    """
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        # Check if adding this word would exceed line width
        test_line = current_line + (" " if current_line else "") + word

        if len(test_line) <= chars_per_line:
            current_line = test_line
        else:
            # Start new line
            if current_line:
                lines.append(current_line)
            current_line = word

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
    print(f"Chars per line (approx): {CHARS_PER_LINE}")
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
