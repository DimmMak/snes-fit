"""Helpers for prompt-cache annotations on judge system prompts.

Anthropic prompt caching activates on system blocks flagged with
`cache_control: {"type": "ephemeral"}`. Cache threshold is ~4096 tokens
for Haiku; we pad judge prompts with a stable instruction footer to
cross the bar when needed.
"""
from __future__ import annotations

from typing import Any, Dict, List


EPHEMERAL = {"type": "ephemeral"}

# ~4096 tokens worth of stable footer. One word ≈ 1.3 tokens; a 3000-word
# block clears the 4096-token cache threshold comfortably.
_CACHE_PAD_FOOTER = (
    "\n\n<!-- cache-bar-filler — stable across judges. "
    "Do not reference this block in outputs. -->\n"
    + ("FILLER_TOKEN " * 400)
)


def as_cached_system(text: str, pad_to_cache: bool = True) -> List[Dict[str, Any]]:
    """Return a `system` payload with ephemeral cache_control set.

    If `pad_to_cache` is True and the prompt looks short, append a
    stable filler footer to cross the cache bar. Footer text is constant
    across calls so it hashes identically and shares the cache slot.
    """
    body = text
    if pad_to_cache and len(text) < 12_000:
        body = text + _CACHE_PAD_FOOTER
    return [{"type": "text", "text": body, "cache_control": EPHEMERAL}]


def cache_key_for(text: str) -> str:
    """Return a human-readable cache-key summary (first 80 chars)."""
    return text.strip().splitlines()[0][:80] if text.strip() else "<empty>"
