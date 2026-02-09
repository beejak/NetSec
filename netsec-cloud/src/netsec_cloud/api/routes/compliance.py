"""Compliance checking routes."""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from datetime import datetime

from netsec_cloud.scanner import CloudScanner
from netsec_cloud.compliance.mapping import (
    map_findings_to_framework,
    get_framework_controls,
)

router = APIRouter()

SUPPORTED_FRAMEWORKS = ["cis", "nist", "pci_dss", "hipaa"]


@router.get("/frameworks")
async def list_frameworks():
    """List supported compliance frameworks."""
    return {
        "frameworks": [
            {
                "name": "cis",
                "display_name": "CIS Benchmarks",
                "description": "Center for Internet Security Benchmarks (AWS/Azure/GCP)",
                "supported_providers": ["aws", "azure", "gcp"],
                "implemented": True,
            },
            {
                "name": "nist",
                "display_name": "NIST CSF",
                "description": "NIST Cybersecurity Framework (subcategory mapping)",
                "supported_providers": ["aws", "azure", "gcp"],
                "implemented": True,
            },
            {
                "name": "pci_dss",
                "display_name": "PCI-DSS",
                "description": "Payment Card Industry Data Security Standard (finding-to-control mapping)",
                "supported_providers": ["aws", "azure", "gcp"],
                "implemented": True,
            },
            {
                "name": "hipaa",
                "display_name": "HIPAA",
                "description": "Health Insurance Portability and Accountability Act (finding-to-safeguard mapping)",
                "supported_providers": ["aws", "azure", "gcp"],
                "implemented": True,
            },
        ],
    }


@router.get("/frameworks/{framework}/controls")
async def list_framework_controls(framework: str):
    """List known controls for a compliance framework."""
    fw = framework.lower()
    if fw not in SUPPORTED_FRAMEWORKS:
        raise HTTPException(
            status_code=400,
            detail=f"Framework must be one of: {SUPPORTED_FRAMEWORKS}",
        )
    controls = get_framework_controls(fw)
    return {"framework": fw, "controls": controls}


@router.post("/check")
async def check_compliance(
    provider: str,
    framework: str,
    credentials: Dict[str, Any],
    regions: Optional[List[str]] = None,
    check_types: Optional[List[str]] = None,
):
    """
    Run a cloud scan and map findings to the given compliance framework.

    Runs storage, IAM, networking, and compute checks (or check_types if provided),
    then maps each finding to framework controls (CIS or NIST). Returns control-level
    pass/fail and which findings failed each control.
    """
    fw = framework.lower()
    if fw not in SUPPORTED_FRAMEWORKS:
        raise HTTPException(
            status_code=400,
            detail=f"Framework must be one of: {SUPPORTED_FRAMEWORKS}",
        )

    try:
        scanner = CloudScanner()
        success = scanner.add_provider(
            provider_name=provider.lower(),
            credentials=credentials,
            regions=regions,
        )
        if not success:
            raise HTTPException(
                status_code=401,
                detail=f"Failed to authenticate with provider: {provider}",
            )

        findings = scanner.scan_provider(
            provider_name=provider.lower(),
            check_types=check_types,
        )
        control_results = map_findings_to_framework(findings, fw)
        failed_count = sum(1 for c in control_results if c["status"] == "failed")
        passed_count = len(control_results) - failed_count

        return {
            "provider": provider.lower(),
            "framework": fw,
            "timestamp": datetime.utcnow().isoformat(),
            "findings_count": len(findings),
            "controls": control_results,
            "summary": {
                "total_controls_evaluated": len(control_results),
                "passed": passed_count,
                "failed": failed_count,
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Compliance check failed: {str(e)}",
        )
