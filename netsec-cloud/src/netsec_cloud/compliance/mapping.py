"""Map security findings to compliance framework controls (CIS, NIST, etc.)."""

from typing import List, Dict, Any, Optional

# Finding type -> CIS control ID (CIS AWS/Azure/GCP Benchmark style)
# Format: control_id, control_title (short)
CIS_MAPPING: Dict[str, Dict[str, Any]] = {
    # Storage
    "s3_public_access": {"control_id": "2.1.1", "title": "S3 Block Public Access", "framework": "cis"},
    "s3_no_encryption": {"control_id": "2.1.2", "title": "S3 Bucket Encryption", "framework": "cis"},
    "s3_no_versioning": {"control_id": "2.1.3", "title": "S3 Versioning", "framework": "cis"},
    "storage_public_access": {"control_id": "3.1", "title": "Storage Public Access", "framework": "cis"},
    "storage_no_encryption": {"control_id": "3.2", "title": "Storage Encryption", "framework": "cis"},
    "storage_no_versioning": {"control_id": "3.3", "title": "Storage Versioning", "framework": "cis"},
    # IAM
    "iam_root_access_keys": {"control_id": "1.4", "title": "Root Access Keys Inactive", "framework": "cis"},
    "iam_no_mfa": {"control_id": "1.10", "title": "MFA for Console Access", "framework": "cis"},
    "iam_overprivileged": {"control_id": "1.16", "title": "Least Privilege IAM Policies", "framework": "cis"},
    "rbac_broad_role": {"control_id": "1.1", "title": "Azure RBAC Least Privilege", "framework": "cis"},
    "rbac_sp_owner": {"control_id": "1.2", "title": "Azure SP No Owner", "framework": "cis"},
    "iam_broad_role": {"control_id": "1.4", "title": "GCP IAM Least Privilege", "framework": "cis"},
    "iam_sa_owner": {"control_id": "1.5", "title": "GCP SA No Owner", "framework": "cis"},
    # Networking
    "security_group_open": {"control_id": "4.1", "title": "Restrict Security Group Rules", "framework": "cis"},
    "nsg_open_rule": {"control_id": "6.1", "title": "NSG Restrict Inbound", "framework": "cis"},
    "firewall_open_rule": {"control_id": "3.7", "title": "Firewall Restrict Inbound", "framework": "cis"},
    # Compute
    "ec2_imdsv1": {"control_id": "4.2", "title": "EC2 IMDSv2 Required", "framework": "cis"},
    "ec2_public_ip": {"control_id": "4.3", "title": "EC2 Public Exposure", "framework": "cis"},
    "ebs_unencrypted": {"control_id": "4.4", "title": "EBS Encryption", "framework": "cis"},
    # Audit
    "cloudtrail_disabled": {"control_id": "3.1", "title": "CloudTrail Enabled", "framework": "cis"},
    "cloudtrail_not_logging": {"control_id": "3.2", "title": "CloudTrail Logging", "framework": "cis"},
    # Errors (informational only)
    "scan_error": {"control_id": "N/A", "title": "Scan Error", "framework": "cis"},
}

# NIST CSF subcategory mapping (simplified)
NIST_MAPPING: Dict[str, str] = {
    "s3_public_access": "PR.AC-5",
    "s3_no_encryption": "PR.DS-1",
    "storage_public_access": "PR.AC-5",
    "storage_no_encryption": "PR.DS-1",
    "iam_root_access_keys": "PR.AC-4",
    "iam_no_mfa": "PR.AC-7",
    "iam_overprivileged": "PR.AC-4",
    "rbac_broad_role": "PR.AC-4",
    "rbac_sp_owner": "PR.AC-4",
    "iam_broad_role": "PR.AC-4",
    "iam_sa_owner": "PR.AC-4",
    "security_group_open": "PR.AC-5",
    "nsg_open_rule": "PR.AC-5",
    "firewall_open_rule": "PR.AC-5",
    "ec2_imdsv1": "PR.IP-1",
    "ebs_unencrypted": "PR.DS-1",
    "cloudtrail_disabled": "DE.CM-1",
    "cloudtrail_not_logging": "DE.CM-1",
}

# PCI-DSS (simplified; finding type -> requirement id)
PCI_DSS_MAPPING: Dict[str, str] = {
    "s3_public_access": "3.4",
    "s3_no_encryption": "3.4",
    "storage_public_access": "3.4",
    "storage_no_encryption": "3.4",
    "iam_root_access_keys": "7.1",
    "iam_no_mfa": "8.2",
    "iam_overprivileged": "7.1",
    "rbac_broad_role": "7.1",
    "rbac_sp_owner": "7.1",
    "iam_broad_role": "7.1",
    "iam_sa_owner": "7.1",
    "security_group_open": "1.2",
    "nsg_open_rule": "1.2",
    "firewall_open_rule": "1.2",
    "ec2_imdsv1": "2.2",
    "ebs_unencrypted": "3.4",
    "cloudtrail_disabled": "10.2",
    "cloudtrail_not_logging": "10.2",
}

# HIPAA (simplified; finding type -> safeguard)
HIPAA_MAPPING: Dict[str, str] = {
    "s3_public_access": "Access Control",
    "s3_no_encryption": "Encryption",
    "storage_public_access": "Access Control",
    "storage_no_encryption": "Encryption",
    "iam_root_access_keys": "Access Control",
    "iam_no_mfa": "Access Control",
    "iam_overprivileged": "Access Control",
    "rbac_broad_role": "Access Control",
    "rbac_sp_owner": "Access Control",
    "iam_broad_role": "Access Control",
    "iam_sa_owner": "Access Control",
    "security_group_open": "Access Control",
    "nsg_open_rule": "Access Control",
    "firewall_open_rule": "Access Control",
    "ec2_imdsv1": "Integrity",
    "ebs_unencrypted": "Encryption",
    "cloudtrail_disabled": "Audit Controls",
    "cloudtrail_not_logging": "Audit Controls",
}


def map_findings_to_cis(findings: List[Any]) -> List[Dict[str, Any]]:
    """
    Map a list of Finding-like objects (with .type, .finding_id, .severity) to CIS controls.

    Returns list of control results: control_id, title, status (failed if any finding maps to it).
    """
    return map_findings_to_framework(findings, "cis")


def map_findings_to_framework(
    findings: List[Any],
    framework: str,
) -> List[Dict[str, Any]]:
    """
    Map findings to a compliance framework (cis, nist).

    Args:
        findings: List of objects with .type, .finding_id, .severity
        framework: "cis" or "nist"

    Returns:
        List of control result dicts with control_id, control_title, status, finding_ids, etc.
    """
    framework_lower = framework.lower()
    if framework_lower == "nist":
        mapping = NIST_MAPPING
        control_title_key = "subcategory"
    elif framework_lower == "pci_dss":
        mapping = PCI_DSS_MAPPING
        control_title_key = "title"
    elif framework_lower == "hipaa":
        mapping = HIPAA_MAPPING
        control_title_key = "title"
    else:
        mapping = CIS_MAPPING
        control_title_key = "title"

    # Build control_id -> list of finding ids and max severity
    control_findings: Dict[str, Dict[str, Any]] = {}

    for f in findings:
        finding_type = getattr(f, "type", None) or (f.get("type") if isinstance(f, dict) else None)
        finding_id = getattr(f, "finding_id", None) or (f.get("finding_id") if isinstance(f, dict) else None)
        severity = getattr(f, "severity", None) or (f.get("severity") if isinstance(f, dict) else None)

        if not finding_type or finding_type == "scan_error":
            continue

        if framework_lower == "nist":
            control_id = mapping.get(finding_type)
            control_title = control_id or "Other"
        elif framework_lower in ("pci_dss", "hipaa"):
            control_id = mapping.get(finding_type, "N/A")
            control_title = control_id if framework_lower == "pci_dss" else mapping.get(finding_type, "Other")
        else:
            info = mapping.get(finding_type)
            if not info:
                continue
            control_id = info.get("control_id", "N/A")
            control_title = info.get("title", finding_type)

        if framework_lower in ("pci_dss", "hipaa") and not mapping.get(finding_type):
            continue
        key = f"{control_id}:{control_title}"
        if key not in control_findings:
            control_findings[key] = {
                "control_id": control_id,
                "control_title": control_title,
                "finding_ids": [],
                "max_severity": "info",
            }
        control_findings[key]["finding_ids"].append(finding_id or "")
        if severity:
            curr = control_findings[key]["max_severity"]
            order = ["info", "low", "medium", "high", "critical"]
            try:
                if severity in order and (curr not in order or order.index(severity) > order.index(curr)):
                    control_findings[key]["max_severity"] = severity
            except (ValueError, KeyError):
                pass

    results = []
    for data in control_findings.values():
        results.append({
            "control_id": data["control_id"],
            "control_title": data["control_title"],
            "framework": framework_lower,
            "status": "failed" if data["finding_ids"] else "passed",
            "finding_ids": data["finding_ids"],
            "finding_count": len(data["finding_ids"]),
            "severity": data.get("max_severity"),
        })
    results.sort(key=lambda x: (x["control_id"], x["control_title"]))
    return results


def get_framework_controls(framework: str) -> List[Dict[str, str]]:
    """Return list of known controls for a framework (for display)."""
    framework_lower = framework.lower()
    if framework_lower == "cis":
        return [
            {"control_id": v["control_id"], "title": v["title"]}
            for v in CIS_MAPPING.values()
            if v.get("control_id") != "N/A"
        ]
    if framework_lower == "nist":
        return [
            {"control_id": k, "title": k}
            for k in sorted(set(NIST_MAPPING.values()))
        ]
    if framework_lower == "pci_dss":
        return [
            {"control_id": k, "title": k}
            for k in sorted(set(PCI_DSS_MAPPING.values()))
        ]
    if framework_lower == "hipaa":
        return [
            {"control_id": k, "title": k}
            for k in sorted(set(HIPAA_MAPPING.values()))
        ]
    return []
