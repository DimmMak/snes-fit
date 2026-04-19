# Dimension 05 — Threat Intel (i18n / injection)

**What it probes:** i18n-flavored attacks that slip past ASCII-only thinking.

**Why:** a homograph attack hides a malicious URL in plain text. A UTF-8 BOM at the start of `rules.json` breaks naive `json.load()` callers. CRLF line endings leak Windows-provenance data and confuse downstream tools.

## Checks

| 🟣 Check | 🟣 Severity |
|---|---|
| UTF-8 BOM at file start | minor |
| CRLF line endings (non-Windows files) | cosmetic |
| Homograph / confusable chars (Cyrillic impostors) | major |
