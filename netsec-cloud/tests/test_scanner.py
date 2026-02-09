"""Tests for cloud scanner."""

import pytest
from netsec_cloud.scanner import CloudScanner


@pytest.mark.unit
def test_scanner_initialization(scanner):
    """Test scanner initialization using shared fixture."""
    assert scanner is not None
    assert scanner.providers == {}


def test_scanner_initialization_standalone():
    """Test scanner initialization without fixture."""
    s = CloudScanner()
    assert s is not None
    assert s.providers == {}


@pytest.mark.unit
def test_scanner_add_provider():
    """Test adding provider to scanner."""
    scanner = CloudScanner()
    # Will fail without valid credentials, but should not crash
    result = scanner.add_provider("aws", {})
    # Result depends on credentials availability
    assert isinstance(result, bool)


@pytest.mark.unit
def test_scanner_list_providers(scanner):
    """Test listing providers."""
    providers = scanner.list_providers()
    assert isinstance(providers, list)


@pytest.mark.unit
def test_scanner_get_summary(scanner):
    """Test getting scan summary."""
    summary = scanner.get_summary({})
    assert "total_findings" in summary
    assert "by_severity" in summary
    assert "by_type" in summary
