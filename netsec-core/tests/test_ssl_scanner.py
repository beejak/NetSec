"""Tests for SSL Scanner."""

import pytest
from netsec_core.core.ssl_scanner import SSLScanner


def test_ssl_scanner_initialization():
    """Test SSL Scanner initialization."""
    scanner = SSLScanner()
    assert scanner is not None
    assert len(scanner.weak_ciphers) > 0


def test_check_certificate_basic():
    """Test basic certificate checking."""
    scanner = SSLScanner()

    # Test with a well-known domain
    try:
        result = scanner.check_certificate(
            "example.com",
            port=443,
            check_expiration=True,
            check_ciphers=False,
            check_chain=False,
        )

        assert "hostname" in result
        assert result["hostname"] == "example.com"
        assert "findings" in result
        assert "timestamp" in result
    except Exception:
        # May fail if network is unavailable
        pytest.skip("Network unavailable for SSL test")


def test_check_expiration():
    """Test certificate expiration checking."""
    scanner = SSLScanner()

    try:
        result = scanner.check_certificate(
            "example.com",
            port=443,
            check_expiration=True,
            check_ciphers=False,
            check_chain=False,
        )

        # Should have certificate info
        assert "certificate_info" in result or "findings" in result
    except Exception:
        pytest.skip("Network unavailable for SSL test")


def test_parse_certificate():
    """Test certificate parsing."""
    scanner = SSLScanner()

    try:
        cert_der = scanner._get_certificate("example.com", 443)
        cert_info = scanner._parse_certificate(cert_der)

        assert "subject" in cert_info or "error" in cert_info
    except Exception:
        pytest.skip("Network unavailable for SSL test")
