# .auto-test scorecard — dataflow-tutor

**Overall score:** 92/100  |  **Grade:** A
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
| 08_design_audit | 0.45 | 5 | FAIL |

## Findings

### Major (2)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 08_design_audit | Missing design doc: ARCHITECTURE.md | /Users/danny/Desktop/CLAUDE CODE/dataflow-tutor/ARCHITECTURE.md |
| 08_design_audit | Missing design doc: SCHEMA.md | /Users/danny/Desktop/CLAUDE CODE/dataflow-tutor/SCHEMA.md |

### Minor (3)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 08_design_audit | Missing design doc: CHANGELOG.md | /Users/danny/Desktop/CLAUDE CODE/dataflow-tutor/CHANGELOG.md |
| 08_design_audit | No NON_GOALS.md and no 'Non-goals' section in SKILL.md | /Users/danny/Desktop/CLAUDE CODE/dataflow-tutor |
| 08_design_audit | No schema_version field found in any config/*.json or logs/*.jsonl | /Users/danny/Desktop/CLAUDE CODE/dataflow-tutor |

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

**Clean streak (trailing):** 0 rounds · **Ship gate:** 2 required · ⏳ IN PROGRESS
