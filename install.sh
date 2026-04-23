#!/bin/bash
set -e
SRC="$HOME/Desktop/CLAUDE CODE/snes-fit"
DEST="$HOME/.claude/skills/snes-fit"

# Remove existing (symlink or dir)
if [ -L "$DEST" ] || [ -e "$DEST" ]; then
    rm -rf "$DEST"
fi

# Symlink source into skills dir
ln -s "$SRC" "$DEST"
echo "✅ .snes-fit symlinked: $DEST -> $SRC"

# Optional: run validator if present
VALIDATOR="$HOME/Desktop/CLAUDE CODE/future-proof/scripts/validate-skill.py"
if [ -f "$VALIDATOR" ]; then
    python3 "$VALIDATOR" "$DEST" || echo "⚠️  validator reported issues"
fi
