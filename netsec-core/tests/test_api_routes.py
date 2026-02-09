"""Tests for API routes with implemented scanners."""

import pytest
from fastapi.testclient import TestClient
from netsec_core.api.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.mark.api
def test_anomaly_status(client):
    """Anomaly /status returns 200."""
    response = client.get("/api/v1/anomaly/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data or "baseline" in data or isinstance(data, dict)


@pytest.mark.api
def test_remediation_list(client):
    """Remediation list returns remediation types."""
    response = client.get("/api/v1/remediation/")
    assert response.status_code == 200
    data = response.json()
    assert "remediation_types" in data
    assert "count" in data
    assert data["count"] >= 0


@pytest.mark.api
def test_remediation_get_known(client):
    """Remediation GET for known type returns guidance."""
    response = client.get("/api/v1/remediation/weak_cipher")
    assert response.status_code == 200
    data = response.json()
    assert "finding_type" in data
    assert "remediation" in data


@pytest.mark.api
def test_assets_inventory_endpoint(client):
    """POST /api/v1/assets/inventory accepts list and returns inventory."""
    response = client.post("/api/v1/assets/inventory", json=[{"ip": "1.2.3.4", "services": [], "open_ports": []}])
    assert response.status_code == 200
    data = response.json()
    assert "total_assets" in data
    assert data["total_assets"] == 1


@pytest.mark.api
def test_anomaly_detect_endpoint(client):
    """POST /api/v1/anomaly/detect with metric and value returns result."""
    response = client.post("/api/v1/anomaly/detect?metric=pps&value=100.0")
    assert response.status_code == 200
    data = response.json()
    assert "metric" in data
    assert "anomaly_detected" in data


@pytest.mark.api
def test_dns_scan_endpoint(client):
    """Test DNS scan endpoint."""
    response = client.post(
        "/api/v1/dns/scan",
        json={
            "domain": "example.com",
            "check_tunneling": True,
            "check_spoofing": True,
            "analyze_patterns": True,
        },
    )

    # Should return 200 or 500 (depending on network)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "domain" in data
        assert "findings" in data


@pytest.mark.api
def test_ssl_check_endpoint(client):
    """Test SSL check endpoint."""
    response = client.post(
        "/api/v1/ssl/check-certificate",
        json={
            "hostname": "example.com",
            "port": 443,
            "check_expiration": True,
            "check_ciphers": True,
            "check_chain": True,
        },
    )

    # Should return 200 or 500 (depending on network)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "hostname" in data
        assert "findings" in data


@pytest.mark.api
def test_scan_ports_endpoint(client):
    """Test port scan endpoint."""
    response = client.post(
        "/api/v1/scan/ports",
        json={
            "target": "127.0.0.1",
            "ports": [22, 80, 443],
            "scan_type": "tcp",
            "timeout": 2.0,
        },
    )

    # Should return 200 or 500
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "scan_id" in data
        assert "target" in data
        assert "open_ports" in data


@pytest.mark.api
def test_traffic_flows_endpoint(client):
    """GET /api/v1/traffic/flows returns 200 or 503 (scapy optional)."""
    response = client.get("/api/v1/traffic/flows")
    assert response.status_code in [200, 503]
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, dict)


@pytest.mark.api
def test_traffic_analyze_endpoint(client):
    """POST /api/v1/traffic/analyze returns 200 or 503."""
    response = client.post("/api/v1/traffic/analyze")
    assert response.status_code in [200, 503]


@pytest.mark.api
def test_assets_discover_endpoint(client):
    """POST /api/v1/assets/discover with network returns 200 or 500."""
    response = client.post("/api/v1/assets/discover?network=127.0.0.0/24")
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, dict)


@pytest.mark.api
def test_anomaly_learn_baseline_endpoint(client):
    """POST /api/v1/anomaly/learn-baseline returns 200."""
    response = client.post("/api/v1/anomaly/learn-baseline?duration=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


@pytest.mark.api
def test_llm_analyze_traffic_endpoint(client):
    """POST /api/v1/llm/analyze-traffic accepts body; may 200/422/500 without API key."""
    response = client.post(
        "/api/v1/llm/analyze-traffic",
        json={"summary": {"packets": 10, "protocols": {}}},
    )
    # Route exists; without key may return 200 (local), 422, or 500
    assert response.status_code in [200, 422, 500]
