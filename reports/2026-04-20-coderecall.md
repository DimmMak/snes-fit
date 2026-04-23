# .auto-test scorecard — coderecall

**Overall score:** 91/100  |  **Grade:** A
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
| 07_structural | 0.92 | 4 | PASS |
| 08_design_audit | 0.45 | 5 | FAIL |

## Findings

### Major (2)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 08_design_audit | Missing design doc: ARCHITECTURE.md | /Users/danny/Desktop/CLAUDE CODE/coderecall/ARCHITECTURE.md |
| 08_design_audit | Missing design doc: SCHEMA.md | /Users/danny/Desktop/CLAUDE CODE/coderecall/SCHEMA.md |

### Minor (4)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 07_structural | Tree depth 10 > 5 | /Users/danny/Desktop/CLAUDE CODE/coderecall |
| 08_design_audit | Missing design doc: CHANGELOG.md | /Users/danny/Desktop/CLAUDE CODE/coderecall/CHANGELOG.md |
| 08_design_audit | No NON_GOALS.md and no 'Non-goals' section in SKILL.md | /Users/danny/Desktop/CLAUDE CODE/coderecall |
| 08_design_audit | No schema_version field found in any config/*.json or logs/*.jsonl | /Users/danny/Desktop/CLAUDE CODE/coderecall |

### Cosmetic (4)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 03_composition | No composable_with list declared | /Users/danny/Desktop/CLAUDE CODE/coderecall/SKILL.md |
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

**Clean streak (trailing):** 0 rounds · **Ship gate:** 2 required · ⏳ IN PROGRESS
