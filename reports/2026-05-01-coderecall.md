# .snes-fit scorecard — coderecall

**Overall score:** 98/100  |  **Grade:** A+
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
| 07_structural | 0.92 | 4 | PASS |
| 08_design_audit | 0.95 | 1 | PASS |
| 09_llm_output_quality | 1.00 | 0 | PASS |
| 10_trigger_precision | 1.00 | 0 | PASS |
| 11_hallucination_probe | 1.00 | 0 | PASS |
| 12_prompt_injection | 0.95 | 1 | PASS |
| 13_contract_drift | 0.95 | 1 | PASS |
| 14_llm_self_audit | 1.00 | 0 | PASS |

## Findings

### Minor (4)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 07_structural | Tree depth 10 > 5 | /Users/danny/Desktop/CLAUDE CODE/coderecall |
| 08_design_audit | No schema_version field found in any config/*.json or logs/*.jsonl | /Users/danny/Desktop/CLAUDE CODE/coderecall |
| 12_prompt_injection | prompt-injection probe skipped — running in mock mode (ANTHROPIC_API_KEY missing or AUTO_TEST_MOCK=1). Set ANTHROPIC_API_KEY to enable live probing. | /Users/danny/Desktop/CLAUDE CODE/coderecall |
| 13_contract_drift | declared peer '--' not found on disk | /Users/danny/Desktop/CLAUDE CODE |

### Cosmetic (3)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 07_structural | Non-canonical top-level subdir: node_modules | /Users/danny/Desktop/CLAUDE CODE/coderecall/node_modules |
| 07_structural | Non-canonical top-level subdir: public | /Users/danny/Desktop/CLAUDE CODE/coderecall/public |
| 07_structural | Non-canonical top-level subdir: src | /Users/danny/Desktop/CLAUDE CODE/coderecall/src |

## Rounds

| 🟣 Round | 🟣 Structural | 🟣 Minor | 🟣 Cosmetic | 🟣 Markers | 🟣 Verdict |
|---|---|---|---|---|---|
| 1 | 62 | 54 | 44 | 3 | 🔴 DIRTY |
| 2 | 2 | 4 | 4 | 1 | 🔴 DIRTY |
| 3 | 2 | 4 | 4 | 1 | 🔴 DIRTY |
| 4 | 2 | 4 | 4 | 1 | 🔴 DIRTY |
| 5 | 2 | 4 | 4 | 1 | 🔴 DIRTY |
| 6 | 2 | 4 | 4 | 1 | 🔴 DIRTY |
| 7 | 2 | 4 | 4 | 1 | 🔴 DIRTY |
| 8 | 9 | 4 | 3 | 1 | 🔴 DIRTY |
| 9 | 16 | 3 | 3 | 1 | 🔴 DIRTY |
| 10 | 16 | 3 | 3 | 1 | 🔴 DIRTY |
| 11 | 0 | 4 | 3 | 1 | 🔴 DIRTY |
| 12 | 0 | 4 | 3 | 1 | 🔴 DIRTY |
| 13 | 0 | 4 | 3 | 1 | 🔴 DIRTY |
| 14 | 0 | 4 | 3 | 1 | 🔴 DIRTY |
| 15 | 0 | 4 | 3 | 1 | 🔴 DIRTY |

**Clean streak (trailing):** 0 rounds · **Ship gate:** 2 required · ⏳ IN PROGRESS
