"""Tests for API models."""

from datetime import datetime
from netsec_core.api.models import (
    ScanRequest,
    ScanResult,
    Finding,
    Severity,
    DNSScanRequest,
    SSLCheckRequest,
)


def test_scan_request():
    """Test ScanRequest model."""
    request = ScanRequest(target="example.com", ports=[80, 443])
    assert request.target == "example.com"
    assert request.ports == [80, 443]
    assert request.scan_type == "tcp"


def test_scan_result():
    """Test ScanResult model."""
    result = ScanResult(
        scan_id="test-123",
        target="example.com",
        open_ports=[80, 443],
    )
    assert result.scan_id == "test-123"
    assert result.target == "example.com"
    assert result.open_ports == [80, 443]
    assert isinstance(result.timestamp, datetime)


def test_finding():
    """Test Finding model."""
    finding = Finding(
        finding_id="find-123",
        type="vulnerability",
        severity=Severity.HIGH,
        description="Test finding",
    )
    assert finding.finding_id == "find-123"
    assert finding.severity == Severity.HIGH
    assert finding.description == "Test finding"


def test_dns_scan_request():
    """Test DNSScanRequest model."""
    request = DNSScanRequest(domain="example.com")
    assert request.domain == "example.com"
    assert request.check_tunneling is True


def test_ssl_check_request():
    """Test SSLCheckRequest model."""
    request = SSLCheckRequest(hostname="example.com", port=443)
    assert request.hostname == "example.com"
    assert request.port == 443
    assert request.check_expiration is True
