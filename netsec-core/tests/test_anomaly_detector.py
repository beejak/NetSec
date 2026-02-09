"""Unit tests for AnomalyDetector (no network)."""

import pytest
from netsec_core.core.anomaly_detector import AnomalyDetector


@pytest.mark.unit
def test_anomaly_detector_init():
    """AnomalyDetector initializes."""
    detector = AnomalyDetector()
    assert detector is not None
    assert detector.anomaly_threshold == 3.0
    assert not detector.learning


@pytest.mark.unit
def test_learn_baseline_returns_status():
    """learn_baseline returns learning status."""
    detector = AnomalyDetector()
    result = detector.learn_baseline(duration=60)
    assert "status" in result
    assert result["status"] == "learning"
    assert result["duration"] == 60
    assert "start_time" in result
    assert detector.learning is True


@pytest.mark.unit
def test_detect_anomalies_insufficient_baseline():
    """detect_anomalies returns no anomaly when baseline is empty."""
    detector = AnomalyDetector()
    result = detector.detect_anomalies(metric="packets_per_second", value=100.0)
    assert "anomaly_detected" in result
    assert result["anomaly_detected"] is False
    assert "reason" in result
    assert "Insufficient" in result["reason"]


@pytest.mark.unit
def test_detect_anomalies_with_baseline():
    """detect_anomalies with built baseline returns z-score and anomaly flag."""
    detector = AnomalyDetector()
    detector.learn_baseline(duration=3600)
    for i in range(10):
        detector.add_traffic_data("pps", 100.0 + i)
    # Manually set baseline so we don't wait for duration
    detector.baseline_data["pps"]["mean"] = 104.5
    detector.baseline_data["pps"]["std"] = 3.0
    detector.learning = False
    result = detector.detect_anomalies(metric="pps", value=200.0)
    assert "anomaly_detected" in result
    assert "z_score" in result
    assert result["z_score"] > 3.0
    assert result["anomaly_detected"] is True


@pytest.mark.unit
def test_get_status():
    """get_status returns status dict."""
    detector = AnomalyDetector()
    status = detector.get_status()
    assert "learning" in status
    assert "baseline_metrics" in status
    assert isinstance(status["baseline_metrics"], (list, dict))
