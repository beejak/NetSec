"""Tests for compliance mapping."""

import pytest
from netsec_cloud.compliance.mapping import (
    CIS_MAPPING,
    NIST_MAPPING,
    map_findings_to_cis,
    map_findings_to_framework,
    get_framework_controls,
)


class _MockFinding:
    def __init__(self, finding_id: str, type: str, severity: str = "high"):
        self.finding_id = finding_id
        self.type = type
        self.severity = severity


@pytest.mark.unit
def test_cis_mapping_has_expected_keys():
    """CIS mapping includes storage, IAM, networking, compute types."""
    assert "s3_public_access" in CIS_MAPPING
    assert "iam_no_mfa" in CIS_MAPPING
    assert "security_group_open" in CIS_MAPPING
    assert "ec2_imdsv1" in CIS_MAPPING


@pytest.mark.unit
def test_map_findings_to_cis_empty():
    """Empty findings yield empty control results."""
    result = map_findings_to_cis([])
    assert result == []


def test_map_findings_to_cis_single():
    """Single finding maps to one failed control."""
    findings = [_MockFinding("f1", "s3_public_access", "high")]
    result = map_findings_to_cis(findings)
    assert len(result) == 1
    assert result[0]["control_id"] == "2.1.1"
    assert result[0]["status"] == "failed"
    assert result[0]["finding_ids"] == ["f1"]
    assert result[0]["finding_count"] == 1


def test_map_findings_to_framework_nist():
    """Findings map to NIST subcategories."""
    findings = [_MockFinding("f1", "s3_public_access")]
    result = map_findings_to_framework(findings, "nist")
    assert len(result) >= 1
    failed = [r for r in result if r["status"] == "failed"]
    assert len(failed) >= 1
    assert failed[0]["framework"] == "nist"


def test_get_framework_controls_cis():
    """CIS controls list is non-empty."""
    controls = get_framework_controls("cis")
    assert isinstance(controls, list)
    assert len(controls) > 0
    assert all("control_id" in c and "title" in c for c in controls)


def test_get_framework_controls_nist():
    """NIST controls list is non-empty."""
    controls = get_framework_controls("nist")
    assert isinstance(controls, list)
    assert len(controls) > 0


def test_scan_error_findings_ignored():
    """Scan error findings are not mapped to controls."""
    findings = [_MockFinding("err1", "scan_error", "info")]
    result = map_findings_to_cis(findings)
    assert len(result) == 0


def test_iam_root_access_keys_in_mapping():
    """IAM root access keys finding type maps to CIS 1.4 and NIST."""
    assert "iam_root_access_keys" in CIS_MAPPING
    assert CIS_MAPPING["iam_root_access_keys"]["control_id"] == "1.4"
    assert "iam_root_access_keys" in NIST_MAPPING


def test_azure_rbac_and_gcp_iam_types_in_cis_mapping():
    """Azure RBAC and GCP IAM finding types map to CIS controls."""
    assert "rbac_broad_role" in CIS_MAPPING
    assert "rbac_sp_owner" in CIS_MAPPING
    assert "iam_broad_role" in CIS_MAPPING
    assert "iam_sa_owner" in CIS_MAPPING
    assert CIS_MAPPING["rbac_broad_role"]["control_id"] == "1.1"
    assert CIS_MAPPING["iam_broad_role"]["control_id"] == "1.4"


def test_map_rbac_finding_to_nist():
    """RBAC broad role maps to NIST PR.AC-4."""
    findings = [_MockFinding("f1", "rbac_broad_role")]
    result = map_findings_to_framework(findings, "nist")
    assert len(result) >= 1
    assert any(r["control_id"] == "PR.AC-4" for r in result)
