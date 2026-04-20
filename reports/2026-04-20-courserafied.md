# .auto-test scorecard — courserafied

**Overall score:** 92/100  |  **Grade:** A
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
| 07_structural | 0.96 | 4 | PASS |
| 08_design_audit | 0.50 | 4 | FAIL |

## Findings

### Major (2)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 08_design_audit | Missing design doc: ARCHITECTURE.md | /Users/danny/Desktop/CLAUDE CODE/courserafied/ARCHITECTURE.md |
| 08_design_audit | Missing design doc: SCHEMA.md | /Users/danny/Desktop/CLAUDE CODE/courserafied/SCHEMA.md |

### Minor (2)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 08_design_audit | No NON_GOALS.md and no 'Non-goals' section in SKILL.md | /Users/danny/Desktop/CLAUDE CODE/courserafied |
| 08_design_audit | No schema_version field found in any config/*.json or logs/*.jsonl | /Users/danny/Desktop/CLAUDE CODE/courserafied |

### Cosmetic (4)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 07_structural | Non-canonical top-level subdir: agents | /Users/danny/Desktop/CLAUDE CODE/courserafied/agents |
| 07_structural | Non-canonical top-level subdir: courses | /Users/danny/Desktop/CLAUDE CODE/courserafied/courses |
| 07_structural | Non-canonical top-level subdir: examples | /Users/danny/Desktop/CLAUDE CODE/courserafied/examples |
| 07_structural | Non-canonical top-level subdir: schemas | /Users/danny/Desktop/CLAUDE CODE/courserafied/schemas |

## Rounds

| 🟣 Round | 🟣 Structural | 🟣 Minor | 🟣 Cosmetic | 🟣 Markers | 🟣 Verdict |
|---|---|---|---|---|---|
| 1 | 4 | 4 | 8 | 2 | 🔴 DIRTY |
| 2 | 2 | 2 | 4 | 1 | 🔴 DIRTY |
| 3 | 2 | 2 | 4 | 1 | 🔴 DIRTY |

**Clean streak (trailing):** 0 rounds · **Ship gate:** 2 required · ⏳ IN PROGRESS
