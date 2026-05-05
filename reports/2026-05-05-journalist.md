# .snes-fit scorecard — journalist

**Overall score:** 91/100  |  **Grade:** A
**Ship-ready (decay rule):** NO

## Per-dimension results

| 🟣 Dimension | 🟣 Score | 🟣 Findings | 🟣 Verdict |
|---|---|---|---|
| 01_adversarial | 1.00 | 0 | PASS |
| 02_scale | 1.00 | 0 | PASS |
| 03_composition | 1.00 | 0 | PASS |
| 04_security | 1.00 | 0 | PASS |
| 05_threat_intel | 1.00 | 0 | PASS |
| 06_types | 1.00 | 0 | PASS |
| 07_structural | 1.00 | 0 | PASS |
| 08_design_audit | 0.50 | 4 | FAIL |
| 09_llm_output_quality | 0.80 | 1 | PASS |
| 10_trigger_precision | 1.00 | 0 | PASS |
| 11_hallucination_probe | 1.00 | 0 | PASS |
| 12_prompt_injection | 0.95 | 1 | PASS |
| 13_contract_drift | 0.70 | 3 | FAIL |
| 14_llm_self_audit | 0.80 | 1 | PASS |

## Findings

### Major (5)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 08_design_audit | Missing design doc: ARCHITECTURE.md | /Users/danny/Desktop/CLAUDE CODE/journalist/ARCHITECTURE.md |
| 08_design_audit | Missing design doc: SCHEMA.md | /Users/danny/Desktop/CLAUDE CODE/journalist/SCHEMA.md |
| 09_llm_output_quality | judge verdict FAIL: [mock] deterministic response for testing | /Users/danny/Desktop/CLAUDE CODE/journalist |
| 13_contract_drift | contract drift with 'royal-rumble': [mock] deterministic response for testing | /Users/danny/Desktop/CLAUDE CODE/journalist |
| 14_llm_self_audit | self-audit FAIL: [mock] deterministic response for testing | /Users/danny/Desktop/CLAUDE CODE/journalist |

### Minor (5)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 08_design_audit | No NON_GOALS.md and no 'Non-goals' section in SKILL.md | /Users/danny/Desktop/CLAUDE CODE/journalist |
| 08_design_audit | No schema_version field found in any config/*.json or logs/*.jsonl | /Users/danny/Desktop/CLAUDE CODE/journalist |
| 12_prompt_injection | prompt-injection probe skipped — running in mock mode (ANTHROPIC_API_KEY missing or AUTO_TEST_MOCK=1). Set ANTHROPIC_API_KEY to enable live probing. | /Users/danny/Desktop/CLAUDE CODE/journalist |
| 13_contract_drift | declared peer 'accuracy-tracker' not found on disk | /Users/danny/Desktop/CLAUDE CODE |
| 13_contract_drift | declared peer '--' not found on disk | /Users/danny/Desktop/CLAUDE CODE |

## Rounds

| 🟣 Round | 🟣 Structural | 🟣 Minor | 🟣 Cosmetic | 🟣 Markers | 🟣 Verdict |
|---|---|---|---|---|---|
| 1 | 4 | 4 | 0 | 2 | 🔴 DIRTY |
| 2 | 2 | 2 | 0 | 1 | 🔴 DIRTY |
| 3 | 2 | 2 | 0 | 1 | 🔴 DIRTY |
| 4 | 2 | 2 | 0 | 1 | 🔴 DIRTY |
| 5 | 2 | 2 | 0 | 1 | 🔴 DIRTY |
| 6 | 2 | 2 | 0 | 1 | 🔴 DIRTY |
| 7 | 2 | 2 | 0 | 1 | 🔴 DIRTY |
| 8 | 21 | 4 | 0 | 1 | 🔴 DIRTY |
| 9 | 21 | 4 | 0 | 1 | 🔴 DIRTY |
| 10 | 21 | 4 | 0 | 1 | 🔴 DIRTY |
| 11 | 21 | 4 | 0 | 1 | 🔴 DIRTY |
| 12 | 21 | 4 | 0 | 1 | 🔴 DIRTY |
| 13 | 21 | 4 | 0 | 1 | 🔴 DIRTY |
| 14 | 21 | 4 | 0 | 1 | 🔴 DIRTY |
| 15 | 21 | 4 | 0 | 1 | 🔴 DIRTY |
| 16 | 5 | 5 | 0 | 1 | 🔴 DIRTY |
| 17 | 5 | 5 | 0 | 1 | 🔴 DIRTY |
| 18 | 5 | 5 | 0 | 1 | 🔴 DIRTY |
| 19 | 5 | 5 | 0 | 1 | 🔴 DIRTY |
| 20 | 5 | 5 | 0 | 1 | 🔴 DIRTY |
| 21 | 5 | 5 | 0 | 1 | 🔴 DIRTY |
| 22 | 5 | 5 | 0 | 1 | 🔴 DIRTY |
| 23 | 5 | 5 | 0 | 1 | 🔴 DIRTY |
| 24 | 5 | 5 | 0 | 1 | 🔴 DIRTY |
| 25 | 5 | 5 | 0 | 1 | 🔴 DIRTY |
| 26 | 5 | 5 | 0 | 1 | 🔴 DIRTY |
| 27 | 5 | 5 | 0 | 1 | 🔴 DIRTY |

**Clean streak (trailing):** 0 rounds · **Ship gate:** 2 required · ⏳ IN PROGRESS
