#!/usr/bin/env bash
# Validate the skill, then zip it as <repo>/skills/dist/animation-director.zip
# (zip root contains the animation-director/ folder, the layout skill uploaders expect).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
skill_dir="$(dirname "$here")"
skills_root="$(dirname "$skill_dir")"
name="$(basename "$skill_dir")"

python3 "$here/validate_skill.py" "$skill_dir"
mkdir -p "$skills_root/dist"
rm -f "$skills_root/dist/$name.zip"
(cd "$skills_root" && zip -qr "dist/$name.zip" "$name" -x '*/__pycache__/*' '*.DS_Store')
echo "Packaged: $skills_root/dist/$name.zip"
