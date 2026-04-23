# .snes-fit — Architecture

## Why this exists

Danny's fleet now has 25+ skills. Without automated QA, drift is invisible: a skill that was world-class at v0.1 silently rots as its dependencies change, its schema ages, and new sibling skills import its internals.

`.snes-fit` operationalizes `principle_stress_test_cadence` from Danny's memory:

> Every new skill / feature / refactor fires the battery: adversarial → scale → composition → security → threat-intel. Ship only when bug-rate decays to ≤1 cosmetic / 0 structural for two rounds.

That principle used to be manual. `.snes-fit` makes it a one-command pass.

---

## 4-mode lifecycle

```
                         ┌──────────────┐
              ┌─────────>│   Create     │  scaffold evals/<skill>/evals.json
              │          └──────┬───────┘
              │                 │
              │                 v
      (new skill)         ┌──────────────┐
                          │   Eval       │  run all dims → scorecard
                          └──────┬───────┘
                                 │
                         ┌───────┴────────┐
                         v                v
                   ┌──────────┐    ┌──────────────┐
                   │ Improve  │    │  Benchmark   │  delta vs previous
                   └────┬─────┘    └──────┬───────┘
                        │                 │
                        └────────┬────────┘
                                 v
                           (next round)
```

Two always-on gates sit alongside the lifecycle:

- **Audit** — runs every enabled dim (the default entry point)
- **DesignAudit** — runs ONLY dim 08 (fast doc-presence check; good for CI)

---

## Plugin contract

All dimensions subclass `DimensionPlugin` in `dimensions/_plugin_base.py`:

```python
class DimensionPlugin(ABC):
    name: str
    version: str
    runs_on: str  # "skill" | "file" | "fleet"

    @abstractmethod
    def probe(self, target) -> list[Finding]: ...

    def score(self, findings: list[Finding]) -> float: ...

    def regression_tests(self) -> list[dict]:
        return []
```

`probe()` returns `Finding` objects; `score()` has a default implementation (critical → 0.0, -0.2 per major, -0.05 per minor); `regression_tests()` is optional and returns tests to pin in the vault so a fixed bug can never recur.

---

## Data flow

```
 skill/         ─────> tree_walker.py  ────> SkillInfo
                                              │
 dimensions/*/plugin.py ─> plugin_loader ─> [Plugin, Plugin, ...]
                                              │
                                              v
                                       for each plugin:
                                         probe(skill) -> findings
                                         score(findings) -> 0.0-1.0
                                              │
                                              v
                                      scorecard.calculate_score()
                                              │
                              ┌───────────────┼───────────────┐
                              v                               v
                     reports/<date>-<skill>.md     vault/<skill>/findings.jsonl
                     (markdown, one per run)      (append-only, monotonic)
                                                         │
                                                         v
                                               decay_tracker.is_ship_ready()
```

---

## Decay tracker

`scripts/lib/decay_tracker.py` reads `vault/<skill>/findings.jsonl`, groups findings by `round`, applies the stopping rule:

- a round is **clean** if it has 0 structural + ≤1 cosmetic finding (informational markers don't count)
- ship when `clean_streak()` ≥ N (default 2) AND the overall score clears `ship_score_threshold` (default 80)

Public helpers:

| 🟣 Function | 🟣 Returns | 🟣 Used by |
|---|---|---|
| `summarize_rounds(by_round)` | `List[RoundSummary]` — per-round structural/minor/cosmetic/marker counts + clean flag | report renderer's `## Rounds` table |
| `clean_streak(summaries)` | `int` trailing consecutive clean rounds | ship-ready check |
| `next_round_id(by_round)` | `max(rounds) + 1` or `1` if empty | CLI auto-increment (prevents round-1 stacking) |
| `is_ship_ready(by_round, N)` | legacy `bool` wrapper | tests, back-compat |

Rounds monotonically increase; never rewritten. The vault is the audit trail. The renderer emits a self-describing per-round table (🟢 CLEAN / 🔴 DIRTY per row) — the compact sparkline used in 0.2.0 was deleted because aggregate counts were easy to misread as round counts.

---

## Anthropic schema compatibility

| 🟣 Anthropic file | 🟣 Our mapping | 🟣 Notes |
|---|---|---|
| `evals.json` | `evals/<skill>/evals.json` | Same shape: `{skill_name, evals: [...]}` |
| `grading.json` | `vault/<skill>/grading.json` | Per-eval PASS/FAIL/UNKNOWN + rationale |
| `benchmark.json` | `vault/<skill>/benchmark.jsonl` | We append rather than overwrite (auditable) |

Anthropic's skill-creator can consume our `evals.json` directly.

---

## Phase roadmap

| 🟣 Phase | 🟣 Contents | 🟣 Status |
|---|---|---|
| Phase 1 | Core infra + 8 pure-Python dims (01–08) | **This build** |
| Phase 2 | LLM-eval dims 09–14 (executor=sonnet-4-7, judge=haiku-4-5) | Planned |
| Phase 3 | Advanced dims 15–30 (property-based, mutation, fuzzing) | Planned |
| Phase 4 | Meta layers M1–M8 (cross-dim invariants, fleet-wide trend) | Planned |

---

## Half-life projection

Per the fleet's 3-axis architecture (tree + plugin + unix), each axis targets 99% annual survival:

```
0.99 × 0.99 × 0.99 ≈ 0.9703 → ~35-year half-life
```

Plugin tree means new dimensions don't touch the core. Unix contract (JSONL + markdown) means files are readable in any decade. Tree structure means no graph cycles to confuse future readers.

---

## Reading order for new contributors

1. `SKILL.md` — what it does, subcommands
2. `NON_GOALS.md` — what it refuses to do
3. `SCHEMA.md` — every file format
4. `ARCHITECTURE.md` (this file) — why the shape is the shape
5. `dimensions/_plugin_base.py` — the one contract that matters
