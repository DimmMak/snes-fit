# Dimension 07 — Structural

**What it probes:** the skill's tree must obey fleet-wide invariants.

**Why:** without structural guarantees, skills become spaghetti. Cross-skill imports turn a tree into a graph (principle_tree_structure_always violation).

## Invariants

| 🟣 Invariant | 🟣 Severity if broken |
|---|---|
| SKILL.md at root | critical |
| Only canonical top-level subdirs | cosmetic |
| Tree depth ≤ 5 | minor |
| No `from <sibling-skill>` imports in scripts/ | major |

Canonical subdirs: `scripts/`, `config/`, `prompts/`, `tests/`, `logs/`, `dimensions/`, `evals/`, `vault/`, `reports/`, `data/`.
