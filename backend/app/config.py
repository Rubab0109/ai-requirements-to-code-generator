"""Application configuration loaded from .env.

Beginner note:
- Keep secret keys in backend/.env, never inside source code.
- The app can run in demo fallback mode when no API key is present.
"""
from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    """Typed settings for the backend."""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "AI Requirements-to-Code Generator"
    ENVIRONMENT: str = "development"
    FRONTEND_ORIGIN: str = "http://localhost:5173"

    # LLM provider: gemini | groq | openai
    LLM_PROVIDER: str = Field(default="gemini")
    LLM_TEMPERATURE: float = 0.2
    ALLOW_DEMO_FALLBACK: bool = True

    # Gemini REST API settings
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Groq OpenAI-compatible API settings
    GROQ_API_KEY: str | None = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # OpenAI Chat Completions API settings
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4.1-mini"

    # SQLite storage
    SQLITE_DB_PATH: str = str(BASE_DIR / "data" / "projects.db")


@lru_cache
def get_settings() -> Settings:
    return Settings()
