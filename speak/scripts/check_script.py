#!/usr/bin/env python3
"""Flag text that the speech engine would read wrongly.

Exit code 1 means at least one ERROR. WARN lines do not block the audio.

Usage: check_script.py SCRIPT.txt
"""
import re
import sys
from pathlib import Path

# Tested on this engine: these capital-letter words are read acceptably.
SAFE_CAPS = {"RNA", "DNA", "GPU", "CPU", "PCA", "UMAP", "MP3", "HPC", "API", "PDF", "ATAC"}

ERROR_PATTERNS = [
    (r"[<>=~/\\_`|^*#$@{}\[\]%&+]", "symbol: write it as words"),
    (r"[←-⇿∀-⋿²³—–]", "symbol: write it as words"),
    (r"\b\d+(\.\d+)?[eE][-+]?\d+\b", "scientific notation: say it as a rounded value or in words"),
    (r"\b\d{4}-\d{2}-\d{2}\b", "date: say it in words"),
    (r"\b\d+\.\d+\.\d+", "version or dotted number: remove it, or say it in words"),
    (r"\b\d{5,}\b", "long number: round it, or remove it if it is an identifier"),
    (r"\b\d+\.\d{3,}\b", "too many decimal places: round it"),
    (r"\b\w+\.(py|sh|md|txt|csv|json|h5ad|ipynb|mp3)\b", "file name: describe the file instead"),
    (r"\b(e\.g\.|i\.e\.|etc\.|vs\.|cf\.)", "abbreviation: write it as plain words"),
    (r"\b\w+(n't|n’t)\b", "negative contraction: write cannot, does not, and so on"),
]


def main() -> int:
    path = Path(sys.argv[1])
    text = path.read_text()
    errors = warnings = 0

    for number, line in enumerate(text.splitlines(), 1):
        for pattern, why in ERROR_PATTERNS:
            for match in re.finditer(pattern, line):
                print(f"ERROR line {number}: {match.group(0)!r}: {why}")
                errors += 1
        for word in re.findall(r"\b[A-Z][A-Z0-9-]{2,}\b", line):
            if word not in SAFE_CAPS:
                print(f"ERROR line {number}: {word!r}: spell it out, as in I C C, or add it to references/pronunciation.md and SAFE_CAPS after testing")
                errors += 1
        for char in sorted({c for c in line if ord(c) > 127 and c not in "‘’“”"}):
            print(f"ERROR line {number}: {char!r}: non-English character")
            errors += 1

    for sentence in re.split(r"(?<=[.!?])\s+", text):
        count = len(sentence.split())
        if count > 25:
            print(f"WARN {count} words: {sentence[:70]}...")
            warnings += 1

    for section in re.split(r"\n\s*\n", text):
        count = len(re.findall(r"[.!?](?:\s|$)", section))
        if count > 6:
            print(f"WARN section of {count} sentences: {section[:70]}...")
            warnings += 1

    print(f"{errors} errors, {warnings} warnings, {len(text.split())} words")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
