# .auto-test — Non-Goals

What this skill will **never** do. Each entry is a structural commitment, not a preference.

| 🟣 # | 🟣 Non-goal | 🟣 Why |
|---|---|---|
| 1 | No web UI | Terminal-first; markdown scorecards stay readable in any editor for 50 years |
| 2 | No auto-fix / auto-commit | Findings propose; humans decide. Intern/Senior pattern |
| 3 | No continuous background monitoring | Use `scheduled-tasks` or `cron` to trigger runs — we are a one-shot tool |
| 4 | No skills ranking / gamification across users | Single-user tool; no leaderboards; no social layer |
| 5 | No cloud sync | All state stays on local disk under `vault/` |
| 6 | No model comparisons | We audit skills, not models. Model choice is out of scope |
| 7 | No replacement of pytest | We COMPOSE pytest (and unittest); we do not reimplement it |
| 8 | No per-user accounts | No auth, no sessions, no roles |
| 9 | No score below 0 or above 100 | Grade is clamped; overflow is a bug, not a feature |
| 10 | No bypass of decay rule | Ship gate is enforced in code, not in policy |
| 11 | No external network calls in phase 1 | Stdlib only; reproducible offline |
| 12 | No YAML / pickle / binary formats for state | JSON + JSONL + markdown only — human-readable forever |
| 13 | No modification of the skill being audited | Read-only probes; writes confined to `vault/` and `reports/` |
| 14 | No invented dimensions outside the declared set | Dimensions are versioned; new ones require a spec bump |

These are invariants. Changing any of them requires a MAJOR version bump and a migration plan.
