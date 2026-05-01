"""Deterministic demo generator.

This lets the full web prototype work even when the student has not configured
an API key yet. When a real key is present, llm_service.py calls the LLM API.
"""
from __future__ import annotations

from textwrap import dedent


def build_demo_response(requirements: str, title: str | None = None) -> dict:
    project_name = title or "Generated Software System"
    lower = requirements.lower()

    # Small keyword-based guesses to make the demo feel relevant.
    user_entity = "User"
    main_entity = "Project"
    if "event" in lower:
        main_entity = "Event"
    elif "attendance" in lower:
        main_entity = "Attendance"
    elif "ecommerce" in lower or "shop" in lower:
        main_entity = "Product"
    elif "library" in lower:
        main_entity = "Book"

    if "student" in lower:
        user_entity = "Student"
    elif "teacher" in lower:
        user_entity = "Teacher"
    elif "admin" in lower:
        user_entity = "AdminUser"

    return {
        "source": "demo-fallback",
        "warning": "No valid LLM API key was used. This is deterministic demo output. Configure .env for real AI generation.",
        "analysis": dedent(f"""
            {project_name} is a software system based on the submitted requirements. The system needs user-facing workflows, admin management, persistent records, and clear reporting. The main risk is requirement ambiguity, so the generated design separates core entities, service logic, database schema, and starter API/UI code.
        """).strip(),
        "assumptions": [
            "The system will have an admin role and at least one normal user role.",
            "Authentication is required for protected actions.",
            "Generated code is starter code and must be customized before production use.",
            "All important transactions are stored in a database for later reporting.",
        ],
        "functional_requirements": [
            f"Users can create and manage {main_entity.lower()} records.",
            "Admins can view, update, delete, and audit system records.",
            "System validates required fields before saving data.",
            "System provides searchable project/history records.",
            "System generates reports or summaries for admins.",
        ],
        "non_functional_requirements": [
            "Responsive UI for desktop and mobile screens.",
            "Secure API key handling through environment variables.",
            "Database persistence using SQLite for prototype deployment.",
            "Readable modular code structure for beginner developers.",
            "Graceful error handling for API and validation failures.",
        ],
        "uml_mermaid": dedent(f"""
            classDiagram
              class {user_entity} {{
                +int id
                +string name
                +string email
                +login()
              }}
              class Admin {{
                +int id
                +manageRecords()
                +viewReports()
              }}
              class {main_entity} {{
                +int id
                +string title
                +string status
                +DateTime createdAt
                +save()
                +update()
              }}
              class Report {{
                +int id
                +string type
                +DateTime generatedAt
                +exportPDF()
              }}
              {user_entity} "1" --> "many" {main_entity}
              Admin --> {main_entity}
              Admin --> Report
        """).strip(),
        "erd_mermaid": dedent(f"""
            erDiagram
              USERS ||--o{{ RECORDS : creates
              ADMINS ||--o{{ REPORTS : generates
              RECORDS ||--o{{ REPORTS : included_in
              USERS {{
                int id PK
                string name
                string email
                string password_hash
                string role
              }}
              ADMINS {{
                int id PK
                string name
                string email
              }}
              RECORDS {{
                int id PK
                int user_id FK
                string title
                string status
                datetime created_at
              }}
              REPORTS {{
                int id PK
                int record_id FK
                string report_type
                datetime generated_at
              }}
        """).strip(),
        "database_schema": dedent("""
            CREATE TABLE users (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              email TEXT UNIQUE NOT NULL,
              password_hash TEXT NOT NULL,
              role TEXT DEFAULT 'user',
              created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE records (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER NOT NULL,
              title TEXT NOT NULL,
              status TEXT DEFAULT 'pending',
              created_at TEXT DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE reports (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              record_id INTEGER NOT NULL,
              report_type TEXT NOT NULL,
              generated_at TEXT DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (record_id) REFERENCES records(id)
            );
        """).strip(),
        "code_skeleton": dedent('''
            # Starter FastAPI skeleton generated from requirements
            from fastapi import FastAPI, HTTPException
            from pydantic import BaseModel

            app = FastAPI(title="Generated Starter API")

            class RecordCreate(BaseModel):
                title: str
                status: str = "pending"

            records = []

            @app.get("/health")
            def health():
                return {"status": "ok"}

            @app.post("/records")
            def create_record(payload: RecordCreate):
                item = {"id": len(records) + 1, **payload.model_dump()}
                records.append(item)
                return item

            @app.get("/records")
            def list_records():
                return records

            @app.get("/records/{record_id}")
            def get_record(record_id: int):
                for item in records:
                    if item["id"] == record_id:
                        return item
                raise HTTPException(status_code=404, detail="Record not found")
        ''').strip(),
        "tech_stack": [
            "Frontend: React.js, Tailwind CSS, Mermaid.js",
            "Backend: FastAPI, Pydantic, HTTPX",
            "Database: SQLite for prototype storage",
            "AI: Gemini/Groq/OpenAI API through backend service",
            "Deployment: Vercel frontend + Render/Railway backend",
        ],
        "testing_notes": [
            "Test empty input returns validation error.",
            "Test very short input returns helpful message.",
            "Test complex input returns all required output sections.",
            "Test API failure returns safe error or demo fallback.",
            "Test Mermaid output starts with classDiagram or erDiagram.",
        ],
    }
