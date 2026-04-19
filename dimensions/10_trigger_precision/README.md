# 10 — Trigger precision

| 🟣 Field | 🟣 Value |
|---|---|
| Dimension | `10_trigger_precision` |
| Runs on | skill |
| Requires API | yes |
| Default enabled | no |

Runs true-positive and collision-case prompts through the skill and
asks Haiku whether the skill correctly fired (or correctly declined).
User-authored tests at `evals/<skill>/trigger-tests.json` take priority;
otherwise auto-generated from SKILL.md's `NOT for:` clauses.
