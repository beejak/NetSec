"""Tests for health check API endpoints."""

from fastapi.testclient import TestClient
from netsec_core.api.main import app


def test_root_endpoint():
    """Test root endpoint."""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "NetSec-Core API"
    assert "version" in data
    assert data["status"] == "running"


def test_health_endpoint():
    """Test health check endpoint."""
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data
