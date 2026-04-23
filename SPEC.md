# SNES-Fit Spec v0.2

The FLEET standard. A skill "fits" the SNES cartridge slot when it satisfies
every rule below. This file is the **single source of truth** — both
`snes-fit`'s audit plugins AND `snes-builder`'s scaffolder read from it.

Spec version: **0.2.0**
Last reviewed: **2026-04-23**

---

## How this file is consumed

| Consumer | Role | Reads |
|---|---|---|
| `snes-fit/dimensions/*/plugin.py` | Audit — enforces spec | "Required files" + "Required frontmatter" + "Canonical subdirs" + "Forbidden patterns" |
| `snes-builder` Phase 5.5 | Scaffold — generates compliant skills | Same sections; emits stubs that pass snes-fit on first audit |

When this spec changes, both consumers pick it up automatically. Bump
`spec_version` in the front matter when breaking changes land.

---

## Required files per skill

Every skill folder must contain:

| Filename | Purpose | Severity if missing |
|---|---|---|
| `SKILL.md` | Entry point, YAML frontmatter + body | **critical** (structural) |
| `ARCHITECTURE.md` | Why the skill is structured this way | **major** |
| `SCHEMA.md` | JSON schemas the skill relies on (or `N/A` if none) | **major** |
| `CHANGELOG.md` | Version history | **minor** |
| `NON_GOALS.md` OR `## Non-goals` section in SKILL.md | What the skill explicitly does NOT do | **minor** |

---

## Required frontmatter fields (SKILL.md)

YAML block at top of SKILL.md. Fields marked **R** are required.

| Field | Required | Notes |
|---|---|---|
| `name` | **R** | kebab-case, matches folder name, max 64 chars |
| `description` | **R** | max 1024 chars, MUST include `NOT for:` clauses naming 2+ sibling skills |
| `composable_with` | optional | list of sibling skills that actually exist on disk |
| `metadata.version` | optional | skill version — place under `metadata:`, not top-level |
| `metadata.last_reviewed` | optional | ISO date — place under `metadata:`, not top-level |
| `metadata.spec_version` | optional | which SNES-fit spec version the skill targets |

**Top-level custom keys are forbidden.** Use `metadata:` for anything non-standard.

---

## Required SKILL.md body sections

Headers must appear verbatim (case-insensitive OK):

- `## Purpose` — 1-3 paragraph summary
- `## When to trigger` — explicit trigger phrases or conditions
- `## When NOT to trigger` — explicit exclusions (collision fence)
- `## Anti-patterns` — what failure modes the skill guards against
- `## Exit conditions` — when the skill stops applying

---

## Canonical subdirectories

Top-level dirs inside a skill folder. Unknown dirs are flagged **cosmetic**.

```
scripts/    config/    prompts/    tests/    logs/
dimensions/ evals/     vault/      reports/  data/
```

Dirs prefixed with `_` (e.g., `_archive`) are allowed without flag.

---

## Forbidden patterns

| Pattern | Dimension | Severity |
|---|---|---|
| Hardcoded secrets (API keys, tokens, passwords) | 04_security | **critical** |
| Path traversal (`../` in file ops without validation) | 04_security | **major** |
| ReDoS — nested quantifiers in capture groups | 04_security | **major** |
| Cross-skill Python imports (`from <sibling-skill>`) | 07_structural | **major** |
| CRLF injection markers in text files | 05_threat_intel | **minor** |
| BOM at start of text files | 05_threat_intel | **minor** |
| Homograph / confusable unicode chars | 05_threat_intel | **minor** |
| Tree depth > 5 | 07_structural | **minor** |
| Functions missing type hints | 06_types | **minor** |
| Files > per-file size cap (2 MB) | 02_scale | **minor** |
| Skill total size > 50 MB (excluding `data/cache/**`) | 02_scale | **major** |

**Size exemption:** `data/cache/**` is exempt from all 02_scale size caps
(total bytes + per-file). Rationale: API-rate-limited skills (filings-desk,
earnings-desk, options-desk, macro-desk) legitimately cache large source
documents (SEC filings, earnings transcripts, options chains). Caching is
best practice for rate-limited APIs; flagging it as bloat punishes
responsible behavior. If a skill needs data outside `data/cache/`, size
rules still apply.

---

## Severity tiers

Used by snes-fit to grade audits:

| Tier | Meaning | Ship impact |
|---|---|---|
| **critical** | Skill is broken or dangerous | Blocks ship |
| **major** | Real gap, skill works but drifts from spec | Blocks ship |
| **minor** | Should-fix, not dangerous | Allowed 1 per round |
| **cosmetic** | Style / consistency only | Allowed freely |

**Ship-ready decay rule:** skill ships only when it hits
**≤1 cosmetic + 0 structural/major findings for 2 consecutive audit rounds.**
Each round = one audit pass with fixes in between. Enforced by
`scripts/lib/decay_tracker.py`. No bypass.

---

## Scoring

- Starts at 100
- Each finding deducts per-dimension weight × severity multiplier
- Grade: A ≥ 90, B ≥ 80, C ≥ 70, D ≥ 60, F < 60
- Final score capped at [0, 100]

---

## Versioning this spec

When a snes-fit dimension adds/removes a rule:

1. Update the relevant section above
2. Bump `spec_version` at the top of this file
3. Commit both the dimension change AND this SPEC.md in the same PR
4. Skills record `metadata.spec_version` in their SKILL.md to track which
   spec version they were audited against

---

## Non-goals for this spec

- Does NOT enforce semantic quality (e.g., "is this skill useful?") — that's a human judgment
- Does NOT define test coverage thresholds (future work)
- Does NOT cover LLM-eval dimensions (09-14) — those are phase 2, documented separately
