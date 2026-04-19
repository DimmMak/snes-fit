# Dimension 03 — Composition

**What it probes:** every `composable_with` entry in the skill's SKILL.md frontmatter must point to a real sibling directory in the fleet.

**Why:** stale composition references are lies. A skill that claims to compose with `price-desk` but references a renamed/deleted skill silently confuses mewtwo and other orchestrators.

## Checks

| 🟣 Check | 🟣 Severity |
|---|---|
| SKILL.md has frontmatter | minor if missing |
| composable_with declared | cosmetic if missing |
| Each entry resolves to a real directory | major if broken |
