#!/usr/bin/env python3
"""Validate the skill folder: frontmatter rules and that every referenced file exists.

Usage: python3 validate_skill.py [skill_dir]   (default: parent of this script)
"""
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parent.parent)
errors = []

skill = root / "SKILL.md"
if not skill.exists():
    sys.exit("FAIL: SKILL.md missing")
text = skill.read_text()

m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
if not m:
    errors.append("frontmatter block missing")
else:
    fm = m.group(1)
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    if not name:
        errors.append("frontmatter: name missing")
    elif not re.fullmatch(r"[a-z0-9-]{1,64}", name.group(1).strip()):
        errors.append("frontmatter: name must be lowercase letters/digits/hyphens, <=64 chars")
    elif name.group(1).strip() != root.name:
        errors.append(f"frontmatter: name '{name.group(1).strip()}' != folder '{root.name}'")
    desc = re.search(r"^description:\s*>-?\n((?:  .*\n?)+)", fm + "\n", re.M) or \
        re.search(r"^description:\s*(.+)$", fm, re.M)
    if not desc:
        errors.append("frontmatter: description missing")
    else:
        d = " ".join(line.strip() for line in desc.group(1).splitlines())
        if len(d) > 1024:
            errors.append(f"frontmatter: description is {len(d)} chars (max 1024)")
        if "<" in d or ">" in d:
            errors.append("frontmatter: description must not contain angle brackets")

body_lines = text.count("\n")
if body_lines > 500:
    errors.append(f"SKILL.md is {body_lines} lines (keep under 500; move detail to references/)")

all_md = "\n".join(p.read_text() for p in root.rglob("*.md"))
for ref in sorted(set(re.findall(r"`((?:references|templates|scripts|examples)/[\w./-]+)`", all_md))):
    if "*" in ref:
        continue
    if not (root / ref).exists():
        errors.append(f"referenced file missing: {ref}")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)
files = sorted(p.relative_to(root) for p in root.rglob("*") if p.is_file())
print(f"OK: {root.name} ({len(files)} files)")
