---
name: snes-fit
domain: general
version: 0.2.2
description: >
  Fleet-wide QA skill that audits any other skill against structural, adversarial, scale, composition, security, threat-intel, type, and design dimensions. Plugin architecture lets you add dimensions as separate dirs — no core code changes. Ship only when decay rule hits 2 consecutive zero-finding rounds. Compatible with Anthropic skill-creator eval schemas. NOT for: creating new skills (use snes-builder). NOT for: running skills (use the skill directly). NOT for: continuous background monitoring (use scheduled-tasks).
capabilities:
  reads:
    - "any skill's SKILL.md + scripts/ + config/"
    - config/*.json
    - dimensions/*/plugin.py
    - vault/**
  writes:
    - vault/<skill>/*.jsonl (append only)
    - reports/<date>-<skill>.md
  calls: []  # phase 2 adds: anthropic SDK (sonnet + haiku)
  cannot:
    - modify the skill being audited
    - auto-push fixes
    - send data outside the local disk
    - bypass decay stopping rule
    - score below 0 or above 100
unix_contract:
  data_format: "JSONL + markdown"
  schema_version: "0.1"
  stdin_support: true
  stdout_format: "markdown scorecard"
  composable_with:
    - snes-builder
    - future-proof
    - mewtwo
    - home
---

# .snes-fit — Fleet-Wide QA Skill

## Purpose

Runs 8 pure-Python dimensions against any skill in the fleet. Binary PASS/FAIL/UNKNOWN verdicts; aggregated into a letter grade; ship gated by the decay stopping rule (≤1 cosmetic + 0 structural/major findings for 2 consecutive rounds).

Phase 1 is stdlib-only. No Claude API key required. Phase 2 adds LLM-backed dimensions (executor + judge).

snes-fit is the structural-conformance auditor of the fleet — it grades skills against `SPEC.md`. Use `.forensic` for editorial / quality critique on artifacts; use snes-fit for spec-compliance.

## When to trigger

Fires when the user invokes any of:
- `.snes-fit audit --skill <name>` / `.snes-fit audit --all`
- `.snes-fit design-audit --skill <name>`
- `.snes-fit create --skill <name>` / `.snes-fit improve` / `.snes-fit benchmark`
- Natural-language phrasings: "snes-fit this", "audit skill X for spec compliance", "run the fleet QA on X", "score skill X", "grade skill X against spec", "is X ship-ready?", "check fleet conformance"
- Any request to verify a skill's frontmatter, required sections, forbidden patterns, or canonical subdirectories against SPEC.md
- Self-audit: `.snes-fit audit --skill snes-fit` (the auditor must audit itself; see `dimensions/00_self/`)

## When NOT to trigger

- **Editorial / logical / quality critique on an artifact** — that's `.forensic`. snes-fit is structural; forensic is mechanism-and-quote.
- **Creating a new skill from scratch** — that's `snes-builder`. snes-fit grades; it does not author.
- **Running a skill** — that's the skill itself. snes-fit is a meta-tool; calling it does not invoke the audited skill.
- **Continuous background monitoring** — use `scheduled-tasks` to trigger snes-fit on a cadence; snes-fit itself is one-shot.
- **Cross-skill code execution / orchestration** — that's `mewtwo`. snes-fit reads source files; it does not run them.
- **Live model comparisons or A/B prompt evaluation** — out of scope (NON_GOALS.md #6).

## Anti-patterns

- **Audit drift** — running snes-fit, finding zero issues, declaring victory. The decay rule requires **2 consecutive zero-finding rounds**, not one. Single-pass green is not ship-ready.
- **Self-audit skip** — auditing every skill except snes-fit itself. If the auditor doesn't pass its own bar, every grade it emits is suspect. Run `audit --skill snes-fit` before any fleet sweep.
- **Severity inflation** — tagging every minor finding as "critical" to force attention. Severity tiers are critical / major / minor / cosmetic per SPEC.md:108-115. Do not invent tiers.
- **Score gaming** — exempting unfavorable findings via private skip-list. SPEC.md is the single source of truth; any exemption must be a SPEC.md edit + version bump, not a config-file workaround.
- **Compatibility theater** — claiming "Anthropic skill-creator eval schemas" compatibility without a pinned schema version + test. Pin the version; commit the test.
- **Composability claim without bilateral check** — declaring `composable_with: mewtwo` in frontmatter without verifying mewtwo's contract accepts snes-fit as a caller. Mewtwo refuses skills lacking contract declarations.

## Exit conditions

- **Audit complete** — scorecard emitted to `reports/<date>-<skill>.md`, findings to `vault/<skill>/findings.jsonl`, decay state updated. Skill done for this round.
- **Decay rule satisfied** — 2 consecutive rounds with ≤1 cosmetic + 0 structural/major. Ship gate opens. Skill done.
- **Critical finding** — block the round, surface to user, exit. Critical = broken or dangerous (per SPEC.md:111). Cannot ship past critical.
- **Self-audit failure** — if `audit --skill snes-fit` produces critical findings, snes-fit refuses to fleet-sweep until self-audit clears. The auditor must clear its own bar first.

---

## Subcommands

| 🟣 Command | 🟣 Mode | 🟣 What it does | 🟣 Writes |
|---|---|---|---|
| `.snes-fit audit --skill <name>` | Eval | Runs all enabled dims, prints scorecard | `vault/<skill>/findings.jsonl`, `reports/<date>-<skill>.md` |
| `.snes-fit audit --all` | Eval | Fleet sweep — all skills under `~/Desktop/CLAUDE CODE/` | per-skill vault + one summary report |
| `.snes-fit design-audit --skill <name>` | DesignAudit | Runs ONLY dimension 08 — fast structural/design check | `vault/<skill>/findings.jsonl` |
| `.snes-fit create --skill <name>` | Create | Scaffolds `evals/<skill>/evals.json` (Anthropic-compatible) | `evals/<skill>/evals.json` |
| `.snes-fit improve --skill <name>` | Improve | Phase-1 stub; phase-2 LLM fix engine | — |
| `.snes-fit benchmark --skill <name>` | Benchmark | Rolling baseline; delta vs previous run | `vault/<skill>/benchmark.jsonl` |

---

## 4-mode lifecycle

| 🟣 Mode | 🟣 Input | 🟣 Output | 🟣 Purpose |
|---|---|---|---|
| Create | skill name | `evals.json` scaffold | Seed an eval suite |
| Eval | skill + evals | scorecard + findings | Run once; grade it |
| Improve | findings | fix proposals (phase 2) | Close the loop |
| Benchmark | skill + history | delta report | Track drift over time |

Plus two always-on gates: **Audit** (all dims) and **DesignAudit** (dim 08 only).

---

## Decay stopping rule

Per `principle_stress_test_cadence` — ship only when findings decay to **≤1 cosmetic + 0 structural for 2 consecutive rounds**. Each round = one full audit pass with fixes in between. The decay tracker in `scripts/lib/decay_tracker.py` enforces this automatically; no bypass.

---

## Plugin tree

Every dimension is its own dir under `dimensions/`. Drop in `dimensions/NN_name/plugin.py` with a `DimensionPlugin` subclass and it gets auto-discovered. No core code touched.

See `ARCHITECTURE.md` for the DimensionPlugin ABC, data flow, and phase roadmap. See `SCHEMA.md` for every file format. See `NON_GOALS.md` for what this skill will never do.
