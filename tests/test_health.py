"""Health endpoint tests for DeepTutor API."""

from fastapi.testclient import TestClient
from deeptutor.api.main import app


def test_health_endpoint():
    """GET /health returns ok status."""
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "version": "0.1.0"}


def test_root_endpoint():
    """GET / returns API root information."""
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "DeepTutor API"
    assert "version" in data
    assert "endpoints" in data
    # Root endpoints map surface names to paths
    endpoints = data["endpoints"]
    assert "health" in endpoints
    assert "/health" in endpoints.values() or endpoints.get("health") == "/health"
