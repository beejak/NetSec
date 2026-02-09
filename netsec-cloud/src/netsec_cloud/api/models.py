"""Pydantic models for NetSec-Cloud API."""

from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime


class CloudProvider(str, Enum):
    """Supported cloud providers."""

    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"


class Severity(str, Enum):
    """Finding severity levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ScanRequest(BaseModel):
    """Request model for cloud scanning."""

    provider: CloudProvider = Field(..., description="Cloud provider to scan")
    regions: Optional[List[str]] = Field(None, description="Regions to scan (None = all)")
    check_types: Optional[List[str]] = Field(
        None,
        description="Types of checks to run (storage, iam, networking, compute)",
    )
    credentials: Dict[str, Any] = Field(..., description="Provider credentials")


class FindingModel(BaseModel):
    """Finding model for API responses."""

    finding_id: str
    type: str
    severity: Severity
    title: str
    description: str
    resource: str
    region: str
    provider: str
    remediation: Optional[Dict[str, Any]] = None
    timestamp: datetime


class ScanResponse(BaseModel):
    """Response model for cloud scanning."""

    scan_id: str
    provider: str
    findings: List[FindingModel]
    summary: Dict[str, Any]
    timestamp: datetime


class ComplianceCheckRequest(BaseModel):
    """Request body for compliance check."""

    credentials: Dict[str, Any] = Field(default_factory=dict, description="Provider credentials")
    regions: Optional[List[str]] = Field(None, description="Regions to scan")
    check_types: Optional[List[str]] = Field(
        None,
        description="Check types (storage, iam, networking, compute)",
    )


class MultiCloudScanRequest(BaseModel):
    """Request model for multi-cloud scanning."""

    providers: List[Dict[str, Any]] = Field(
        ...,
        description="List of provider configurations with credentials",
    )
    check_types: Optional[List[str]] = Field(
        None,
        description="Types of checks to run",
    )


class MultiCloudScanResponse(BaseModel):
    """Response model for multi-cloud scanning."""

    scan_id: str
    results: Dict[str, List[FindingModel]]
    summary: Dict[str, Any]
    timestamp: datetime
