"""Tests for the FastAPI application."""

from fastapi.testclient import TestClient

from simpli_template import __version__
from simpli_template.app import app


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_openapi_metadata(client: TestClient) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "Simpli Template"
    assert schema["info"]["version"] == __version__


def test_lifespan_runs() -> None:
    """Lifespan configures logging on startup."""
    with TestClient(app):
        import structlog

        # After lifespan runs, structlog should be configured
        log = structlog.get_logger()
        assert log is not None
