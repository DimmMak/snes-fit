# .auto-test scorecard — promptlatro

**Overall score:** 93/100  |  **Grade:** A
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
| 07_structural | 1.00 | 0 | PASS |
| 08_design_audit | 0.50 | 4 | FAIL |

## Findings

### Major (2)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 08_design_audit | Missing design doc: ARCHITECTURE.md | /Users/danny/Desktop/CLAUDE CODE/promptlatro/ARCHITECTURE.md |
| 08_design_audit | Missing design doc: SCHEMA.md | /Users/danny/Desktop/CLAUDE CODE/promptlatro/SCHEMA.md |

### Minor (2)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 08_design_audit | No NON_GOALS.md and no 'Non-goals' section in SKILL.md | /Users/danny/Desktop/CLAUDE CODE/promptlatro |
| 08_design_audit | No schema_version field found in any config/*.json or logs/*.jsonl | /Users/danny/Desktop/CLAUDE CODE/promptlatro |

### Cosmetic (1)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 03_composition | No composable_with list declared | /Users/danny/Desktop/CLAUDE CODE/promptlatro/SKILL.md |

## Rounds

| 🟣 Round | 🟣 Structural | 🟣 Minor | 🟣 Cosmetic | 🟣 Markers | 🟣 Verdict |
|---|---|---|---|---|---|
| 1 | 4 | 4 | 2 | 2 | 🔴 DIRTY |
| 2 | 2 | 2 | 1 | 1 | 🔴 DIRTY |
| 3 | 2 | 2 | 1 | 1 | 🔴 DIRTY |
| 4 | 2 | 2 | 1 | 1 | 🔴 DIRTY |

**Clean streak (trailing):** 0 rounds · **Ship gate:** 2 required · ⏳ IN PROGRESS
