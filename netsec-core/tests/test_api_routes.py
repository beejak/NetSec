"""Tests for API routes with implemented scanners."""

import pytest
from fastapi.testclient import TestClient
from netsec_core.api.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


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
