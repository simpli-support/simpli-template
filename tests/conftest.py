"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient

from simpli_template.app import app


@pytest.fixture(autouse=True)
def _env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    """Prevent tests from reading the real .env file."""
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.delenv("APP_DEBUG", raising=False)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
