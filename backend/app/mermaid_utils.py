"""Mermaid cleaning and light validation helpers.

Backend cannot fully compile Mermaid diagrams, but it can catch common LLM mistakes:
- code fences around Mermaid
- extra prose before the diagram
- wrong diagram starter
"""
from __future__ import annotations

import re


VALID_STARTS = (
    "classDiagram",
    "erDiagram",
    "flowchart",
    "graph",
    "sequenceDiagram",
    "stateDiagram-v2",
)


def strip_code_fence(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:mermaid)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def sanitize_mermaid(text: str | None, expected_start: str, fallback: str) -> str:
    """Return Mermaid text that starts with expected_start where possible."""
    if not text:
        return fallback

    cleaned = strip_code_fence(text)
    # Remove Markdown bullets accidentally returned before the diagram.
    cleaned = cleaned.replace("```mermaid", "").replace("```", "").strip()

    if cleaned.startswith(expected_start):
        return cleaned

    # Try to recover if the LLM added explanation before the actual diagram.
    idx = cleaned.find(expected_start)
    if idx >= 0:
        return cleaned[idx:].strip()

    return fallback


def validate_mermaid_light(text: str) -> tuple[bool, str | None]:
    """Simple validation used by tests and API response warnings."""
    cleaned = strip_code_fence(text)
    if not cleaned:
        return False, "Mermaid output is empty."
    if not cleaned.startswith(VALID_STARTS):
        return False, "Mermaid output must start with a valid diagram keyword."
    if "```" in cleaned:
        return False, "Mermaid output should not contain Markdown code fences."
    return True, None
