"""DNS security routes."""

from fastapi import APIRouter, HTTPException
from netsec_core.api.models import DNSScanRequest, DNSResult, Finding, Severity
from netsec_core.core.dns_scanner import DNSScanner

router = APIRouter()
scanner = DNSScanner()


@router.post("/scan", response_model=DNSResult)
async def scan_dns(request: DNSScanRequest):
    """Scan domain for DNS security issues."""
    try:
        result = scanner.scan_domain(
            domain=request.domain,
            check_tunneling=request.check_tunneling,
            check_spoofing=request.check_spoofing,
            analyze_patterns=request.analyze_patterns,
        )

        # Convert findings to Finding models
        findings = []
        for finding_data in result.get("findings", []):
            findings.append(
                Finding(
                    finding_id=finding_data.get("finding_id", ""),
                    type=finding_data.get("type", "unknown"),
                    severity=Severity(finding_data.get("severity", "info")),
                    description=finding_data.get("description", ""),
                    remediation=None,
                )
            )

        return DNSResult(
            domain=result["domain"],
            findings=findings,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error scanning DNS: {str(e)}",
        )


@router.get("/monitor")
async def monitor_dns(duration: int = 60):
    """Monitor DNS queries in real-time."""
    try:
        result = scanner.monitor_dns_queries(duration=duration)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error monitoring DNS: {str(e)}",
        )


@router.post("/detect-tunneling")
async def detect_tunneling(request: DNSScanRequest):
    """Detect DNS tunneling attempts."""
    try:
        result = scanner.scan_domain(
            domain=request.domain,
            check_tunneling=True,
            check_spoofing=False,
            analyze_patterns=False,
        )
        # Filter only tunneling findings
        tunneling_findings = [
            f for f in result.get("findings", [])
            if f.get("type") == "dns_tunneling"
        ]
        return {
            "domain": request.domain,
            "tunneling_detected": len(tunneling_findings) > 0,
            "findings": tunneling_findings,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error detecting tunneling: {str(e)}",
        )


@router.get("/anomalies")
async def get_anomalies(domain: str):
    """Get DNS anomalies."""
    try:
        result = scanner.scan_domain(
            domain=domain,
            check_tunneling=True,
            check_spoofing=True,
            analyze_patterns=True,
        )
        # Filter anomaly-related findings
        anomalies = [
            f for f in result.get("findings", [])
            if f.get("type") in ["dns_tunneling", "dns_spoofing", "dns_pattern"]
        ]
        return {
            "domain": domain,
            "anomalies": anomalies,
            "count": len(anomalies),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting anomalies: {str(e)}",
        )
