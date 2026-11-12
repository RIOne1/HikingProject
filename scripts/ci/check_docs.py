"""Check the repository's Markdown subset without network or dependencies."""

import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]


def prose(text):
    """Ignore HTML comments and fenced examples, preserving line boundaries."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    lines, fence = [], None
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            marker = match[1]
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            lines.append("")
        else:
            lines.append("" if fence else line)
    return "\n".join(lines)


def anchors(text):
    result = set()
    for title in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", prose(text), re.M):
        title = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", title)
        title = title.replace("`", "").replace("*", "").lower()
        slug = "".join(c for c in title if c in " -_" or unicodedata.category(c)[0] in "LN")
        slug = slug.replace(" ", "-")
        candidate, suffix = slug, 0
        while candidate in result:
            suffix += 1
            candidate = f"{slug}-{suffix}"
        result.add(candidate)
    return result


def check_document(path, root):
    errors = []
    text = path.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        errors.append(f"{path.relative_to(root)}: missing final newline")
    for number, line in enumerate(text.splitlines(), 1):
        if line.rstrip() != line:
            errors.append(f"{path.relative_to(root)}:{number}: trailing whitespace")
    # Repository convention: inline links; encode parentheses/spaces in targets.
    for target in re.findall(r"\[[^]\n]*\]\(([^)\n]+)\)", prose(text)):
        target = target.strip().removeprefix("<").removesuffix(">")
        parts = urlsplit(target)
        if parts.scheme or parts.netloc:
            continue  # No external network checks in this fast, offline job.
        destination = (path.parent / unquote(parts.path)).resolve() if parts.path else path.resolve()
        if not destination.is_relative_to(root.resolve()) or not destination.exists():
            errors.append(f"{path.relative_to(root)}: missing/outside local target {target}")
        elif parts.fragment and destination.suffix.lower() == ".md":
            if unquote(parts.fragment) not in anchors(destination.read_text(encoding="utf-8")):
                errors.append(f"{path.relative_to(root)}: missing Markdown anchor {target}")
    return errors


def check_mvp(root):
    errors, versions = [], []
    for filename, acceptance in [("MVP.md", "**Acceptance:**"), ("MVP.zh-CN.md", "**验收：**")]:
        text = (root / "docs" / filename).read_text(encoding="utf-8")
        ids = re.findall(r"^### (MVP-\d+)\b", text, re.M)
        versions.append(ids)
        if len(ids) != len(set(ids)) or not ids:
            errors.append(f"{filename}: missing or duplicate requirement IDs")
        for section in re.split(r"^### MVP-\d+\b", text, flags=re.M)[1:]:
            if section.count(acceptance) != 1:
                errors.append(f"{filename}: each requirement needs one acceptance block")
    if versions[0] != versions[1]:
        errors.append("MVP language versions have different requirement IDs/order")
    return errors


def main():
    paths = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=ROOT
    ).decode().split("\0")
    documents = sorted({ROOT / p for p in paths if p.endswith(".md")})
    errors = [error for path in documents for error in check_document(path, ROOT)]
    errors += check_mvp(ROOT)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Passed: {len(documents)} Markdown files; local links/anchors, whitespace and bilingual MVP structure.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
