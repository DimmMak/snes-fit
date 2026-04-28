# .forensic audit — snes-fit (audit-the-auditor pass)

**Date:** 2026-04-28
**Auditor:** .forensic v0.1.0
**Target:** snes-fit v0.1.0
**Files reviewed:** SKILL.md, SPEC.md, NON_GOALS.md
**Severity counts:** CRIT=2 · HIGH=2 · MED=3 · LOW=2

---

## Biggest Issues

### 1. **[CRIT] snes-fit's own SKILL.md fails its own SPEC**
> "Required SKILL.md body sections — Headers must appear verbatim (case-insensitive OK):
> - `## Purpose` — 1-3 paragraph summary
> - `## When to trigger` — explicit trigger phrases or conditions
> - `## When NOT to trigger` — explicit exclusions (collision fence)
> - `## Anti-patterns` — what failure modes the skill guards against
> - `## Exit conditions` — when the skill stops applying"
> *(SPEC.md:55-64)*
>
> snes-fit's actual SKILL.md body sections (per Read of lines 35-80):
> "# .snes-fit — Fleet-Wide QA Skill / ## Subcommands / ## 4-mode lifecycle / ## Decay stopping rule / ## Plugin tree"
> *(SKILL.md:35-80)*

**Why this fails:** Zero of the five required sections are present in snes-fit's SKILL.md. The auditor of fleet compliance is itself non-compliant against the spec it audits against. Mechanism: if snes-fit ran `audit --skill snes-fit`, the structural dimension (07_structural) would emit ≥5 critical findings. The decay-rule ship-gate "≤1 cosmetic + 0 structural/major" would fire and refuse to ship — meaning snes-fit cannot ship itself. Yet it has shipped (v0.1.0 in frontmatter). Either the dimension doesn't actually check the spec it claims to, or self-audit was skipped.

---

### 2. **[CRIT] Audit-the-auditor blind spot is structural**
> "Plugin tree — Every dimension is its own dir under `dimensions/`. Drop in `dimensions/NN_name/plugin.py` with a `DimensionPlugin` subclass and it gets auto-discovered."
> *(SKILL.md:75-77)*
>
> "When this spec changes, both consumers pick it up automatically."
> *(SPEC.md:19-20)*

**Why this fails:** SPEC.md names two consumers — snes-fit dimensions and snes-builder. snes-fit reads SPEC.md to audit OTHER skills. There is no consumer that audits snes-fit's own conformance to SPEC.md. The plugin-architecture claim ("auto-discovered") means dimensions can drift independently of SPEC, but no dimension audits the dimension framework itself. Mechanism: same self-reference paradox documented in the mewtwo audit (CRIT #2). Two of four audited skills share this class — pattern, not coincidence.

---

### 3. **[HIGH] Severity tier vocabulary inconsistent within the spec**
> "Severity tiers: critical / major / minor / cosmetic"
> *(SPEC.md:108-115)*
>
> "Ship-ready decay rule: skill ships only when it hits **≤1 cosmetic + 0 structural/major findings** for 2 consecutive audit rounds."
> *(SPEC.md:117-118)*

**Why this fails:** "structural" is not a tier name. The four declared tiers are critical/major/minor/cosmetic. The decay rule introduces a new term ("structural") without definition. Mechanism: ambiguity at the ship-gate. Does "structural/major" mean "issues tagged critical OR major"? Or "structural-class issues regardless of tier"? A reader cannot tell. Compare snes-fit/SPEC.md:84-95 where "Forbidden patterns" tags entries with the explicit tiers (critical, major, minor) — consistent there, drifted at the decay rule.

---

### 4. **[HIGH] composable_with claim with mewtwo is one-way**
> "composable_with: snes-builder, future-proof, mewtwo, home"
> *(SKILL.md:28-32)*
>
> "Skills without a registry entry are invisible to Mewtwo. On purpose."
> *(mewtwo/CONTRACT.md:96, cross-referenced)*

**Why this fails:** snes-fit declares mewtwo as composable_with, but mewtwo's contract requires four checkmarks (reports / archives / fails-loud / reversible) declared in SKILLS_REGISTRY.md. snes-fit's SKILL.md does not declare those four checkmarks. Mechanism: mewtwo will refuse to call snes-fit. The composability claim is aspirational, not actual. Equivalent to declaring you can be called via TCP without opening a port.

---

## Other Issues

- **[MED] "ship gate enforced in code, not in policy" — but ship action is undefined** — > "No bypass of decay rule | Ship gate is enforced in code, not in policy" *(NON_GOALS.md:16)*. What is "ship"? Git push? Symlink to ~/.claude/skills/? Tag as v1.0.0? The non-goal asserts code enforcement of a verb that has no defined target. Compare cash-out's `--autonomous` flag which has clear push targets — snes-fit's "ship" is abstract.

- **[MED] Phase 2 referenced but unspecified** — > "calls: [] # phase 2 adds: anthropic SDK (sonnet + haiku)" *(SKILL.md:16)* and > "Does NOT cover LLM-eval dimensions (09-14) — those are phase 2, documented separately" *(SPEC.md:149)*. Phase 2 is anchored in two places but no phase 2 spec file exists in the repo. SCHEMA.md, ARCHITECTURE.md, and SPEC.md were checked; none is the phase-2 spec. "Documented separately" → where?

- **[MED] "Compatible with Anthropic skill-creator eval schemas" — claim untested** — > "Compatible with Anthropic skill-creator eval schemas." *(SKILL.md:6)*. Asserted in description, no test reference, no schema-version pin, no compatibility test referenced. The whole "create" subcommand at SKILL.md:50 produces evals.json — but compatibility against which schema version is unstated.

- **[LOW] Score clamping is band-aid not formula** — > "Final score capped at [0, 100]" *(SPEC.md:129)*. The scoring formula at SPEC.md:127 is "Each finding deducts per-dimension weight × severity multiplier" — no upper bound on deductions. A skill with 200 cosmetic findings could underflow to -50 before the clamp. The clamp masks the underflow rather than preventing it. NON_GOALS.md:15 says "overflow is a bug, not a feature" — but the design produces overflows that must be clamped.

- **[LOW] NON_GOALS.md non-goal #11 is phase-bound** — > "11 | No external network calls in phase 1 | Stdlib only; reproducible offline" *(NON_GOALS.md:17)*. Listed as a permanent invariant ("Each entry is a structural commitment, not a preference") but conditioned on "phase 1." Phase 2 explicitly adds Anthropic SDK calls (network). Either the non-goal expires (then it's not invariant) or phase 2 violates a structural commitment. Pick one.

---

## Summary

snes-fit ships a coherent plugin-architecture spec and a defensible decay rule, but **the auditor is itself unaudited and itself non-compliant** with the spec it enforces. Its SKILL.md is missing all five required body sections, its severity vocabulary drifts at the ship-gate, and its composability claims with mewtwo are aspirational. The skill that grades the fleet would receive a failing grade from itself.

---

## Self-audit (what forensic might have missed)

- Did not read `dimensions/*/plugin.py`. The "07_structural" dimension may already have a self-skip exemption that explains why snes-fit hasn't been failing its own audit (escape valve).
- Did not run `snes-fit audit --skill snes-fit` to verify the CRIT #1 prediction empirically. The finding is structural (read of source files), not measured.
- The "ship action undefined" critique presumes shipping = pushing to remote. If snes-fit treats "ship" as marking a skill ready-for-use in the registry, the gate is observable in code (a registry write).
- The "structural" vs "structural/major" ambiguity may be resolved in `scripts/lib/decay_tracker.py` (not read). If the code uses tier names as canonical and "structural" is informal English, the spec drift is documentation-only.
