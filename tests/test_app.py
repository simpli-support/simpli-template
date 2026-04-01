"""Tests for the FastAPI application."""

import pytest
from fastapi.testclient import TestClient

from simpli_template.app import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
