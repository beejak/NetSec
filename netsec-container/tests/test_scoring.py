"""Unit tests for risk scoring."""

import pytest
from datetime import datetime
from netsec_container.core.results import ScanResults
from netsec_container.core.scoring import RiskScorer


@pytest.mark.unit
def test_risk_scorer_init():
    """RiskScorer initializes with severity weights."""
    scorer = RiskScorer()
    assert scorer is not None
    assert "critical" in scorer.severity_weights
    assert scorer.severity_weights["critical"] == 10.0


@pytest.mark.unit
def test_calculate_score_empty_results():
    """calculate_score with empty results returns low/zero score."""
    scorer = RiskScorer()
    results = ScanResults(
        image="test:latest",
        scan_start=datetime.utcnow(),
        vulnerabilities=[],
        secrets=[],
    )
    score = scorer.calculate_score(results)
    assert isinstance(score, (int, float))
    assert 0 <= score <= 100
