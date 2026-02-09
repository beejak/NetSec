"""Cloud scanning routes."""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from datetime import datetime, timezone
import uuid

from netsec_cloud.api.models import (
    ScanRequest,
    ScanResponse,
    MultiCloudScanRequest,
    MultiCloudScanResponse,
    FindingModel,
)
from netsec_cloud.scanner import CloudScanner

router = APIRouter()


@router.post("/scan", response_model=ScanResponse)
async def scan_cloud(request: ScanRequest):
    """Scan a single cloud provider."""
    try:
        scanner = CloudScanner()

        # Add provider
        success = scanner.add_provider(
            provider_name=request.provider.value,
            credentials=request.credentials,
            regions=request.regions,
        )

        if not success:
            raise HTTPException(
                status_code=401,
                detail=f"Failed to authenticate with {request.provider.value}",
            )

        # Run scan
        findings = scanner.scan_provider(
            provider_name=request.provider.value,
            check_types=request.check_types,
        )

        # Convert to API models
        finding_models = [
            FindingModel(**finding.to_dict()) for finding in findings
        ]

        # Generate summary
        results_dict = {request.provider.value: findings}
        summary = scanner.get_summary(results_dict)

        scan_id = f"scan-{request.provider.value}-{uuid.uuid4().hex[:8]}"

        return ScanResponse(
            scan_id=scan_id,
            provider=request.provider.value,
            findings=finding_models,
            summary=summary,
            timestamp=datetime.now(timezone.utc),
        )

    except HTTPException:
        raise
    except Exception as e:
        msg = str(e).lower()
        if "credential" in msg or "auth" in msg or "unauthorized" in msg or "access denied" in msg:
            raise HTTPException(
                status_code=401,
                detail=f"Failed to authenticate with {request.provider.value}",
            )
        raise HTTPException(
            status_code=500,
            detail=f"Error scanning cloud: {str(e)}",
        )


@router.post("/scan/multi", response_model=MultiCloudScanResponse)
async def scan_multi_cloud(request: MultiCloudScanRequest):
    """Scan multiple cloud providers."""
    try:
        scanner = CloudScanner()

        # Add all providers
        for provider_config in request.providers:
            provider_name = provider_config.get("provider", "").lower()
            credentials = provider_config.get("credentials", {})
            regions = provider_config.get("regions")

            scanner.add_provider(
                provider_name=provider_name,
                credentials=credentials,
                regions=regions,
            )

        # Run scan on all providers
        results = scanner.scan(check_types=request.check_types)

        # Convert to API models
        results_models = {}
        for provider_name, findings in results.items():
            results_models[provider_name] = [
                FindingModel(**finding.to_dict()) for finding in findings
            ]

        # Generate summary
        summary = scanner.get_summary(results)

        scan_id = f"scan-multi-{uuid.uuid4().hex[:8]}"

        return MultiCloudScanResponse(
            scan_id=scan_id,
            results=results_models,
            summary=summary,
            timestamp=datetime.now(timezone.utc),
        )

    except HTTPException:
        raise
    except Exception as e:
        msg = str(e).lower()
        if "credential" in msg or "auth" in msg or "unauthorized" in msg or "access denied" in msg:
            raise HTTPException(
                status_code=401,
                detail="Failed to authenticate with one or more providers",
            )
        raise HTTPException(
            status_code=500,
            detail=f"Error scanning clouds: {str(e)}",
        )


@router.get("/providers")
async def list_providers():
    """List supported cloud providers."""
    return {
        "providers": [
            {
                "name": "aws",
                "display_name": "Amazon Web Services",
                "supported_checks": ["storage", "iam", "networking", "compute"],
            },
            {
                "name": "azure",
                "display_name": "Microsoft Azure",
                "supported_checks": ["storage", "iam", "networking", "compute"],
            },
            {
                "name": "gcp",
                "display_name": "Google Cloud Platform",
                "supported_checks": ["storage", "iam", "networking", "compute"],
            },
        ]
    }
