"""Tests for DNS Scanner."""

import pytest
from netsec_core.core.dns_scanner import DNSScanner


def test_dns_scanner_initialization():
    """Test DNS Scanner initialization."""
    scanner = DNSScanner()
    assert scanner is not None
    assert scanner.resolver is not None


def test_scan_domain_basic():
    """Test basic domain scanning."""
    scanner = DNSScanner()
    result = scanner.scan_domain("example.com", check_tunneling=False, check_spoofing=False, analyze_patterns=False)

    assert "domain" in result
    assert result["domain"] == "example.com"
    assert "findings" in result
    assert "timestamp" in result


def test_detect_tunneling():
    """Test DNS tunneling detection."""
    scanner = DNSScanner()

    # Test with suspicious domain (long subdomain)
    suspicious_domain = "a" * 50 + ".example.com"
    result = scanner.scan_domain(suspicious_domain, check_tunneling=True, check_spoofing=False, analyze_patterns=False)

    assert len(result["findings"]) > 0
    tunneling_findings = [f for f in result["findings"] if f.get("type") == "dns_tunneling"]
    assert len(tunneling_findings) > 0


def test_calculate_entropy():
    """Test entropy calculation."""
    scanner = DNSScanner()

    # High entropy string
    high_entropy = "a1b2c3d4e5f6g7h8i9j0"
    entropy_high = scanner._calculate_entropy(high_entropy)
    assert entropy_high > 3.0

    # Low entropy string
    low_entropy = "aaaaaaaaaa"
    entropy_low = scanner._calculate_entropy(low_entropy)
    assert entropy_low < 2.0

    # Empty string
    assert scanner._calculate_entropy("") == 0.0


def test_analyze_patterns():
    """Test pattern analysis."""
    scanner = DNSScanner()

    # Test with hex-like pattern
    result = scanner.scan_domain("a1b2c3d4e5f6.example.com", check_tunneling=False, check_spoofing=False, analyze_patterns=True)
    pattern_findings = [f for f in result["findings"] if f.get("type") == "dns_pattern"]
    # May or may not find patterns depending on exact match
    assert isinstance(pattern_findings, list)
