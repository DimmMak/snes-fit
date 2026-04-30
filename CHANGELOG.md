# Changelog

All notable changes to `.snes-fit`.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [SemVer](https://semver.org/).

## [0.2.2] — 2026-04-30

### Fixed
- **`12_prompt_injection` mock-mode false positives** (`dimensions/12_prompt_injection/plugin.py` v0.1.0 → v0.2.0). Previously: when `ANTHROPIC_API_KEY` was missing, every skill audit emitted **16 critical findings** of shape `injection succeeded on lm01-XX (...): [mock] deterministic response for testing`. Root cause: the mock client in `anthropic_client.py` returns canned `verdict: FAIL` JSON whenever the prompt blob contains keywords `jailbreak_success`, `fail_keyword`, or `hallucinate` — and the OWASP attack corpus literally includes the string `JAILBREAK_SUCCESS` as the *desired* LLM hallucination. Result: every attack tripped the mock-FAIL keyword check → 16 fake criticals × 45 skills = **720 false-positive critical findings fleet-wide**, dragging every skill's score down by ~12 points.
- **Fix:** plugin now short-circuits in mock mode and emits ONE minor finding (`prompt-injection probe skipped — running in mock mode`) instead of 16 fake criticals. Real probing resumes the moment `ANTHROPIC_API_KEY` is set.
- **Impact:** every skill grade jumps ~12 points overnight on the next 9am cash-out audit. eli5 (was B+ 88) projected → A 95+. Same lift across all 45 audited skills.

### Why this matters
- Mock-mode is the default for any Mac that doesn't have `ANTHROPIC_API_KEY` exported in the shell snes-fit runs in (cron + cash-out scheduler typically don't inherit interactive shell env). So the fleet has been audited in mock-mode the entire time.
- Without this fix, `Ship-ready: NO` was guaranteed forever for every skill, no matter how clean — because dim 12 always emitted 16 crits.

### Origin
2026-04-30 — found while investigating eli5 v0.10.0 audit (88/100, B+, 16 mocked criticals). Danny: "wire it up to lift every skill in the fleet by ~12 points overnight." Done.

---

## [0.2.1] — 2026-04-19

### Fixed
- **Cosmetic findings ignored by default scorer** (`dimensions/_plugin_base.py`) — now score `-0.01` each. Previously invisible to the scorecard grade while still counting toward the decay ship gate, producing 100/100 + "not ship-ready" contradictions.
- **Plugin name collisions silently won by load order** (`scripts/lib/plugin_loader.py`) — duplicate `name` values now emit a stderr warning and the second instance is skipped.
- **Judge cost-guard token estimate off ~2×** (`scripts/lib/judge.py`) — `len(text)//3` → `len(text)//4` to match Anthropic's documented English approximation.
- **Round IDs never incremented across invocations** (`scripts/audit.py`, `audit_all.py`, `design_audit.py`) — every `--round`-less run stacked markers under round 1. CLI default changed `1 → None`; `decay_tracker.next_round_id()` now auto-increments from `max(existing) + 1`.
- **Decay visualization was ambiguous** (`scripts/lib/report_renderer.py`) — replaced the compact sparkline + digit tuple (e.g. `7→1→0→1→1`) with a self-describing `## Rounds` table: one row per round, explicit 🟢 CLEAN / 🔴 DIRTY verdict, separate structural/minor/cosmetic/marker columns, and a plain-English streak + ship-gate line.

### Added
- `decay_tracker.summarize_rounds()` + `RoundSummary` dataclass (per-round structural/minor/cosmetic/marker counts, clean flag)
- `decay_tracker.clean_streak()` — trailing consecutive clean-round counter
- `decay_tracker.next_round_id()` — auto-increment helper
- 9 regression tests (**66 total**):
  - `tests/test_plugin_base_score.py` — cosmetic scoring + mixed-severity behaviour (7 tests)
  - `tests/test_plugin_loader_collision.py` — collision warning + independent loads (2 tests)
  - `tests/test_decay_tracker.py` — `next_round_id`, `summarize_rounds`, `clean_streak` (5 new tests)

### Changed
- `report_renderer.render_scorecard()` signature: `decay_curve` replaced with `round_summaries` + `clean_streak` + `zero_rounds_required`. Legacy `_decay_ascii` sparkline helper deleted.
- `--round` CLI default `1 → None` across audit/audit_all/design_audit. Explicit integers still honored for tests and replays.

### Notes
Born from a session where the old sparkline was misread three turns in a row — the display was ambiguous, the JSONL vault was authoritative. Fix makes the display self-describing so the same misread can't happen again. Also pinned a `feedback_verify_before_quoting` rule in the memory repo.

---

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
