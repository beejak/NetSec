"""Tests for Network Scanner."""

import pytest
from netsec_core.core.network_scanner import NetworkScanner


def test_network_scanner_initialization():
    """Test Network Scanner initialization."""
    scanner = NetworkScanner()
    assert scanner is not None
    assert scanner.timeout > 0
    assert scanner.max_workers > 0


def test_scan_port():
    """Test single port scanning."""
    scanner = NetworkScanner()

    # Test scanning a common port (may or may not be open)
    result = scanner._scan_port("127.0.0.1", 22, "tcp")

    assert "open" in result
    assert "port" in result
    assert result["port"] == 22
    assert isinstance(result["open"], bool)


def test_detect_service():
    """Test service detection."""
    scanner = NetworkScanner()

    # Test common ports
    assert scanner._detect_service(80) == "http"
    assert scanner._detect_service(443) == "https"
    assert scanner._detect_service(22) == "ssh"
    assert scanner._detect_service(25) == "smtp"

    # Test with banner
    banner = "SSH-2.0-OpenSSH"
    assert scanner._detect_service(2222, banner) == "ssh"


def test_scan_ports():
    """Test port scanning."""
    scanner = NetworkScanner()

    # Test scanning localhost (limited ports)
    result = scanner.scan_ports("127.0.0.1", ports=[22, 80, 443], scan_type="tcp", timeout=1.0)

    assert "scan_id" in result
    assert "target" in result
    assert result["target"] == "127.0.0.1"
    assert "open_ports" in result
    assert "services" in result
    assert isinstance(result["open_ports"], list)
    assert isinstance(result["services"], list)


def test_scan_services():
    """Test service scanning."""
    scanner = NetworkScanner()

    result = scanner.scan_services("127.0.0.1", ports=[22, 80])

    assert "scan_id" in result
    assert "services" in result
    assert isinstance(result["services"], list)
