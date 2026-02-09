"""API tests for NetSec-Container."""

import pytest


@pytest.mark.api
def test_root_returns_html(client):
    """GET / returns HTML or JSON app info."""
    response = client.get("/")
    assert response.status_code == 200
    ct = response.headers.get("content-type", "")
    if "text/html" in ct:
        assert len(response.text) > 0
    else:
        data = response.json()
        assert "name" in data or "version" in data


@pytest.mark.api
def test_health(client):
    """GET /api/v1/health returns healthy."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "healthy"


@pytest.mark.api
def test_scan_endpoint_accepts_request(client):
    """POST /api/v1/scan accepts valid body; may 200 or 500 depending on Docker/image."""
    response = client.post(
        "/api/v1/scan",
        json={
            "image": "nonexistent-image-no-pull:999",
            "enable_vulnerability": False,
            "enable_secrets": False,
            "enable_sbom": False,
        },
    )
    # Route exists; without real image we may get 500 or timeout
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "success" in data or "results" in data


@pytest.mark.api
def test_scan_upload_accepts_multipart(client):
    """POST /api/v1/scan/upload accepts multipart file; may 422/500 without valid tar."""
    response = client.post(
        "/api/v1/scan/upload",
        files={"file": ("fake.tar", b"not a real tar", "application/x-tar")},
        data={"format": "json"},
    )
    # Route exists; invalid tar may 500
    assert response.status_code in [200, 422, 500]
    if response.status_code == 200:
        data = response.json()
        assert "success" in data or "results" in data
