# .snes-fit — Data Contracts (SCHEMA.md)

Every file written or read by `.snes-fit` is defined here. Every schema carries an explicit `schema_version` field.

Current schema version: **0.1**

---

## config/thresholds.json

```json
{
  "schema_version": "0.1",
  "pass_rate_min": 0.8,
  "p0_max": 0,
  "decay_zero_rounds": 2,
  "max_parallel": 4,
  "ship_score_threshold": 80
}
```

| 🟣 Field | 🟣 Type | 🟣 Meaning |
|---|---|---|
| pass_rate_min | float 0.0–1.0 | Minimum per-dim pass rate to PASS |
| p0_max | int ≥ 0 | Max allowable critical findings |
| decay_zero_rounds | int ≥ 1 | Consecutive clean rounds required to ship |
| max_parallel | int ≥ 1 | Reserved; phase 1 runs serially |
| ship_score_threshold | int 0–100 | Aggregate grade threshold for ship |

Backward compat: future versions only ADD fields. Never remove or rename.

---

## config/dimensions.json

```json
{
  "schema_version": "0.1",
  "dimensions": [
    {"id": "01_adversarial",  "enabled": true, "runs_on": "skill", "weight": 1.0},
    {"id": "02_scale",        "enabled": true, "runs_on": "skill", "weight": 1.0},
    {"id": "03_composition",  "enabled": true, "runs_on": "skill", "weight": 1.0},
    {"id": "04_security",     "enabled": true, "runs_on": "skill", "weight": 1.5},
    {"id": "05_threat_intel", "enabled": true, "runs_on": "skill", "weight": 1.0},
    {"id": "06_types",        "enabled": true, "runs_on": "skill", "weight": 0.75},
    {"id": "07_structural",   "enabled": true, "runs_on": "skill", "weight": 1.5},
    {"id": "08_design_audit", "enabled": true, "runs_on": "skill", "weight": 1.25}
  ]
}
```

| 🟣 Field | 🟣 Type | 🟣 Meaning |
|---|---|---|
| id | string | Must match `dimensions/<id>/plugin.py` path |
| enabled | bool | If false, plugin loader skips it |
| runs_on | enum | `skill` \| `file` \| `fleet` |
| weight | float ≥ 0 | Contribution to weighted aggregate score |

---

## config/models.json

```json
{
  "schema_version": "0.1",
  "executor": "claude-sonnet-4-7",
  "judge": "claude-haiku-4-5",
  "phase": 1,
  "notes": "Unused in phase 1 — reserved for phase-2 LLM-backed dims"
}
```

---

## evals/<skill>/evals.json (Anthropic-compatible)

```json
{
  "schema_version": "0.1",
  "skill_name": "<skill>",
  "evals": [
    {
      "id": "eval_001",
      "prompt": "Invocation or task to run against the skill",
      "expected_output": "substring or regex the output must contain",
      "files": [],
      "expectations": ["exit_code=0", "contains:<text>"]
    }
  ]
}
```

| 🟣 Field | 🟣 Type | 🟣 Meaning |
|---|---|---|
| id | string | Unique eval ID within the skill |
| prompt | string | Input given to the executor |
| expected_output | string | Substring / regex judge checks for |
| files | string[] | Optional file fixtures |
| expectations | string[] | Extra pass/fail clauses |

Matches Anthropic skill-creator's `evals.json` shape so their tooling can consume ours verbatim.

---

## vault/<skill>/findings.jsonl (append-only)

One JSON object per line:

```json
{"schema_version":"0.1","timestamp_iso":"2026-04-19T12:00:00Z","round":1,"dimension":"07_structural","severity":"major","message":"Missing ARCHITECTURE.md","evidence":"/path/to/skill"}
```

| 🟣 Field | 🟣 Type | 🟣 Meaning |
|---|---|---|
| schema_version | string | Always present; enables future migrations |
| timestamp_iso | string (ISO-8601 UTC) | When the finding was recorded |
| round | int ≥ 1 | Decay-tracker round number |
| dimension | string | Matches a `dimensions/<id>/` dir |
| severity | enum | `critical` \| `major` \| `minor` \| `cosmetic` |
| message | string | Human-readable |
| evidence | string | Path or excerpt proving the finding |

**Append-only.** Never rewrite. Parse-tolerant — unreadable lines are skipped with a warning.

---

## vault/<skill>/grading.json (Anthropic-compatible)

```json
{
  "schema_version": "0.1",
  "skill_name": "<skill>",
  "run_id": "<iso-ts>",
  "overall_verdict": "PASS",
  "evals": [
    {"id": "eval_001", "verdict": "PASS", "rationale": "matched substring"}
  ]
}
```

`verdict` enum: `PASS` | `FAIL` | `UNKNOWN` (three values, locked).

---

## vault/<skill>/benchmark.jsonl

Append-only timeseries of per-run scores:

```json
{"schema_version":"0.1","timestamp_iso":"2026-04-19T12:00:00Z","run_id":"...","overall_score":84,"grade":"B+","per_dim":{"01_adversarial":1.0,"07_structural":0.8}}
```

---

## reports/<date>-<skill>.md

Human-readable markdown scorecard. Not machine-parsed — the vault is the canonical store.

Structure:

1. Header: skill name, run timestamp, overall grade + score, ship-ready verdict (yes/no)
2. Per-dimension table (🟣 headers)
3. Findings list grouped by severity
4. Rounds table — one row per round with explicit 🟢 CLEAN / 🔴 DIRTY verdict and structural/minor/cosmetic/marker columns
5. Clean-streak + ship-gate summary line (e.g. "Clean streak: 5 rounds · Ship gate: 2 required · ✅ PASSED")

---

## Version bumps

| 🟣 Rule | 🟣 Action |
|---|---|
| Add optional field | PATCH (0.1 → 0.1.1), no migration |
| Add required field | MINOR (0.1 → 0.2), writer must populate, reader tolerates absence |
| Rename / remove field | MAJOR (0.1 → 1.0), migration script required |

All readers MUST branch on `schema_version`. Unknown versions warn-and-continue.
