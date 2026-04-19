# Dimension 04 — Security

**What it probes:** OWASP LLM Top 10 baseline + common Python CWEs.

**Why:** a leaked API key in a committed file is game over. Path traversal lets an attacker read `../../etc/passwd`. A ReDoS regex on user input freezes the whole process.

## Checks

| 🟣 Check | 🟣 Severity | 🟣 CWE / OWASP |
|---|---|---|
| AWS / OpenAI / GitHub / Slack tokens | critical | CWE-798 |
| Private key material | critical | CWE-798 |
| Hardcoded password literal | major | CWE-798 |
| Path traversal in open() | major | CWE-22 |
| ReDoS (nested quantifiers) | minor | CWE-1333 |

False positives are acceptable; findings are heuristic. Severity is erred-toward-loud.
