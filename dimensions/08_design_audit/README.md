# Dimension 08 — Design Audit

**What it probes:** the *design docs* a world-class skill must ship.

**Why:** code without design docs rots the fastest — nobody remembers why a decision was made. Per Danny's `principle_50_year_preservation`, a successor opening the repo in 2076 should be able to read + run + continue.

## Checks

| 🟣 Check | 🟣 Severity if missing |
|---|---|
| ARCHITECTURE.md present | major |
| SCHEMA.md present | major |
| CHANGELOG.md present | minor |
| NON_GOALS.md OR "Non-goals" section in SKILL.md | minor |
| `schema_version` field in any config/*.json or logs/*.jsonl | minor |

This dim is also invocable stand-alone via `.snes-fit design-audit --skill <name>` for a fast CI gate.
