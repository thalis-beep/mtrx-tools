# MTRX Skills

## animation-director

The AI Animation Production Director. It turns a Creative Strategist script into a
production-ready animated ad, through Higgsfield (Plan A), an external-tool prompt
package (Plan B), or a mix of the two (Hybrid).

Start with `animation-director/SKILL.md`. The worked example is in
`animation-director/examples/walkthrough.md`.

### Install

Build the shareable zip:
```bash
bash skills/animation-director/scripts/package_skill.sh
# → skills/dist/animation-director.zip
```

- **Claude (claude.ai / Desktop):** Settings → Capabilities → Skills → upload
  `animation-director.zip`. Connect the Higgsfield connector for Plan A.
- **Claude Code:** copy the `animation-director/` folder into `~/.claude/skills/`
  (personal) or `<project>/.claude/skills/` (shared with the repo).
- **ChatGPT / other assistants that support the SKILL.md (Agent Skills) format:**
  upload the same zip where that product accepts skills. If the product has no skill
  support, paste `SKILL.md` into a Custom GPT / project's instructions and attach the
  `references/` and `templates/` files as knowledge. The Higgsfield steps only run
  when a Higgsfield connector is available. Otherwise the skill falls back to Plan B.

### Maintain
- After every job, add a retro to `references/house-lessons.md`.
- Re-quote credits periodically and refresh the cost snapshot in
  `references/credit-budgeting.md`.
- Run `python3 skills/animation-director/scripts/validate_skill.py` before re-packaging.
