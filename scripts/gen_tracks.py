#!/usr/bin/env python3
"""
Scans all solution files in problems/ (excluding scratch/ and inbox/),
parses metadata headers, groups by platform, and generates track README
files with solution tables sorted by id.
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_DIR = ROOT / "problems"
TRACKS_DIR = ROOT / "tracks"

EXCLUDE_DIRS = {"scratch", "inbox"}

PLATFORM_MAP = {
    "lc": ("leetcode", "LeetCode"),
    "cf": ("codeforces", "Codeforces"),
    "csc2720": ("csc_2720", "CSC 2720"),
}

FILENAME_PREFIX_MAP = {
    "lc-": "lc",
    "cf-": "cf",
    "csc2720-": "csc2720",
}


def parse_metadata(filepath):
    """Parse the metadata header from a solution file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(2000)
    except Exception:
        return None

    header = None
    if content.lstrip().startswith('"""'):
        match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if match:
            header = match.group(1)
    elif content.lstrip().startswith("/*"):
        match = re.search(r'/\*(.*?)\*/', content, re.DOTALL)
        if match:
            header = match.group(1)

    if not header:
        return None

    metadata = {}
    for line in header.splitlines():
        line = line.strip()
        m = re.match(r'^(\w+)\s*:\s*(.+)$', line)
        if m:
            key = m.group(1).strip()
            value = m.group(2).strip()
            if key in ("platform", "id", "name", "pattern", "tags"):
                metadata[key] = value

    if "platform" in metadata:
        return metadata
    return None


def detect_platform_from_filename(filename):
    """Try to detect platform from the filename prefix."""
    for prefix, platform in FILENAME_PREFIX_MAP.items():
        if filename.startswith(prefix):
            return platform
    return None


def extract_info_from_filename(filename, platform_prefix):
    """Extract id and name from a filename like 'lc-125-valid-palindrome.py'."""
    stem = Path(filename).stem

    if platform_prefix in ("lc", "cf"):
        m = re.match(r'^(?:lc|cf)-([^-]+)-(.+)$', stem)
        if m:
            return m.group(1), m.group(2)
    elif platform_prefix == "csc2720":
        m = re.match(r'^csc2720-(.+)$', stem)
        if m:
            return "", m.group(1)

    return None, None


def get_pattern_from_path(filepath):
    """Extract the pattern (subdirectory path relative to problems/) from a file path."""
    rel = filepath.relative_to(PROBLEMS_DIR)
    return str(rel.parent)


def title_case_name(slug):
    """Convert a hyphen-separated slug to title case."""
    if not slug:
        return ""
    words = slug.split("-")
    result = []
    roman_numerals = {"i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"}
    for w in words:
        if w.lower() in roman_numerals and len(w) <= 4:
            result.append(w.upper())
        else:
            result.append(w.capitalize())
    return " ".join(result)


def sort_key_lc(entry):
    """Sort key for LeetCode: numeric id."""
    try:
        return (0, int(entry["id"]), entry["name"])
    except (ValueError, TypeError):
        return (1, 0, entry.get("name", ""))


def sort_key_cf(entry):
    """Sort key for Codeforces: alphanumeric id (e.g. 4A, 69A, 499B)."""
    raw_id = entry.get("id", "")
    m = re.match(r'^(\d+)([A-Za-z]*)$', raw_id)
    if m:
        return (0, int(m.group(1)), m.group(2), entry["name"])
    return (1, 0, raw_id, entry.get("name", ""))


def sort_key_generic(entry):
    """Generic sort: by name."""
    return (entry.get("name", ""),)


def make_relative_link(filepath):
    """Make a relative link from tracks/<track>/README.md to the solution file."""
    rel = filepath.relative_to(PROBLEMS_DIR)
    return f"../../problems/{rel}"


def collect_solutions():
    """Walk the problems directory and collect all solution entries."""
    solutions = {}

    for dirpath, dirnames, filenames in os.walk(PROBLEMS_DIR):
        dirpath = Path(dirpath)

        rel_to_problems = dirpath.relative_to(PROBLEMS_DIR)
        top_level = rel_to_problems.parts[0] if rel_to_problems.parts else ""
        if top_level in EXCLUDE_DIRS:
            continue

        for filename in filenames:
            if not (filename.endswith(".py") or filename.endswith(".cpp")):
                continue

            filepath = dirpath / filename
            pattern = get_pattern_from_path(filepath)

            meta = parse_metadata(filepath)

            if meta and meta.get("platform"):
                platform = meta["platform"]
                entry = {
                    "id": meta.get("id", ""),
                    "name": meta.get("name", ""),
                    "pattern": meta.get("pattern", pattern),
                    "tags": meta.get("tags", ""),
                    "filepath": filepath,
                }
            else:
                platform = detect_platform_from_filename(filename)
                if platform:
                    file_id, file_name = extract_info_from_filename(filename, platform)
                    if file_name is None:
                        continue
                    entry = {
                        "id": file_id or "",
                        "name": file_name,
                        "pattern": pattern,
                        "tags": "",
                        "filepath": filepath,
                    }
                else:
                    continue

            if platform not in solutions:
                solutions[platform] = []
            solutions[platform].append(entry)

    return solutions


def generate_readme(platform, entries):
    """Generate README content for a given platform track."""
    if platform not in PLATFORM_MAP:
        return None, None

    track_dir, title = PLATFORM_MAP[platform]

    if platform == "lc":
        entries.sort(key=sort_key_lc)
    elif platform == "cf":
        entries.sort(key=sort_key_cf)
    else:
        entries.sort(key=sort_key_generic)

    lines = [
        f"# {title}",
        "",
        "Canonical solutions live in `/problems`.",
        "",
        "| # | Problem | Pattern | Tags |",
        "|---|---------|---------|------|",
    ]

    for entry in entries:
        display_id = entry["id"]
        display_name = title_case_name(entry["name"])
        link = make_relative_link(entry["filepath"])
        pattern = entry.get("pattern", "")
        tags = entry.get("tags", "")

        lines.append(
            f"| {display_id} | [{display_name}]({link}) | {pattern} | {tags} |"
        )

    lines.append("")
    return track_dir, "\n".join(lines)


def main():
    solutions = collect_solutions()

    for platform, entries in solutions.items():
        result = generate_readme(platform, entries)
        if result is None:
            print(f"  Skipping unknown platform: {platform}")
            continue

        track_dir, content = result
        readme_path = TRACKS_DIR / track_dir / "README.md"

        if not readme_path.parent.exists():
            print(f"  Warning: track directory {readme_path.parent} does not exist, creating it")
            readme_path.parent.mkdir(parents=True, exist_ok=True)

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"  Generated {readme_path} ({len(entries)} solutions)")

    print(f"\nPlatforms found: {', '.join(sorted(solutions.keys()))}")
    print(f"Total solutions: {sum(len(v) for v in solutions.values())}")


if __name__ == "__main__":
    main()
