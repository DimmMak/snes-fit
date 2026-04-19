# Changelog

All notable changes to `.auto-test`.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [SemVer](https://semver.org/).

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
