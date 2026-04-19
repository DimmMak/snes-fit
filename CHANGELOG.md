# Changelog

All notable changes to `.auto-test`.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [SemVer](https://semver.org/).

## [0.2.0] — 2026-04-19

### Added — phase 2: LLM-eval dimensions
- 6 new dimensions (all **opt-in**, `enabled: false` in `config/dimensions.json`):
  - `09_llm_output_quality` — Sonnet executor + Haiku judge vs SKILL.md promises
  - `10_trigger_precision`  — true-positive + collision prompts; judge grades trigger behaviour
  - `11_hallucination_probe` — 4 fabricated-input probes (fake tickers, invented papers, bogus endpoints, non-existent paths)
  - `12_prompt_injection`   — 16 OWASP-LLM-Top-10 baseline attacks; critical finding per successful hijack
  - `13_contract_drift`     — compares `composable_with:` peers' SKILL.md for input/output shape alignment
  - `14_llm_self_audit`     — meta-dim: SKILL.md + ARCHITECTURE.md + NON_GOALS.md consistency
- Shared infrastructure:
  - `scripts/lib/anthropic_client.py` — SDK wrapper with deterministic mock mode, cost tracking, graceful no-API fallback
  - `scripts/lib/judge.py` — Haiku judge invocation (temperature 0, JSON envelope parse + validate)
  - `scripts/lib/executor.py` — Sonnet executor (loads SKILL.md as system)
  - `scripts/lib/prompt_cache.py` — ephemeral `cache_control` helper, 4096-token padding footer
  - `scripts/lib/cost_guard.py` — `CostGuard` + `CostBudgetExceeded`; reads `max_cost_usd_per_run` from `config/thresholds.json` (default $5)
- Corpora:
  - `dimensions/12_prompt_injection/corpora/owasp-llm-top10.json` — 16 canonical attacks across 8 categories
- Config:
  - `config/llm_eval.json` — per-dimension model/temperature/max_tokens
  - `config/thresholds.json` — added `max_cost_usd_per_run: 5.0`
- Tests (+20 over phase 1 → **52 total**):
  - `test_anthropic_client_mock.py` — 8 tests; mock determinism + pricing
  - `test_cost_guard.py` — 7 tests; boundaries, charge/trip, config loading
  - `test_judge.py` — 11 tests; envelope parsing + UNKNOWN fallbacks + cost gating
  - `test_phase2_dims_smoke.py` — 6 tests; all 6 dims discoverable + runnable + phase-1 still intact
  - `tests/fixtures/` — canned executor + judge responses
- `scripts/audit.py`:
  - Honors `requires_api` flag; logs API mode (`live` / `mock` / `no-api`) per run
  - Explicit `--dimensions` filter now overrides `enabled: false` (opt-in)

### Invariants preserved
- No external deps beyond the single existing `anthropic` exception.
- Python 3.9 compatible (`Optional[...]` + `List[...]`; no `X | Y`).
- stdlib `unittest` only — no pytest.
- Binary verdicts only (PASS / FAIL / UNKNOWN); no numeric scoring in judges.
- Prompt caching annotated on every judge system block.
- Per-dim judge prompts, each ≤200 words, each versioned (`prompt_version: 0.1.0`).
- Default audit behaviour UNCHANGED — phase-2 dims off unless user opts in.

## [0.1.0] — 2026-04-19

### Added
- Initial release (phase 1).
- Core infrastructure:
  - `scripts/lib/tree_walker.py` — fleet discovery + `SkillInfo` introspection
  - `scripts/lib/decay_tracker.py` — stress-test cadence stopping rule
  - `scripts/lib/scorecard.py` — weighted aggregate grade
  - `scripts/lib/regression_vault.py` — append-only JSONL findings store
  - `scripts/lib/plugin_loader.py` — dynamic discovery of `dimensions/*/plugin.py`
  - `scripts/lib/report_renderer.py` — markdown scorecard output
- 8 pure-Python dimensions:
  - 01_adversarial, 02_scale, 03_composition, 04_security
  - 05_threat_intel, 06_types, 07_structural, 08_design_audit
- Entry-point scripts: `audit.py`, `audit_all.py`, `design_audit.py`, `create.py`, `improve.py` (stub), `benchmark.py`
- 4-mode lifecycle (Create / Eval / Improve / Benchmark) + Audit + DesignAudit gates
- Anthropic-compatible schemas (evals.json, grading.json, benchmark)
- ~30 stdlib unittest tests
- Install script with validator hook

### Deferred to phase 2
- LLM-backed dimensions 09–14 (executor + judge)
- `improve` mode fix-generation engine

### Deferred to phase 3
- Advanced dimensions 15–30 (property-based, mutation, fuzzing)

### Deferred to phase 4
- Meta layers M1–M8
