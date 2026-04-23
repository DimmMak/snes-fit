---
name: snes-fit
domain: general
version: 0.1.0
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

Runs 8 pure-Python dimensions against any skill in the fleet. Binary PASS/FAIL/UNKNOWN verdicts; aggregated into a letter grade; ship gated by the decay stopping rule (2 consecutive rounds of ≤1 cosmetic + 0 structural findings).

Phase 1 is stdlib-only. No Claude API key required. Phase 2 adds LLM-backed dimensions (executor + judge).

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
