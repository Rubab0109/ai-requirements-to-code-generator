from fastapi.testclient import TestClient

from main import app
from app.mermaid_utils import sanitize_mermaid, validate_mermaid_light


client = TestClient(app)


def test_empty_requirement_input():
    response = client.post("/api/generate", json={"title": "Test", "requirements": "   "})
    assert response.status_code == 422


def test_very_short_requirement():
    response = client.post("/api/generate", json={"title": "Test", "requirements": "make app"})
    assert response.status_code == 400


def test_complex_requirement_uses_demo_fallback_when_no_key():
    response = client.post(
        "/api/generate",
        json={
            "title": "Campus Event Management",
            "requirements": "Build a campus event and society management system with student registration, admin approval, voucher generation, event reports, and role based dashboards.",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["generated"]["uml_mermaid"].startswith("classDiagram")
    assert data["generated"]["erd_mermaid"].startswith("erDiagram")


def test_api_failure_when_demo_disabled(monkeypatch):
    async def fake_failure(*args, **kwargs):
        from app.llm_service import LLMError

        raise LLMError("forced failure")

    monkeypatch.setattr("app.llm_service.generate_ai_project", fake_failure)
    response = client.post(
        "/api/generate",
        json={
            "title": "Failure Test",
            "requirements": "Build a complex inventory system with purchase orders, suppliers, products, stock audit, and reporting dashboards.",
        },
    )
    assert response.status_code == 503


def test_invalid_mermaid_output_handling():
    fallback = "classDiagram\n  class User"
    cleaned = sanitize_mermaid("Here is diagram:\nclassDiagram\n  class User", "classDiagram", fallback)
    ok, message = validate_mermaid_light(cleaned)
    assert ok is True
    assert message is None

    ok, message = validate_mermaid_light("This is not mermaid")
    assert ok is False
    assert "valid diagram keyword" in message
