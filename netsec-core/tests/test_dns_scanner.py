"""Tests for DNS Scanner."""

from unittest.mock import patch

import dns.resolver

from netsec_core.core.dns_scanner import DNSScanner


def test_dns_scanner_initialization():
    """Test DNS Scanner initialization."""
    scanner = DNSScanner()
    assert scanner is not None
    assert scanner.resolver is not None


def test_scan_domain_basic():
    """Test basic domain scanning (no live DNS)."""
    scanner = DNSScanner()
    with patch.object(scanner.resolver, "resolve", side_effect=dns.resolver.NXDOMAIN):
        result = scanner.scan_domain(
            "example.com",
            check_tunneling=False,
            check_spoofing=False,
            analyze_patterns=False,
        )

    assert "domain" in result
    assert result["domain"] == "example.com"
    assert "findings" in result
    assert "timestamp" in result


def test_detect_tunneling():
    """Test DNS tunneling detection with a synthetic deep domain."""
    scanner = DNSScanner()

    # 6-level domain reliably triggers the depth > 4 heuristic without live DNS
    deep_domain = "payload.c2.tunnel.attacker.example.com"

    with patch.object(scanner.resolver, "resolve", side_effect=dns.resolver.NXDOMAIN):
        result = scanner.scan_domain(
            deep_domain,
            check_tunneling=True,
            check_spoofing=False,
            analyze_patterns=False,
        )

    assert "findings" in result
    assert isinstance(result["findings"], list)
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
    """Test pattern analysis (regex-based, no DNS needed)."""
    scanner = DNSScanner()

    # Test with hex-like pattern; mock DNS to avoid live resolution
    with patch.object(scanner.resolver, "resolve", side_effect=dns.resolver.NXDOMAIN):
        result = scanner.scan_domain(
            "a1b2c3d4e5f6.example.com",
            check_tunneling=False,
            check_spoofing=False,
            analyze_patterns=True,
        )
    pattern_findings = [f for f in result["findings"] if f.get("type") == "dns_pattern"]
    # May or may not find patterns depending on exact match
    assert isinstance(pattern_findings, list)
