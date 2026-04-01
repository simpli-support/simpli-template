"""Tests for the FastAPI application."""

from fastapi.testclient import TestClient

from simpli_template.app import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
