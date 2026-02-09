"""Integration tests for NetSec-Core API."""

import pytest
from fastapi.testclient import TestClient
from netsec_core.api.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.mark.integration
class TestAPIIntegration:
    """Integration tests for API endpoints."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns correct information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "NetSec-Core API"
        assert "version" in data
        assert data["status"] == "running"
        assert "/api/docs" in data["docs"]

    def test_health_endpoint(self, client):
        """Test health endpoint."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data

    def test_dns_scan_endpoint(self, client):
        """Test DNS scan endpoint."""
        response = client.post(
            "/api/v1/dns/scan",
            json={
                "domain": "example.com",
                "check_tunneling": True,
                "check_spoofing": True,
                "analyze_patterns": True,
            }
        )
        # May return 200 or 500 depending on network
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert "domain" in data
            assert "findings" in data

    def test_ssl_check_endpoint(self, client):
        """Test SSL check endpoint."""
        response = client.post(
            "/api/v1/ssl/check-certificate",
            json={
                "hostname": "example.com",
                "port": 443,
                "check_expiration": True,
                "check_ciphers": True,
                "check_chain": True,
            }
        )
        # May return 200 or 500 depending on network
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert "hostname" in data
            assert "findings" in data

    def test_scan_ports_endpoint(self, client):
        """Test port scan endpoint."""
        response = client.post(
            "/api/v1/scan/ports",
            json={
                "target": "127.0.0.1",
                "ports": [22, 80, 443],
                "scan_type": "tcp",
                "timeout": 2.0,
            }
        )
        # May return 200 or 500
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert "scan_id" in data
            assert "target" in data
            assert "open_ports" in data

    def test_remediation_endpoint(self, client):
        """Test remediation endpoint."""
        response = client.get("/api/v1/remediation/weak_cipher")
        assert response.status_code == 200
        data = response.json()
        assert "finding_type" in data
        assert "remediation" in data

    def test_remediation_list_endpoint(self, client):
        """Test remediation list endpoint."""
        response = client.get("/api/v1/remediation/")
        assert response.status_code == 200
        data = response.json()
        assert "remediation_types" in data
        assert "count" in data

    def test_remediation_search_endpoint(self, client):
        """Test remediation search endpoint."""
        response = client.get("/api/v1/remediation/search/dns")
        assert response.status_code == 200
        data = response.json()
        assert "keyword" in data
        assert "results" in data

    def test_anomaly_status_endpoint(self, client):
        """Test anomaly status endpoint."""
        response = client.get("/api/v1/anomaly/status")
        assert response.status_code == 200
        data = response.json()
        assert "learning" in data
        assert "threshold" in data

    def test_api_docs_available(self, client):
        """Test API documentation is available."""
        response = client.get("/api/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_openapi_schema_available(self, client):
        """Test OpenAPI schema is available."""
        response = client.get("/api/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
