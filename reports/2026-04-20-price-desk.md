# .auto-test scorecard — price-desk

**Overall score:** 92/100  |  **Grade:** A
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

## Findings

### Major (2)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 08_design_audit | Missing design doc: ARCHITECTURE.md | /Users/danny/Desktop/CLAUDE CODE/price-desk/ARCHITECTURE.md |
| 08_design_audit | Missing design doc: SCHEMA.md | /Users/danny/Desktop/CLAUDE CODE/price-desk/SCHEMA.md |

### Minor (4)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 01_adversarial | unguarded sys.argv indexing (no len-check or argparse) | /Users/danny/Desktop/CLAUDE CODE/price-desk/scripts/price.py:255 |
| 06_types | Type-hint coverage 0% (< 50% threshold) | /Users/danny/Desktop/CLAUDE CODE/price-desk/scripts/ — 0/7 functions annotated |
| 08_design_audit | No NON_GOALS.md and no 'Non-goals' section in SKILL.md | /Users/danny/Desktop/CLAUDE CODE/price-desk |
| 08_design_audit | No schema_version field found in any config/*.json or logs/*.jsonl | /Users/danny/Desktop/CLAUDE CODE/price-desk |

## Rounds

| 🟣 Round | 🟣 Structural | 🟣 Minor | 🟣 Cosmetic | 🟣 Markers | 🟣 Verdict |
|---|---|---|---|---|---|
| 1 | 4 | 8 | 0 | 2 | 🔴 DIRTY |
| 2 | 2 | 4 | 0 | 1 | 🔴 DIRTY |
| 3 | 2 | 4 | 0 | 1 | 🔴 DIRTY |
| 4 | 2 | 4 | 0 | 1 | 🔴 DIRTY |

**Clean streak (trailing):** 0 rounds · **Ship gate:** 2 required · ⏳ IN PROGRESS
