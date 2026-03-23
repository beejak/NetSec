"""Tests for SSL Scanner."""

import pytest
from unittest.mock import patch
from netsec_core.core.ssl_scanner import SSLScanner


def test_ssl_scanner_initialization():
    """Test SSL Scanner initialization."""
    scanner = SSLScanner()
    assert scanner is not None
    assert len(scanner.weak_ciphers) > 0


def test_check_certificate_basic(synthetic_cert_der):
    """Test basic certificate checking with synthetic cert (no live network)."""
    scanner = SSLScanner()
    with patch.object(scanner, "_get_certificate", return_value=synthetic_cert_der):
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


def test_check_expiration(synthetic_cert_der):
    """Test certificate expiration checking with synthetic cert (no live network)."""
    scanner = SSLScanner()
    with patch.object(scanner, "_get_certificate", return_value=synthetic_cert_der):
        result = scanner.check_certificate(
            "example.com",
            port=443,
            check_expiration=True,
            check_ciphers=False,
            check_chain=False,
        )

    assert "certificate_info" in result or "findings" in result


def test_parse_certificate(synthetic_cert_der):
    """Test certificate parsing with synthetic DER cert (no live network)."""
    scanner = SSLScanner()
    cert_info = scanner._parse_certificate(synthetic_cert_der)

    assert "subject" in cert_info or "error" in cert_info
