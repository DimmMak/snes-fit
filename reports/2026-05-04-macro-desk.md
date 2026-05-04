# .snes-fit scorecard — macro-desk

**Overall score:** 95/100  |  **Grade:** A+
**Ship-ready (decay rule):** NO

## Per-dimension results

| 🟣 Dimension | 🟣 Score | 🟣 Findings | 🟣 Verdict |
|---|---|---|---|
| 01_adversarial | 1.00 | 0 | PASS |
| 02_scale | 1.00 | 0 | PASS |
| 03_composition | 1.00 | 0 | PASS |
| 04_security | 1.00 | 0 | PASS |
| 05_threat_intel | 1.00 | 0 | PASS |
| 06_types | 0.95 | 1 | PASS |
| 07_structural | 1.00 | 0 | PASS |
| 08_design_audit | 0.50 | 4 | FAIL |
| 09_llm_output_quality | 1.00 | 0 | PASS |
| 10_trigger_precision | 1.00 | 0 | PASS |
| 11_hallucination_probe | 1.00 | 0 | PASS |
| 12_prompt_injection | 0.95 | 1 | PASS |
| 13_contract_drift | 0.95 | 1 | PASS |
| 14_llm_self_audit | 1.00 | 0 | PASS |

## Findings

### Major (2)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 08_design_audit | Missing design doc: ARCHITECTURE.md | /Users/danny/Desktop/CLAUDE CODE/macro-desk/ARCHITECTURE.md |
| 08_design_audit | Missing design doc: SCHEMA.md | /Users/danny/Desktop/CLAUDE CODE/macro-desk/SCHEMA.md |

### Minor (5)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 06_types | Type-hint coverage 0% (< 50% threshold) | /Users/danny/Desktop/CLAUDE CODE/macro-desk/scripts/ — 0/5 functions annotated |
| 08_design_audit | No NON_GOALS.md and no 'Non-goals' section in SKILL.md | /Users/danny/Desktop/CLAUDE CODE/macro-desk |
| 08_design_audit | No schema_version field found in any config/*.json or logs/*.jsonl | /Users/danny/Desktop/CLAUDE CODE/macro-desk |
| 12_prompt_injection | prompt-injection probe skipped — running in mock mode (ANTHROPIC_API_KEY missing or AUTO_TEST_MOCK=1). Set ANTHROPIC_API_KEY to enable live probing. | /Users/danny/Desktop/CLAUDE CODE/macro-desk |
| 13_contract_drift | declared peer '--' not found on disk | /Users/danny/Desktop/CLAUDE CODE |

## Rounds

| 🟣 Round | 🟣 Structural | 🟣 Minor | 🟣 Cosmetic | 🟣 Markers | 🟣 Verdict |
|---|---|---|---|---|---|
| 1 | 2 | 3 | 0 | 1 | 🔴 DIRTY |
| 2 | 2 | 3 | 0 | 1 | 🔴 DIRTY |
| 3 | 18 | 4 | 0 | 1 | 🔴 DIRTY |
| 4 | 18 | 4 | 0 | 1 | 🔴 DIRTY |
| 5 | 18 | 4 | 0 | 1 | 🔴 DIRTY |
| 6 | 18 | 4 | 0 | 1 | 🔴 DIRTY |
| 7 | 18 | 4 | 0 | 1 | 🔴 DIRTY |
| 8 | 18 | 4 | 0 | 1 | 🔴 DIRTY |
| 9 | 18 | 4 | 0 | 1 | 🔴 DIRTY |
| 10 | 18 | 4 | 0 | 1 | 🔴 DIRTY |
| 11 | 2 | 5 | 0 | 1 | 🔴 DIRTY |
| 12 | 2 | 5 | 0 | 1 | 🔴 DIRTY |
| 13 | 2 | 5 | 0 | 1 | 🔴 DIRTY |
| 14 | 2 | 5 | 0 | 1 | 🔴 DIRTY |
| 15 | 2 | 5 | 0 | 1 | 🔴 DIRTY |
| 16 | 2 | 5 | 0 | 1 | 🔴 DIRTY |
| 17 | 2 | 5 | 0 | 1 | 🔴 DIRTY |
| 18 | 2 | 5 | 0 | 1 | 🔴 DIRTY |
| 19 | 2 | 5 | 0 | 1 | 🔴 DIRTY |
| 20 | 2 | 5 | 0 | 1 | 🔴 DIRTY |

**Clean streak (trailing):** 0 rounds · **Ship gate:** 2 required · ⏳ IN PROGRESS
