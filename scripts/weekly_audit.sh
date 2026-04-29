#!/usr/bin/env bash
# weekly_audit.sh — runs `.snes-fit audit --all` and snapshots results.
#
# Invoked by ~/Library/LaunchAgents/com.dimmmak.snes-fit-weekly.plist
# every Monday at 9am local time. Saves the fleet sweep to
# reports/weekly/YYYY-MM-DD.md and a delta-vs-prior summary so a
# human can scan changes in <30s.
#
# Closes synthesis recommendation #2 from the 2026-04-28 forensic
# fleet audit: institutionalize the audit discipline.

set -euo pipefail

REPO_ROOT="/Users/danny/Desktop/CLAUDE CODE/snes-fit"
WEEKLY_DIR="$REPO_ROOT/reports/weekly"
TODAY="$(date +%Y-%m-%d)"
REPORT="$WEEKLY_DIR/$TODAY.md"

mkdir -p "$WEEKLY_DIR"
cd "$REPO_ROOT"

# Source ~/.zshrc to pick up ANTHROPIC_API_KEY for real-LLM dims.
# If not available, audit runs in mock mode (degraded but still useful).
if [ -f ~/.zshrc ]; then
    # shellcheck source=/dev/null
    source ~/.zshrc 2>/dev/null || true
fi

{
    echo "# Weekly snes-fit fleet sweep — $TODAY"
    echo ""
    echo "Triggered by launchd. Mode: $([ -n "${ANTHROPIC_API_KEY:-}" ] && echo "real-LLM" || echo "mock (no API key)")"
    echo ""

    python3 scripts/audit_all.py 2>&1 || {
        echo ""
        echo "❌ AUDIT FAILED — see logs above. Snapshot preserved at $REPORT."
        exit 1
    }
} > "$REPORT" 2>&1

# Delta vs prior week (if exists)
PRIOR="$(ls -1 "$WEEKLY_DIR"/*.md 2>/dev/null | grep -v "^$REPORT$" | tail -1 || true)"
if [ -n "$PRIOR" ]; then
    {
        echo ""
        echo "---"
        echo ""
        echo "## Delta vs prior week ($(basename "$PRIOR" .md))"
        echo ""
        diff <(grep "^|" "$PRIOR" | head -40) <(grep "^|" "$REPORT" | head -40) || true
    } >> "$REPORT"
fi

# Surface the result via macOS notification (best-effort)
if command -v osascript &>/dev/null; then
    osascript -e "display notification \"Fleet audit complete. See: $REPORT\" with title \"snes-fit weekly\"" 2>/dev/null || true
fi

echo "✅ Weekly audit done: $REPORT"
