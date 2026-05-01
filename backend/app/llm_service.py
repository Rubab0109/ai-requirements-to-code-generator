"""LLM integration service.

Supports:
- Gemini REST API by default
- Groq OpenAI-compatible Chat Completions
- OpenAI Chat Completions

The frontend never sees API keys. Only this backend reads .env.
"""
from __future__ import annotations

import json
import re
from typing import Any

import httpx

from .config import get_settings
from .mermaid_utils import sanitize_mermaid, validate_mermaid_light
from .prompts import master_generation_prompt
from .sample_generator import build_demo_response


settings = get_settings()


class LLMError(RuntimeError):
    """Raised when the selected LLM provider fails."""


UML_FALLBACK = """classDiagram
  class User {
    +int id
    +string name
  }
  class Project {
    +int id
    +string title
  }
  User --> Project
""".strip()

ERD_FALLBACK = """erDiagram
  USERS ||--o{ PROJECTS : owns
  USERS {
    int id PK
    string name
    string email
  }
  PROJECTS {
    int id PK
    int user_id FK
    string title
  }
""".strip()


def _extract_json(text: str) -> dict[str, Any]:
    """Extract JSON even if a model accidentally returns prose or code fences."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start >= 0 and end > start:
            return json.loads(cleaned[start : end + 1])
        raise


def _normalize_payload(payload: dict[str, Any], requirements: str, title: str | None) -> dict[str, Any]:
    """Ensure every required frontend field exists."""
    demo = build_demo_response(requirements, title)
    normalized = {**demo, **payload}
    normalized.pop("warning", None) if payload else None

    normalized["functional_requirements"] = normalized.get("functional_requirements") or []
    normalized["non_functional_requirements"] = normalized.get("non_functional_requirements") or []
    normalized["assumptions"] = normalized.get("assumptions") or []
    normalized["tech_stack"] = normalized.get("tech_stack") or []
    normalized["testing_notes"] = normalized.get("testing_notes") or []

    normalized["uml_mermaid"] = sanitize_mermaid(normalized.get("uml_mermaid"), "classDiagram", UML_FALLBACK)
    normalized["erd_mermaid"] = sanitize_mermaid(normalized.get("erd_mermaid"), "erDiagram", ERD_FALLBACK)

    checks = {
        "uml": validate_mermaid_light(normalized["uml_mermaid"]),
        "erd": validate_mermaid_light(normalized["erd_mermaid"]),
    }
    normalized["mermaid_warnings"] = [message for ok, message in checks.values() if not ok and message]
    normalized["source"] = normalized.get("source", settings.LLM_PROVIDER)
    return normalized


async def generate_ai_project(requirements: str, title: str | None = None) -> dict[str, Any]:
    """Main function used by FastAPI endpoint."""
    provider = settings.LLM_PROVIDER.lower().strip()
    prompt = master_generation_prompt(requirements=requirements, title=title)

    try:
        if provider == "gemini":
            raw = await _call_gemini(prompt)
        elif provider == "groq":
            raw = await _call_openai_compatible(
                prompt=prompt,
                api_key=settings.GROQ_API_KEY,
                model=settings.GROQ_MODEL,
                base_url="https://api.groq.com/openai/v1/chat/completions",
                provider_name="groq",
            )
        elif provider == "openai":
            raw = await _call_openai_compatible(
                prompt=prompt,
                api_key=settings.OPENAI_API_KEY,
                model=settings.OPENAI_MODEL,
                base_url="https://api.openai.com/v1/chat/completions",
                provider_name="openai",
            )
        else:
            raise LLMError(f"Unsupported LLM_PROVIDER '{settings.LLM_PROVIDER}'. Use gemini, groq, or openai.")

        parsed = _extract_json(raw)
        return _normalize_payload(parsed, requirements, title)

    except Exception as exc:  # noqa: BLE001 - we convert all provider errors to a user-safe response
        if settings.ALLOW_DEMO_FALLBACK:
            demo = build_demo_response(requirements, title)
            demo["warning"] = f"LLM provider failed or is not configured. Demo fallback used. Details: {exc}"
            return _normalize_payload(demo, requirements, title)
        raise LLMError(str(exc)) from exc


async def _call_gemini(prompt: str) -> str:
    if not settings.GEMINI_API_KEY:
        raise LLMError("GEMINI_API_KEY is missing in backend/.env")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent"
    params = {"key": settings.GEMINI_API_KEY}
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": settings.LLM_TEMPERATURE,
            "responseMimeType": "application/json",
        },
    }
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, params=params, json=payload)
        response.raise_for_status()
        data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMError(f"Unexpected Gemini response: {data}") from exc


async def _call_openai_compatible(
    prompt: str,
    api_key: str | None,
    model: str,
    base_url: str,
    provider_name: str,
) -> str:
    if not api_key:
        raise LLMError(f"{provider_name.upper()} API key is missing in backend/.env")

    payload = {
        "model": model,
        "temperature": settings.LLM_TEMPERATURE,
        "messages": [
            {"role": "system", "content": "Return only valid JSON. You are a senior software architect."},
            {"role": "user", "content": prompt},
        ],
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(base_url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMError(f"Unexpected {provider_name} response: {data}") from exc
