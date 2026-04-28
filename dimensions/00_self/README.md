# Dimension 00 — Self

Audit-the-auditor. Validates snes-fit's own conformance to `SPEC.md`.

## Why this dimension exists

Closes the self-reference paradox identified in `forensic CRIT #2` (2026-04-28
fleet audit). Three of four enforcement skills (mewtwo, snes-fit, forensic)
shared the same gap: each polices other skills against rules they exempt
themselves from. snes-fit's SKILL.md was missing all five required body
sections defined in its own SPEC.md — and the existing dimension framework
had no consumer that audited snes-fit itself.

This dimension is that consumer.

## Scope

Runs ONLY when `target.name == "snes-fit"`. Returns no findings for any other
skill — dimensions 07 (structural) and 08 (design_audit) handle non-self
skills. The unique value-add here is the recursive check.

## Failure mode if removed

Without this dimension, snes-fit can ship while non-compliant with the spec
it enforces on others. Every grade it emits becomes suspect because the
auditor itself failed the bar.

## Probe checks

| 🟣 Check | 🟣 Severity | 🟣 Source rule |
|---|---|---|
| Required files present (SKILL.md, ARCHITECTURE.md, SCHEMA.md, CHANGELOG.md) | critical | SPEC.md:24-34 |
| NON_GOALS.md OR `## Non-goals` section | minor | SPEC.md:34 |
| 5 required body sections (Purpose, When to trigger, When NOT to trigger, Anti-patterns, Exit conditions) | critical | SPEC.md:55-64 |
| YAML frontmatter present | critical | SPEC.md:38-51 |
| Frontmatter has `name`, `description` | critical | SPEC.md:42-45 |
| Description includes 2+ NOT for: clauses | major | SPEC.md:45 |

## Run cadence

- Every `.snes-fit audit --skill snes-fit` run (explicit self-audit)
- First in any `.snes-fit audit --all` fleet sweep — if self-audit fails,
  fleet sweep refuses to proceed (the auditor must clear its own bar before
  policing the fleet)

## Decision history

| 🟣 Decision | 🟣 Date | 🟣 Outcome |
|---|---|---|
| Add 00_self dimension | 2026-04-28 | Built (forensic CRIT #2 fix) |
| Make it skill-specific (not run on every skill) | 2026-04-28 | Yes — overlap with 07/08 otherwise |
| Block fleet sweep on self-audit failure | 2026-04-28 | Yes — wired into runner Phase 5.5+ |
