"""Tests for cloud scanner."""

import pytest
from netsec_cloud.scanner import CloudScanner


def test_scanner_initialization():
    """Test scanner initialization."""
    scanner = CloudScanner()
    assert scanner is not None
    assert scanner.providers == {}


def test_scanner_add_provider():
    """Test adding provider to scanner."""
    scanner = CloudScanner()
    # Will fail without valid credentials, but should not crash
    result = scanner.add_provider("aws", {})
    # Result depends on credentials availability
    assert isinstance(result, bool)


def test_scanner_list_providers():
    """Test listing providers."""
    scanner = CloudScanner()
    providers = scanner.list_providers()
    assert isinstance(providers, list)


def test_scanner_get_summary():
    """Test getting scan summary."""
    scanner = CloudScanner()
    summary = scanner.get_summary({})
    assert "total_findings" in summary
    assert "by_severity" in summary
    assert "by_type" in summary
