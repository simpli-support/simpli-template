"""Tests for data ingest endpoints."""

import io
import json

import pytest
from fastapi.testclient import TestClient


def test_ingest_csv(client: TestClient) -> None:
    csv_content = "subject,description\nPassword reset,I need help resetting\nBilling issue,Charge dispute\n"
    file = io.BytesIO(csv_content.encode())
    response = client.post(
        "/api/v1/ingest",
        files={"file": ("tickets.csv", file, "text/csv")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["processed"] == 2
    assert len(data["results"]) == 2


def test_ingest_json(client: TestClient) -> None:
    records = [
        {"subject": "Help needed", "description": "Cannot login"},
    ]
    file = io.BytesIO(json.dumps(records).encode())
    response = client.post(
        "/api/v1/ingest",
        files={"file": ("tickets.json", file, "application/json")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["processed"] == 1


def test_ingest_salesforce_missing_credentials(client: TestClient) -> None:
    response = client.post(
        "/api/v1/ingest/salesforce",
        json={"limit": 10},
    )
    assert response.status_code == 400
    assert "credentials" in response.json()["detail"].lower()
