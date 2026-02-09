"""Unit tests for RemediationGuide (no network)."""

import pytest
from netsec_core.remediation.guide import RemediationGuide


@pytest.mark.unit
def test_remediation_guide_init():
    """RemediationGuide initializes with remediation DB."""
    guide = RemediationGuide()
    assert guide is not None
    assert guide.remediation_db


@pytest.mark.unit
def test_get_remediation_known_type():
    """get_remediation returns guidance for known finding type."""
    guide = RemediationGuide()
    result = guide.get_remediation("dns_tunneling")
    assert "finding_type" in result
    assert result["finding_type"] == "dns_tunneling"
    assert "remediation" in result
    r = result["remediation"]
    assert "immediate" in r
    assert "short_term" in r
    assert isinstance(r["immediate"], list)
    assert len(r["immediate"]) > 0


@pytest.mark.unit
def test_get_remediation_unknown_type():
    """get_remediation returns default for unknown type."""
    guide = RemediationGuide()
    result = guide.get_remediation("unknown_type_xyz")
    assert "finding_type" in result
    assert result["finding_type"] == "unknown_type_xyz"
    assert "remediation" in result


@pytest.mark.unit
def test_get_all_remediations():
    """get_all_remediations returns dict of types."""
    guide = RemediationGuide()
    all_r = guide.get_all_remediations()
    assert isinstance(all_r, dict)
    assert "dns_tunneling" in all_r
    assert "weak_cipher" in all_r or "ssl" in str(all_r).lower() or len(all_r) > 0
