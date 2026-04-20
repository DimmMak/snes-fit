# .auto-test scorecard — blue-hill-capital

**Overall score:** 76/100  |  **Grade:** C
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
| 07_structural | 0.00 | 4 | FAIL |
| 08_design_audit | 0.50 | 4 | FAIL |

## Findings

### Critical (1)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 07_structural | SKILL.md missing | /Users/danny/Desktop/CLAUDE CODE/blue-hill-capital |

### Major (2)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 08_design_audit | Missing design doc: ARCHITECTURE.md | /Users/danny/Desktop/CLAUDE CODE/blue-hill-capital/ARCHITECTURE.md |
| 08_design_audit | Missing design doc: SCHEMA.md | /Users/danny/Desktop/CLAUDE CODE/blue-hill-capital/SCHEMA.md |

### Minor (2)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 08_design_audit | No NON_GOALS.md and no 'Non-goals' section in SKILL.md | /Users/danny/Desktop/CLAUDE CODE/blue-hill-capital |
| 08_design_audit | No schema_version field found in any config/*.json or logs/*.jsonl | /Users/danny/Desktop/CLAUDE CODE/blue-hill-capital |

### Cosmetic (3)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 07_structural | Non-canonical top-level subdir: meetings | /Users/danny/Desktop/CLAUDE CODE/blue-hill-capital/meetings |
| 07_structural | Non-canonical top-level subdir: reviews | /Users/danny/Desktop/CLAUDE CODE/blue-hill-capital/reviews |
| 07_structural | Non-canonical top-level subdir: trades | /Users/danny/Desktop/CLAUDE CODE/blue-hill-capital/trades |

## Rounds

| 🟣 Round | 🟣 Structural | 🟣 Minor | 🟣 Cosmetic | 🟣 Markers | 🟣 Verdict |
|---|---|---|---|---|---|
| 1 | 3 | 2 | 3 | 1 | 🔴 DIRTY |

**Clean streak (trailing):** 0 rounds · **Ship gate:** 2 required · ⏳ IN PROGRESS
