# 13 — Contract drift

| 🟣 Field | 🟣 Value |
|---|---|
| Dimension | `13_contract_drift` |
| Runs on | skill |
| Requires API | yes |
| Default enabled | no |

Reads `composable_with:` in SKILL.md. For each declared peer, loads the
peer's SKILL.md and asks Haiku whether their output/input shapes
still line up. Catches silent drift after either side is updated.
