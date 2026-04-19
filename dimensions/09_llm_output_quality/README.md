# 09 — LLM output quality

| 🟣 Field | 🟣 Value |
|---|---|
| Dimension | `09_llm_output_quality` |
| Runs on | skill |
| Requires API | yes |
| Default enabled | no |

Runs a canned prompt through the skill (Sonnet executor), then asks
Haiku whether the resulting output matches SKILL.md's stated purpose.
Graceful UNKNOWN when no API key is present.
