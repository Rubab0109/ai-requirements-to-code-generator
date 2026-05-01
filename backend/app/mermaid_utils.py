"""Mermaid cleaning and light validation helpers.

Backend cannot fully compile Mermaid diagrams, but it can catch common LLM mistakes:
- code fences around Mermaid
- extra prose before the diagram
- wrong diagram starter
- SQL-style ERD attribute types such as VARCHAR(50)
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


def _map_erd_type(raw_type: str) -> str:
    """Convert SQL-ish types into Mermaid-safe ERD types."""
    base = re.sub(r"\(.*?\)", "", raw_type).strip().upper()

    if base in {"VARCHAR", "CHAR", "TEXT", "UUID", "STRING"}:
        return "string"
    if base in {"INT", "INTEGER", "BIGINT", "SMALLINT", "SERIAL", "NUMBER"}:
        return "int"
    if base in {"DECIMAL", "NUMERIC", "FLOAT", "DOUBLE", "REAL"}:
        return "float"
    if base in {"BOOLEAN", "BOOL"}:
        return "boolean"
    if base in {"DATE"}:
        return "date"
    if base in {"DATETIME", "TIMESTAMP", "TIME"}:
        return "datetime"

    return base.lower() or "string"


def normalize_erd_mermaid(text: str) -> str:
    """Fix common Mermaid ERD parse issues caused by LLMs."""
    if not text.strip().startswith("erDiagram"):
        return text

    fixed_lines: list[str] = []

    for line in text.splitlines():
        stripped = line.strip()

        if not stripped:
            fixed_lines.append(line)
            continue

        # Keep diagram title, relations, entity open/close lines as they are.
        if (
            stripped == "erDiagram"
            or "--" in stripped
            or stripped.endswith("{")
            or stripped == "}"
        ):
            fixed_lines.append(line)
            continue

        # Fix attributes inside ERD blocks:
        # Example: VARCHAR(36) id PK  -> string id PK
        # Example: TIMESTAMP created_at -> datetime created_at
        tokens = stripped.replace("}", "").split()
        if len(tokens) >= 2:
            indent = line[: len(line) - len(line.lstrip())]
            mermaid_type = _map_erd_type(tokens[0])
            field_name = tokens[1]

            keys = []
            for token in tokens[2:]:
                upper = token.upper().strip(",")
                if upper in {"PK", "FK", "UK"}:
                    keys.append(upper)

            fixed_line = f"{indent}{mermaid_type} {field_name}"
            if keys:
                fixed_line += " " + " ".join(keys)

            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines).strip()


def sanitize_mermaid(text: str | None, expected_start: str, fallback: str) -> str:
    """Return Mermaid text that starts with expected_start where possible."""
    if not text:
        return fallback

    cleaned = strip_code_fence(text)
    cleaned = cleaned.replace("```mermaid", "").replace("```", "").strip()

    if cleaned.startswith(expected_start):
        if expected_start == "erDiagram":
            cleaned = normalize_erd_mermaid(cleaned)
        return cleaned

    idx = cleaned.find(expected_start)
    if idx >= 0:
        recovered = cleaned[idx:].strip()
        if expected_start == "erDiagram":
            recovered = normalize_erd_mermaid(recovered)
        return recovered

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
