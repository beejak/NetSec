"""Pydantic models for NetSec-Core API."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

from pydantic import BaseModel, Field


class Severity(str, Enum):
    """Severity levels for findings."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ScanRequest(BaseModel):
    """Request model for network scanning."""

    target: str = Field(..., description="Target hostname or IP address")
    ports: Optional[List[int]] = Field(None, description="Specific ports to scan")
    scan_type: str = Field("tcp", description="Type of scan (tcp, udp, syn)")
    timeout: Optional[float] = Field(5.0, description="Timeout in seconds")


class ScanResult(BaseModel):
    """Result model for network scanning."""

    scan_id: str = Field(..., description="Unique scan identifier")
    target: str = Field(..., description="Scanned target")
    open_ports: List[int] = Field(default_factory=list, description="List of open ports")
    services: List[Dict[str, Any]] = Field(
        default_factory=list, description="Detected services"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Scan timestamp")


class Finding(BaseModel):
    """Model for security findings."""

    finding_id: str = Field(..., description="Unique finding identifier")
    type: str = Field(..., description="Type of finding")
    severity: Severity = Field(..., description="Severity level")
    description: str = Field(..., description="Finding description")
    remediation: Optional[Dict[str, Any]] = Field(
        None, description="Remediation guidance"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Finding timestamp")


class DNSScanRequest(BaseModel):
    """Request model for DNS security scanning."""

    domain: str = Field(..., description="Domain to analyze")
    check_tunneling: bool = Field(True, description="Check for DNS tunneling")
    check_spoofing: bool = Field(True, description="Check for DNS spoofing")
    analyze_patterns: bool = Field(True, description="Analyze query patterns")


class DNSResult(BaseModel):
    """Result model for DNS security analysis."""

    domain: str = Field(..., description="Analyzed domain")
    findings: List[Finding] = Field(default_factory=list, description="Security findings")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")


class SSLCheckRequest(BaseModel):
    """Request model for SSL/TLS certificate checking."""

    hostname: str = Field(..., description="Hostname to check")
    port: int = Field(443, description="Port to check")
    check_expiration: bool = Field(True, description="Check certificate expiration")
    check_ciphers: bool = Field(True, description="Check for weak ciphers")
    check_chain: bool = Field(True, description="Validate certificate chain")


class SSLResult(BaseModel):
    """Result model for SSL/TLS checking."""

    hostname: str = Field(..., description="Checked hostname")
    port: int = Field(..., description="Checked port")
    certificate_info: Optional[Dict[str, Any]] = Field(
        None, description="Certificate information"
    )
    findings: List[Finding] = Field(default_factory=list, description="Security findings")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Check timestamp")


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Check timestamp")
