# .snes-fit scorecard — dataflow-tutor

**Overall score:** 95/100  |  **Grade:** A+
**Ship-ready (decay rule):** NO

## Per-dimension results

| 🟣 Dimension | 🟣 Score | 🟣 Findings | 🟣 Verdict |
|---|---|---|---|
| 01_adversarial | 1.00 | 0 | PASS |
| 02_scale | 1.00 | 0 | PASS |
| 03_composition | 0.99 | 1 | PASS |
| 04_security | 1.00 | 0 | PASS |
| 05_threat_intel | 1.00 | 0 | PASS |
| 06_types | 1.00 | 0 | PASS |
| 07_structural | 0.98 | 2 | PASS |
| 08_design_audit | 0.50 | 4 | FAIL |
| 09_llm_output_quality | 1.00 | 0 | PASS |
| 10_trigger_precision | 1.00 | 0 | PASS |
| 11_hallucination_probe | 1.00 | 0 | PASS |
| 12_prompt_injection | 0.95 | 1 | PASS |
| 13_contract_drift | 1.00 | 0 | PASS |
| 14_llm_self_audit | 1.00 | 0 | PASS |

## Findings

### Major (2)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 08_design_audit | Missing design doc: ARCHITECTURE.md | /Users/danny/Desktop/CLAUDE CODE/dataflow-tutor/ARCHITECTURE.md |
| 08_design_audit | Missing design doc: SCHEMA.md | /Users/danny/Desktop/CLAUDE CODE/dataflow-tutor/SCHEMA.md |

### Minor (3)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 08_design_audit | No NON_GOALS.md and no 'Non-goals' section in SKILL.md | /Users/danny/Desktop/CLAUDE CODE/dataflow-tutor |
| 08_design_audit | No schema_version field found in any config/*.json or logs/*.jsonl | /Users/danny/Desktop/CLAUDE CODE/dataflow-tutor |
| 12_prompt_injection | prompt-injection probe skipped — running in mock mode (ANTHROPIC_API_KEY missing or AUTO_TEST_MOCK=1). Set ANTHROPIC_API_KEY to enable live probing. | /Users/danny/Desktop/CLAUDE CODE/dataflow-tutor |

### Cosmetic (3)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 03_composition | No composable_with list declared | /Users/danny/Desktop/CLAUDE CODE/dataflow-tutor/SKILL.md |
| 07_structural | Non-canonical top-level subdir: references | /Users/danny/Desktop/CLAUDE CODE/dataflow-tutor/references |
| 07_structural | Non-canonical top-level subdir: research | /Users/danny/Desktop/CLAUDE CODE/dataflow-tutor/research |

## Rounds

| 🟣 Round | 🟣 Structural | 🟣 Minor | 🟣 Cosmetic | 🟣 Markers | 🟣 Verdict |
|---|---|---|---|---|---|
| 1 | 4 | 6 | 6 | 2 | 🔴 DIRTY |
| 2 | 2 | 3 | 3 | 1 | 🔴 DIRTY |
| 3 | 2 | 3 | 3 | 1 | 🔴 DIRTY |
| 4 | 2 | 3 | 3 | 1 | 🔴 DIRTY |
| 5 | 2 | 3 | 3 | 1 | 🔴 DIRTY |
| 6 | 2 | 3 | 3 | 1 | 🔴 DIRTY |
| 7 | 2 | 3 | 3 | 1 | 🔴 DIRTY |
| 8 | 18 | 3 | 3 | 1 | 🔴 DIRTY |
| 9 | 18 | 3 | 3 | 1 | 🔴 DIRTY |
| 10 | 2 | 4 | 3 | 1 | 🔴 DIRTY |
| 11 | 2 | 4 | 3 | 1 | 🔴 DIRTY |
| 12 | 2 | 4 | 3 | 1 | 🔴 DIRTY |
| 13 | 2 | 4 | 3 | 1 | 🔴 DIRTY |
| 14 | 2 | 4 | 3 | 1 | 🔴 DIRTY |
| 15 | 2 | 3 | 3 | 1 | 🔴 DIRTY |
| 16 | 2 | 3 | 3 | 1 | 🔴 DIRTY |
| 17 | 2 | 3 | 3 | 1 | 🔴 DIRTY |
| 18 | 2 | 3 | 3 | 1 | 🔴 DIRTY |
| 19 | 2 | 3 | 3 | 1 | 🔴 DIRTY |
| 20 | 2 | 3 | 3 | 1 | 🔴 DIRTY |

**Clean streak (trailing):** 0 rounds · **Ship gate:** 2 required · ⏳ IN PROGRESS
