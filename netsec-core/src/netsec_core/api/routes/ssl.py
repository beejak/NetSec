"""SSL/TLS security routes."""

import logging
from fastapi import APIRouter, HTTPException
from netsec_core.api.models import SSLCheckRequest, SSLResult, Finding, Severity
from netsec_core.core.ssl_scanner import SSLScanner

logger = logging.getLogger(__name__)
router = APIRouter()
scanner = SSLScanner()


@router.post("/check-certificate", response_model=SSLResult)
async def check_certificate(request: SSLCheckRequest):
    """Check SSL/TLS certificate."""
    try:
        result = scanner.check_certificate(
            hostname=request.hostname,
            port=request.port,
            check_expiration=request.check_expiration,
            check_ciphers=request.check_ciphers,
            check_chain=request.check_chain,
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

        return SSLResult(
            hostname=result["hostname"],
            port=result["port"],
            certificate_info=result.get("certificate_info"),
            findings=findings,
        )
    except Exception:
        logger.exception("SSL certificate check failed")
        raise HTTPException(status_code=500, detail="An error occurred while checking the certificate.")


@router.get("/certificates")
async def list_certificates():
    """List monitored certificates."""
    try:
        result = scanner.list_certificates()
        return result
    except Exception:
        logger.exception("List certificates failed")
        raise HTTPException(status_code=500, detail="An error occurred while listing certificates.")


@router.post("/detect-weak-ciphers")
async def detect_weak_ciphers(request: SSLCheckRequest):
    """Detect weak SSL/TLS ciphers."""
    try:
        result = scanner.check_certificate(
            hostname=request.hostname,
            port=request.port,
            check_expiration=False,
            check_ciphers=True,
            check_chain=False,
        )
        # Filter only cipher-related findings
        cipher_findings = [
            f for f in result.get("findings", [])
            if f.get("type") in ["weak_cipher", "weak_tls_version"]
        ]
        return {
            "hostname": request.hostname,
            "port": request.port,
            "weak_ciphers_detected": len(cipher_findings) > 0,
            "findings": cipher_findings,
        }
    except Exception:
        logger.exception("Weak cipher detection failed")
        raise HTTPException(status_code=500, detail="An error occurred while detecting weak ciphers.")


@router.get("/expiring-soon")
async def get_expiring_certificates(hostname: str, port: int = 443):
    """Get certificates expiring soon."""
    try:
        result = scanner.check_certificate(
            hostname=hostname,
            port=port,
            check_expiration=True,
            check_ciphers=False,
            check_chain=False,
        )
        # Filter only expiration-related findings
        expiration_findings = [
            f for f in result.get("findings", [])
            if f.get("type") in ["certificate_expired", "certificate_expiring"]
        ]
        return {
            "hostname": hostname,
            "port": port,
            "expiring_soon": len(expiration_findings) > 0,
            "findings": expiration_findings,
        }
    except Exception:
        logger.exception("Certificate expiration check failed")
        raise HTTPException(status_code=500, detail="An error occurred while checking expiration.")
