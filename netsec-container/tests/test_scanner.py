"""Tests for container scanner."""

import pytest
from netsec_container.core.scanner import ContainerScanner


def test_scanner_initialization():
    """Test scanner initialization."""
    scanner = ContainerScanner()
    assert scanner is not None


def test_scanner_scan_image_placeholder():
    """Test scan_image method exists."""
    scanner = ContainerScanner()
    # This will fail without actual image, but tests the method exists
    assert hasattr(scanner, 'scan_image')
    assert callable(scanner.scan_image)


def test_scanner_generate_report():
    """Test generate_report method exists."""
    scanner = ContainerScanner()
    assert hasattr(scanner, 'generate_report')
    assert callable(scanner.generate_report)
