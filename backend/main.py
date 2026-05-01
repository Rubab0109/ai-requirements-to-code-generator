"""FastAPI entry point for AI Requirements-to-Code Generator."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app import database, llm_service
from app.schemas import GenerateRequest


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield


app = FastAPI(title=settings.APP_NAME, version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN, "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}


@app.post("/api/generate")
async def generate_project(payload: GenerateRequest):
    requirements = payload.requirements.strip()
    title = (payload.title or "Untitled Project").strip() or "Untitled Project"

    if not requirements:
        raise HTTPException(status_code=422, detail="Requirement input cannot be empty.")
    if len(requirements) < 30:
        raise HTTPException(status_code=400, detail="Requirement is too short. Please describe modules, users, and main workflow.")

    try:
        generated = await llm_service.generate_ai_project(requirements=requirements, title=title)
        project = database.create_project(title=title, requirements=requirements, generated=generated)
        return project
    except llm_service.LLMError as exc:
        raise HTTPException(status_code=503, detail=f"LLM service failed: {exc}") from exc


@app.get("/api/projects")
def list_previous_projects(limit: int = 25):
    return database.list_projects(limit=limit)


@app.get("/api/projects/{project_id}")
def get_previous_project(project_id: int):
    project = database.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.delete("/api/projects/{project_id}")
def delete_previous_project(project_id: int):
    deleted = database.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"deleted": True}
