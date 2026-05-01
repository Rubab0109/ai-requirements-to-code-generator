"""Centralized LLM prompts for consistent output."""
from __future__ import annotations

from textwrap import dedent


SYSTEM_ROLE = """
You are a senior software architect and AI product developer.
Your job is to convert raw software requirements into implementation-ready artifacts.
Return only valid JSON. Do not wrap JSON in Markdown. Do not add extra commentary.
""".strip()


OUTPUT_CONTRACT = """
Return JSON with exactly these keys:
{
  "analysis": "clean requirement analysis in 1-2 paragraphs",
  "assumptions": ["assumption 1", "assumption 2"],
  "functional_requirements": ["FR 1", "FR 2"],
  "non_functional_requirements": ["NFR 1", "NFR 2"],
  "uml_mermaid": "classDiagram\\n  class User { ... }",
  "erd_mermaid": "erDiagram\\n  USERS ||--o{ ORDERS : places ...",
  "database_schema": "SQL CREATE TABLE statements",
  "code_skeleton": "starter code skeleton, preferably FastAPI or MERN style depending on requirement",
  "tech_stack": ["Frontend: ...", "Backend: ..."],
  "testing_notes": ["test case 1", "test case 2"]
}
Important Mermaid rules:
- uml_mermaid must start with classDiagram.
- erd_mermaid must start with erDiagram.
- Do not use Markdown code fences in Mermaid.
- Keep diagrams valid and not overly large.
""".strip()


def master_generation_prompt(requirements: str, title: str | None = None) -> str:
    return dedent(
        f"""
        {SYSTEM_ROLE}

        Project title: {title or "Untitled Software Project"}

        Raw requirements:
        {requirements}

        Tasks:
        1. Analyze the requirement clearly.
        2. Extract functional requirements.
        3. Extract non-functional requirements.
        4. Generate UML class diagram in Mermaid syntax.
        5. Generate ERD in Mermaid syntax.
        6. Generate normalized database tables as SQL.
        7. Generate clean starter code skeleton.
        8. Suggest a suitable technology stack.
        9. Add testing notes.

        {OUTPUT_CONTRACT}
        """
    ).strip()


def requirement_analysis_prompt(requirements: str) -> str:
    return f"Analyze these software requirements and list scope, actors, modules, and risks:\n{requirements}"


def uml_generation_prompt(requirements: str) -> str:
    return f"Generate a valid Mermaid classDiagram for these requirements. Return only Mermaid syntax:\n{requirements}"


def erd_generation_prompt(requirements: str) -> str:
    return f"Generate a valid Mermaid erDiagram for these requirements. Return only Mermaid syntax:\n{requirements}"


def database_schema_prompt(requirements: str) -> str:
    return f"Generate normalized SQL CREATE TABLE statements for these requirements:\n{requirements}"


def code_skeleton_prompt(requirements: str) -> str:
    return f"Generate beginner-friendly starter code skeleton for these requirements:\n{requirements}"
