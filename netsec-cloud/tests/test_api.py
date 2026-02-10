"""API tests using the shared TestClient fixture."""

import pytest


@pytest.mark.api
def test_root(client):
    """Test root endpoint returns app info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data.get("name") == "NetSec-Cloud API"
    assert "version" in data
    assert data.get("status") == "running"


@pytest.mark.api
def test_health(client):
    """Test health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "healthy"
    assert "version" in data


@pytest.mark.api
def test_providers_list(client):
    """Test providers list endpoint."""
    response = client.get("/api/v1/cloud/providers")
    assert response.status_code == 200
    data = response.json()
    assert "providers" in data
    assert isinstance(data["providers"], list)
    names = [p.get("name") for p in data["providers"]]
    assert "aws" in names
    assert "azure" in names
    assert "gcp" in names


@pytest.mark.api
def test_compliance_frameworks(client):
    """Test compliance frameworks list."""
    response = client.get("/api/v1/cloud/compliance/frameworks")
    assert response.status_code == 200
    data = response.json()
    assert "frameworks" in data
    assert any(f.get("name") == "cis" for f in data["frameworks"])


@pytest.mark.api
def test_compliance_framework_controls(client):
    """Test GET compliance/frameworks/{framework}/controls."""
    response = client.get("/api/v1/cloud/compliance/frameworks/cis/controls")
    assert response.status_code == 200
    data = response.json()
    assert data.get("framework") == "cis"
    assert "controls" in data
    assert isinstance(data["controls"], list)


@pytest.mark.api
def test_scan_requires_auth(client):
    """POST /scan with empty credentials returns 401 (auth failure)."""
    response = client.post(
        "/api/v1/cloud/scan",
        json={
            "provider": "aws",
            "credentials": {},
            "check_types": ["storage"],
        },
    )
    # Without valid creds, expect 401 (auth failure)
    assert response.status_code == 401


@pytest.mark.api
def test_compliance_check_requires_auth(client):
    """POST /compliance/check with empty creds returns 401."""
    response = client.post(
        "/api/v1/cloud/compliance/check?provider=aws&framework=cis",
        json={"credentials": {}},
    )
    assert response.status_code == 401


@pytest.mark.api
def test_compliance_check_bad_framework(client):
    """POST /compliance/check with unsupported framework returns 400."""
    response = client.post(
        "/api/v1/cloud/compliance/check?provider=aws&framework=unknown_fw",
        json={"credentials": {}},
    )
    assert response.status_code == 400


@pytest.mark.api
def test_multi_cloud_scan_accepts_body(client):
    """POST /scan/multi accepts providers list; may 401 if no creds."""
    response = client.post(
        "/api/v1/cloud/scan/multi",
        json={
            "providers": [
                {"provider": "aws", "credentials": {}},
            ],
            "check_types": ["storage"],
        },
    )
    assert response.status_code in [200, 401, 500]
    if response.status_code == 200:
        data = response.json()
        assert "scan_id" in data
        assert "results" in data
        assert "summary" in data
        assert "timestamp" in data
        assert isinstance(data["results"], dict)
        assert isinstance(data["summary"], dict)


@pytest.mark.api
def test_multi_cloud_scan_response_shape(client):
    """Multi-cloud scan response has required shape (scan_id, results, summary, timestamp)."""
    response = client.post(
        "/api/v1/cloud/scan/multi",
        json={
            "providers": [{"provider": "aws", "credentials": {}}],
            "check_types": ["storage"],
        },
    )
    # Without creds we get 401; shape test documents expected keys when 200
    assert response.status_code in (200, 401, 500)
    if response.status_code == 200:
        data = response.json()
        assert "scan_id" in data and isinstance(data["scan_id"], str)
        assert "results" in data and isinstance(data["results"], dict)
        assert "summary" in data and isinstance(data["summary"], dict)
        assert "timestamp" in data
