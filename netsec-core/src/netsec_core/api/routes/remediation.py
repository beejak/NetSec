"""Remediation guidance routes."""

from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, Any
from netsec_core.remediation.guide import RemediationGuide

router = APIRouter()
guide = RemediationGuide()


@router.get("/{finding_type}")
async def get_remediation(finding_type: str):
    """Get remediation guidance for a finding type."""
    try:
        remediation = guide.get_remediation(finding_type)
        return remediation
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting remediation: {str(e)}",
        )


@router.post("/")
async def get_remediation_for_finding(finding: Dict[str, Any]):
    """Get remediation guidance for a specific finding."""
    try:
        finding_type = finding.get("type", "")
        remediation = guide.get_remediation(finding_type, finding)
        return remediation
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting remediation: {str(e)}",
        )


@router.get("/")
async def list_remediations():
    """List all available remediation types."""
    try:
        remediations = guide.get_all_remediations()
        return {
            "remediation_types": list(remediations.keys()),
            "count": len(remediations),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing remediations: {str(e)}",
        )


@router.get("/search/{keyword}")
async def search_remediations(keyword: str):
    """Search remediations by keyword."""
    try:
        results = guide.search_remediation(keyword)
        return {
            "keyword": keyword,
            "results": results,
            "count": len(results),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching remediations: {str(e)}",
        )
