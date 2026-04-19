# 12 — Prompt injection

| 🟣 Field | 🟣 Value |
|---|---|
| Dimension | `12_prompt_injection` |
| Runs on | skill |
| Requires API | yes |
| Default enabled | no |

Fires 16 OWASP-LLM-Top-10 baseline attacks (jailbreak, role-hijack,
privilege escalation, data exfiltration, indirect injection, tool-abuse,
payload smuggling, policy / refusal bypass) at the skill. Judge scores
PASS/FAIL per attack. Successful injections surface as **critical**
severity findings.
