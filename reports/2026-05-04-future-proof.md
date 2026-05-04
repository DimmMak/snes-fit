# .snes-fit scorecard — future-proof

**Overall score:** 95/100  |  **Grade:** A+
**Ship-ready (decay rule):** NO

## Per-dimension results

| 🟣 Dimension | 🟣 Score | 🟣 Findings | 🟣 Verdict |
|---|---|---|---|
| 01_adversarial | 0.95 | 1 | PASS |
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
| 08_design_audit | Missing design doc: ARCHITECTURE.md | /Users/danny/Desktop/CLAUDE CODE/future-proof/ARCHITECTURE.md |
| 08_design_audit | Missing design doc: SCHEMA.md | /Users/danny/Desktop/CLAUDE CODE/future-proof/SCHEMA.md |

### Minor (6)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 01_adversarial | unguarded sys.argv indexing (no len-check or argparse) | /Users/danny/Desktop/CLAUDE CODE/future-proof/scripts/validate-skill.py:156 |
| 06_types | Type-hint coverage 0% (< 50% threshold) | /Users/danny/Desktop/CLAUDE CODE/future-proof/scripts/ — 0/25 functions annotated |
| 08_design_audit | No NON_GOALS.md and no 'Non-goals' section in SKILL.md | /Users/danny/Desktop/CLAUDE CODE/future-proof |
| 08_design_audit | No schema_version field found in any config/*.json or logs/*.jsonl | /Users/danny/Desktop/CLAUDE CODE/future-proof |
| 12_prompt_injection | prompt-injection probe skipped — running in mock mode (ANTHROPIC_API_KEY missing or AUTO_TEST_MOCK=1). Set ANTHROPIC_API_KEY to enable live probing. | /Users/danny/Desktop/CLAUDE CODE/future-proof |
| 13_contract_drift | declared peer '--' not found on disk | /Users/danny/Desktop/CLAUDE CODE |

## Rounds

| 🟣 Round | 🟣 Structural | 🟣 Minor | 🟣 Cosmetic | 🟣 Markers | 🟣 Verdict |
|---|---|---|---|---|---|
| 1 | 4 | 8 | 0 | 2 | 🔴 DIRTY |
| 2 | 2 | 4 | 0 | 1 | 🔴 DIRTY |
| 3 | 2 | 4 | 0 | 1 | 🔴 DIRTY |
| 4 | 2 | 4 | 0 | 1 | 🔴 DIRTY |
| 5 | 2 | 4 | 0 | 1 | 🔴 DIRTY |
| 6 | 2 | 4 | 0 | 1 | 🔴 DIRTY |
| 7 | 2 | 4 | 0 | 1 | 🔴 DIRTY |
| 8 | 18 | 5 | 0 | 1 | 🔴 DIRTY |
| 9 | 18 | 5 | 0 | 1 | 🔴 DIRTY |
| 10 | 18 | 5 | 0 | 1 | 🔴 DIRTY |
| 11 | 18 | 5 | 0 | 1 | 🔴 DIRTY |
| 12 | 18 | 5 | 0 | 1 | 🔴 DIRTY |
| 13 | 18 | 5 | 0 | 1 | 🔴 DIRTY |
| 14 | 18 | 5 | 0 | 1 | 🔴 DIRTY |
| 15 | 18 | 5 | 0 | 1 | 🔴 DIRTY |
| 16 | 2 | 6 | 0 | 1 | 🔴 DIRTY |
| 17 | 2 | 6 | 0 | 1 | 🔴 DIRTY |
| 18 | 2 | 6 | 0 | 1 | 🔴 DIRTY |
| 19 | 2 | 6 | 0 | 1 | 🔴 DIRTY |
| 20 | 2 | 6 | 0 | 1 | 🔴 DIRTY |
| 21 | 2 | 6 | 0 | 1 | 🔴 DIRTY |
| 22 | 2 | 6 | 0 | 1 | 🔴 DIRTY |
| 23 | 2 | 6 | 0 | 1 | 🔴 DIRTY |
| 24 | 2 | 6 | 0 | 1 | 🔴 DIRTY |
| 25 | 2 | 6 | 0 | 1 | 🔴 DIRTY |

**Clean streak (trailing):** 0 rounds · **Ship gate:** 2 required · ⏳ IN PROGRESS
