"""Network scanning routes."""

from fastapi import APIRouter, HTTPException
from netsec_core.api.models import ScanRequest, ScanResult
from netsec_core.core.network_scanner import NetworkScanner

router = APIRouter()
scanner = NetworkScanner()


@router.post("/ports", response_model=ScanResult)
async def scan_ports(request: ScanRequest):
    """Scan target for open ports."""
    try:
        result = scanner.scan_ports(
            target=request.target,
            ports=request.ports,
            scan_type=request.scan_type,
            timeout=request.timeout,
        )

        return ScanResult(
            scan_id=result["scan_id"],
            target=result["target"],
            open_ports=result["open_ports"],
            services=result["services"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error scanning ports: {str(e)}",
        )


@router.post("/services", response_model=ScanResult)
async def scan_services(request: ScanRequest):
    """Scan target for services."""
    try:
        result = scanner.scan_services(
            target=request.target,
            ports=request.ports,
        )

        return ScanResult(
            scan_id=result["scan_id"],
            target=result["target"],
            open_ports=result["open_ports"],
            services=result["services"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error scanning services: {str(e)}",
        )


@router.get("/results/{scan_id}", response_model=ScanResult)
async def get_scan_results(scan_id: str):
    """Get scan results by scan ID."""
    # Note: This would require result storage (database/cache)
    # For now, return a placeholder
    raise HTTPException(
        status_code=501,
        detail="Result storage and retrieval requires database implementation",
    )
