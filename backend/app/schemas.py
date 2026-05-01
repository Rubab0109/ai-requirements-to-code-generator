"""Pydantic request/response schemas."""
from pydantic import BaseModel, Field
from typing import Any


class GenerateRequest(BaseModel):
    title: str | None = Field(default=None, max_length=120)
    requirements: str = Field(..., min_length=1, description="Raw software requirements entered by user")


class ProjectSummary(BaseModel):
    id: int
    title: str
    requirements_preview: str
    created_at: str


class GenerateResponse(BaseModel):
    id: int
    title: str
    requirements: str
    generated: dict[str, Any]
    created_at: str
