# .snes-fit scorecard — royal-rumble

**Overall score:** 97/100  |  **Grade:** A+
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
| 08_design_audit | 1.00 | 0 | PASS |
| 09_llm_output_quality | 1.00 | 0 | PASS |
| 10_trigger_precision | 1.00 | 0 | PASS |
| 11_hallucination_probe | 1.00 | 0 | PASS |
| 12_prompt_injection | 0.95 | 1 | PASS |
| 13_contract_drift | 0.65 | 4 | FAIL |
| 14_llm_self_audit | 1.00 | 0 | PASS |

## Findings

### Major (1)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 13_contract_drift | contract drift with 'journalist': [mock] deterministic response for testing | /Users/danny/Desktop/CLAUDE CODE/royal-rumble |

### Minor (4)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 12_prompt_injection | prompt-injection probe skipped — running in mock mode (ANTHROPIC_API_KEY missing or AUTO_TEST_MOCK=1). Set ANTHROPIC_API_KEY to enable live probing. | /Users/danny/Desktop/CLAUDE CODE/royal-rumble |
| 13_contract_drift | declared peer 'accuracy-tracker' not found on disk | /Users/danny/Desktop/CLAUDE CODE |
| 13_contract_drift | declared peer 'chief-of-staff' not found on disk | /Users/danny/Desktop/CLAUDE CODE |
| 13_contract_drift | declared peer '--' not found on disk | /Users/danny/Desktop/CLAUDE CODE |

## Rounds

| 🟣 Round | 🟣 Structural | 🟣 Minor | 🟣 Cosmetic | 🟣 Markers | 🟣 Verdict |
|---|---|---|---|---|---|
| 1 | 4 | 4 | 4 | 2 | 🔴 DIRTY |
| 2 | 2 | 2 | 2 | 1 | 🔴 DIRTY |
| 3 | 2 | 2 | 2 | 1 | 🔴 DIRTY |
| 4 | 0 | 1 | 2 | 1 | 🔴 DIRTY |
| 5 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 6 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 7 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 8 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 9 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 10 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 11 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 12 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 13 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 14 | 2 | 1 | 2 | 1 | 🔴 DIRTY |
| 15 | 1 | 2 | 2 | 1 | 🔴 DIRTY |
| 16 | 2 | 1 | 2 | 1 | 🔴 DIRTY |
| 17 | 2 | 1 | 2 | 1 | 🔴 DIRTY |
| 18 | 17 | 3 | 3 | 1 | 🔴 DIRTY |
| 19 | 17 | 3 | 3 | 1 | 🔴 DIRTY |
| 20 | 17 | 3 | 3 | 1 | 🔴 DIRTY |
| 21 | 17 | 3 | 3 | 1 | 🔴 DIRTY |
| 22 | 17 | 3 | 3 | 1 | 🔴 DIRTY |
| 23 | 17 | 3 | 3 | 1 | 🔴 DIRTY |
| 24 | 17 | 3 | 0 | 1 | 🔴 DIRTY |
| 25 | 1 | 3 | 0 | 1 | 🔴 DIRTY |
| 26 | 17 | 3 | 0 | 1 | 🔴 DIRTY |
| 27 | 1 | 4 | 0 | 1 | 🔴 DIRTY |
| 28 | 1 | 4 | 0 | 1 | 🔴 DIRTY |
| 29 | 1 | 4 | 0 | 1 | 🔴 DIRTY |
| 30 | 1 | 4 | 0 | 1 | 🔴 DIRTY |
| 31 | 1 | 4 | 0 | 1 | 🔴 DIRTY |
| 32 | 1 | 4 | 0 | 1 | 🔴 DIRTY |
| 33 | 1 | 4 | 0 | 1 | 🔴 DIRTY |

**Clean streak (trailing):** 0 rounds · **Ship gate:** 2 required · ⏳ IN PROGRESS
