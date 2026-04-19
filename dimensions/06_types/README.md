# Dimension 06 — Types

**What it probes:** AST-based type-hint coverage across `scripts/*.py`.

**Why:** a skill with no type hints has no contract. Future readers (and static analyzers) can't reason about its inputs and outputs. 50% coverage is a soft floor.

## Rule

A public function (name not starting with `_`, except `__init__`) is "annotated" iff every non-self param has an annotation AND the function has a return annotation.

If coverage drops below 50%, emit one minor finding. SyntaxErrors surface as major.

Phase 2 adds mypy / pyright integration.
