# .snes-fit scorecard — study-buddy

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
| 06_types | 1.00 | 0 | PASS |
| 07_structural | 0.99 | 1 | PASS |
| 08_design_audit | 0.50 | 4 | FAIL |
| 09_llm_output_quality | 1.00 | 0 | PASS |
| 10_trigger_precision | 1.00 | 0 | PASS |
| 11_hallucination_probe | 1.00 | 0 | PASS |
| 12_prompt_injection | 0.95 | 1 | PASS |
| 13_contract_drift | 0.90 | 2 | PASS |
| 14_llm_self_audit | 1.00 | 0 | PASS |

## Findings

### Major (2)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 08_design_audit | Missing design doc: ARCHITECTURE.md | /Users/danny/Desktop/CLAUDE CODE/study-buddy/ARCHITECTURE.md |
| 08_design_audit | Missing design doc: SCHEMA.md | /Users/danny/Desktop/CLAUDE CODE/study-buddy/SCHEMA.md |

### Minor (5)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 08_design_audit | No NON_GOALS.md and no 'Non-goals' section in SKILL.md | /Users/danny/Desktop/CLAUDE CODE/study-buddy |
| 08_design_audit | No schema_version field found in any config/*.json or logs/*.jsonl | /Users/danny/Desktop/CLAUDE CODE/study-buddy |
| 12_prompt_injection | prompt-injection probe skipped — running in mock mode (ANTHROPIC_API_KEY missing or AUTO_TEST_MOCK=1). Set ANTHROPIC_API_KEY to enable live probing. | /Users/danny/Desktop/CLAUDE CODE/study-buddy |
| 13_contract_drift | declared peer 'courserafied' not found on disk | /Users/danny/Desktop/CLAUDE CODE |
| 13_contract_drift | declared peer '--' not found on disk | /Users/danny/Desktop/CLAUDE CODE |

### Cosmetic (1)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 07_structural | Non-canonical top-level subdir: tampermonkey | /Users/danny/Desktop/CLAUDE CODE/study-buddy/tampermonkey |

## Rounds

| 🟣 Round | 🟣 Structural | 🟣 Minor | 🟣 Cosmetic | 🟣 Markers | 🟣 Verdict |
|---|---|---|---|---|---|
| 1 | 4 | 4 | 4 | 2 | 🔴 DIRTY |
| 2 | 2 | 2 | 2 | 1 | 🔴 DIRTY |
| 3 | 2 | 2 | 2 | 1 | 🔴 DIRTY |
| 4 | 2 | 2 | 2 | 1 | 🔴 DIRTY |
| 5 | 2 | 2 | 2 | 1 | 🔴 DIRTY |
| 6 | 2 | 2 | 2 | 1 | 🔴 DIRTY |
| 7 | 2 | 2 | 2 | 1 | 🔴 DIRTY |
| 8 | 18 | 4 | 2 | 1 | 🔴 DIRTY |
| 9 | 18 | 4 | 2 | 1 | 🔴 DIRTY |
| 10 | 18 | 4 | 2 | 1 | 🔴 DIRTY |
| 11 | 18 | 4 | 2 | 1 | 🔴 DIRTY |
| 12 | 18 | 4 | 2 | 1 | 🔴 DIRTY |
| 13 | 18 | 4 | 2 | 1 | 🔴 DIRTY |
| 14 | 18 | 4 | 2 | 1 | 🔴 DIRTY |
| 15 | 18 | 4 | 1 | 1 | 🔴 DIRTY |
| 16 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 17 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 18 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 19 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 20 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 21 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 22 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 23 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 24 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 25 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 26 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 27 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 28 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 29 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 30 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 31 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 32 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 33 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 34 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 35 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 36 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 37 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 38 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 39 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 40 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 41 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 42 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 43 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 44 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 45 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 46 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 47 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 48 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 49 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 50 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 51 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 52 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 53 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 54 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 55 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 56 | 2 | 5 | 1 | 1 | 🔴 DIRTY |
| 57 | 2 | 5 | 1 | 1 | 🔴 DIRTY |

**Clean streak (trailing):** 0 rounds · **Ship gate:** 2 required · ⏳ IN PROGRESS
