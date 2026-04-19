# Dimension 02 — Scale

**What it probes:** skill-level disk footprint and walk-time benchmarks.

**Why:** a skill that balloons to 50 MB or 2000 files is smuggling data it shouldn't own — logs should rotate, fixtures should be elsewhere. Walk-time over 5s means future audits won't scale across the fleet.

## Thresholds

| 🟣 Metric | 🟣 Limit | 🟣 Severity |
|---|---|---|
| Total files | 2000 | minor |
| Total size | 50 MB | major |
| Single-file size | 2 MB | minor |
| Tree walk time | 5 s | minor |
