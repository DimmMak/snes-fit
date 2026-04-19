# Dimension 01 — Adversarial

**What it probes:** static patterns in the skill's `scripts/` that suggest fragility under hostile input.

**Why:** a skill that indexes `sys.argv[1]` without a length check crashes the first time a user forgets the argument. A `bare except` swallows injection evidence. `eval()` on untrusted input is game over.

**Phase 1 scope (stdlib only):** regex-based static scan. No dynamic fuzzing yet.

**Phase 2 plan:** actually call the skill with None, empty string, 1MB string, unicode, control chars, and record crashes.

## Patterns checked

| 🟣 Pattern | 🟣 Severity | 🟣 Reason |
|---|---|---|
| `sys.argv[1]` without bounds check | minor | IndexError on missing arg |
| Bare `except:` | minor | Swallows adversarial evidence |
| `eval(...)` | major | Arbitrary code execution vector |
| `exec(...)` | major | Arbitrary code execution vector |
