# .snes-fit scorecard — kleppmann

**Overall score:** 99/100  |  **Grade:** A+
**Ship-ready (decay rule):** YES

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
| 13_contract_drift | 0.90 | 2 | PASS |
| 14_llm_self_audit | 1.00 | 0 | PASS |

## Findings

### Minor (3)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 12_prompt_injection | prompt-injection probe skipped — running in mock mode (ANTHROPIC_API_KEY missing or AUTO_TEST_MOCK=1). Set ANTHROPIC_API_KEY to enable live probing. | /Users/danny/Desktop/CLAUDE CODE/kleppmann |
| 13_contract_drift | declared peer 'courserafied' not found on disk | /Users/danny/Desktop/CLAUDE CODE |
| 13_contract_drift | declared peer '--' not found on disk | /Users/danny/Desktop/CLAUDE CODE |

## Rounds

| 🟣 Round | 🟣 Structural | 🟣 Minor | 🟣 Cosmetic | 🟣 Markers | 🟣 Verdict |
|---|---|---|---|---|---|
| 1 | 4 | 2 | 0 | 1 | 🔴 DIRTY |
| 2 | 4 | 2 | 0 | 1 | 🔴 DIRTY |
| 3 | 4 | 2 | 0 | 1 | 🔴 DIRTY |
| 4 | 0 | 0 | 0 | 1 | 🟢 CLEAN |
| 5 | 16 | 2 | 0 | 1 | 🔴 DIRTY |
| 6 | 16 | 2 | 0 | 1 | 🔴 DIRTY |
| 7 | 16 | 2 | 0 | 1 | 🔴 DIRTY |
| 8 | 16 | 2 | 0 | 1 | 🔴 DIRTY |
| 9 | 16 | 2 | 0 | 1 | 🔴 DIRTY |
| 10 | 16 | 2 | 0 | 1 | 🔴 DIRTY |
| 11 | 16 | 2 | 0 | 1 | 🔴 DIRTY |
| 12 | 16 | 2 | 0 | 1 | 🔴 DIRTY |
| 13 | 0 | 3 | 0 | 1 | 🟢 CLEAN |
| 14 | 0 | 3 | 0 | 1 | 🟢 CLEAN |
| 15 | 0 | 3 | 0 | 1 | 🟢 CLEAN |
| 16 | 0 | 3 | 0 | 1 | 🟢 CLEAN |
| 17 | 0 | 3 | 0 | 1 | 🟢 CLEAN |

**Clean streak (trailing):** 5 rounds · **Ship gate:** 2 required · ✅ PASSED
