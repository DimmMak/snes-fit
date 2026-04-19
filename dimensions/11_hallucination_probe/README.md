# 11 — Hallucination probe

| 🟣 Field | 🟣 Value |
|---|---|
| Dimension | `11_hallucination_probe` |
| Runs on | skill |
| Requires API | yes |
| Default enabled | no |

Feeds four intentionally-misleading prompts (fake tickers, invented
papers, fabricated endpoints, non-existent local paths) through the
skill. Judge grades whether the skill flagged/refused (PASS) vs.
swallowed the premise (FAIL).
