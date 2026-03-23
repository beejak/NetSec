"""Unit tests for TrafficAnalyzer (no live capture)."""

import pytest
from unittest.mock import patch

try:
    from netsec_core.core.traffic_analyzer import TrafficAnalyzer, SCAPY_AVAILABLE
except ImportError:
    TrafficAnalyzer = None
    SCAPY_AVAILABLE = False


@pytest.mark.unit
def test_traffic_analyzer_import_error_without_scapy():
    """When scapy is not available, TrafficAnalyzer() raises ImportError."""
    if SCAPY_AVAILABLE:
        pytest.skip("scapy is available in this environment")
    if TrafficAnalyzer is None:
        pytest.skip("traffic_analyzer module did not import")
    with pytest.raises(ImportError):
        TrafficAnalyzer()


@pytest.mark.unit
def test_traffic_analyzer_init():
    """TrafficAnalyzer initializes correctly when SCAPY_AVAILABLE is True.

    The @skipif decorator was removed because it captures SCAPY_AVAILABLE=False
    at module-import time and cannot be overridden at runtime. Patching the
    module-level variable inside the test body works because __init__ reads it
    at call time, not at decoration time.
    """
    if TrafficAnalyzer is None:
        pytest.skip("traffic_analyzer module did not import")
    with patch("netsec_core.core.traffic_analyzer.SCAPY_AVAILABLE", True):
        analyzer = TrafficAnalyzer()
    assert analyzer is not None
    assert analyzer.capturing is False
    assert analyzer.packets == []
    assert len(analyzer.flows) == 0


@pytest.mark.unit
def test_analyze_traffic_no_packets_returns_error():
    """analyze_traffic with no captured packets returns error dict."""
    if TrafficAnalyzer is None:
        pytest.skip("traffic_analyzer module did not import")
    with patch("netsec_core.core.traffic_analyzer.SCAPY_AVAILABLE", True):
        analyzer = TrafficAnalyzer()
        result = analyzer.analyze_traffic()
    assert "error" in result
    assert "No packets" in result["error"]


@pytest.mark.unit
def test_analyze_traffic_pcap_not_implemented():
    """analyze_traffic with pcap_file returns not implemented."""
    if TrafficAnalyzer is None:
        pytest.skip("traffic_analyzer module did not import")
    with patch("netsec_core.core.traffic_analyzer.SCAPY_AVAILABLE", True):
        analyzer = TrafficAnalyzer()
        result = analyzer.analyze_traffic(pcap_file="/tmp/foo.pcap")
    assert "error" in result
    assert "not yet implemented" in result["error"]
