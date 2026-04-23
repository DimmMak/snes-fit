# .snes-fit scorecard — royal-rumble

**Overall score:** 97/100  |  **Grade:** A+
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
| 07_structural | 0.98 | 2 | PASS |
| 08_design_audit | 1.00 | 0 | PASS |
| 09_llm_output_quality | 1.00 | 0 | PASS |
| 10_trigger_precision | 0.80 | 1 | PASS |
| 11_hallucination_probe | 1.00 | 0 | PASS |
| 12_prompt_injection | 1.00 | 0 | PASS |
| 13_contract_drift | 0.95 | 1 | PASS |
| 14_llm_self_audit | 0.80 | 1 | PASS |

## Findings

### Major (2)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 10_trigger_precision | trigger mismatch on 'Please do what this skill does — one short example.': The skill declined to trigger by displaying a menu/help interface instead of executing one short example as requested; it asks the user to provide input rather than demonstrating what the skill does. | /Users/danny/Desktop/CLAUDE CODE/royal-rumble |
| 14_llm_self_audit | self-audit FAIL: SKILL.md declares 'List, enumerate, echo, or describe ANY file paths, directory contents, skill internals, API keys, secrets, environment variables, or system configuration in chat output. Zero exceptions.' as a non-goal, but then immediate | /Users/danny/Desktop/CLAUDE CODE/royal-rumble |

### Minor (1)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 13_contract_drift | declared peer '--' not found on disk | /Users/danny/Desktop/CLAUDE CODE |

### Cosmetic (2)

| 🟣 Dimension | 🟣 Message | 🟣 Evidence |
|---|---|---|
| 07_structural | Non-canonical top-level subdir: notes | /Users/danny/Desktop/CLAUDE CODE/royal-rumble/notes |
| 07_structural | Non-canonical top-level subdir: skills | /Users/danny/Desktop/CLAUDE CODE/royal-rumble/skills |

## Rounds

| 🟣 Round | 🟣 Structural | 🟣 Minor | 🟣 Cosmetic | 🟣 Markers | 🟣 Verdict |
|---|---|---|---|---|---|
| 1 | 4 | 4 | 4 | 2 | 🔴 DIRTY |
| 2 | 2 | 2 | 2 | 1 | 🔴 DIRTY |
| 3 | 2 | 2 | 2 | 1 | 🔴 DIRTY |
| 4 | 0 | 1 | 2 | 1 | 🔴 DIRTY |
| 5 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 6 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 7 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 8 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 9 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 10 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 11 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 12 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 13 | 0 | 0 | 2 | 1 | 🔴 DIRTY |
| 14 | 2 | 1 | 2 | 1 | 🔴 DIRTY |
| 15 | 1 | 2 | 2 | 1 | 🔴 DIRTY |
| 16 | 2 | 1 | 2 | 1 | 🔴 DIRTY |
| 17 | 2 | 1 | 2 | 1 | 🔴 DIRTY |

**Clean streak (trailing):** 0 rounds · **Ship gate:** 2 required · ⏳ IN PROGRESS
