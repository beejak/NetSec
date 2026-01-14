"""Base cloud provider interface."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime


class Finding:
    """Security finding model."""

    def __init__(
        self,
        finding_id: str,
        type: str,
        severity: str,
        title: str,
        description: str,
        resource: str,
        region: str,
        provider: str,
        remediation: Optional[Dict[str, Any]] = None,
    ):
        """Initialize finding."""
        self.finding_id = finding_id
        self.type = type
        self.severity = severity  # critical, high, medium, low, info
        self.title = title
        self.description = description
        self.resource = resource
        self.region = region
        self.provider = provider
        self.remediation = remediation
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "finding_id": self.finding_id,
            "type": self.type,
            "severity": self.severity,
            "title": self.title,
            "description": self.description,
            "resource": self.resource,
            "region": self.region,
            "provider": self.provider,
            "remediation": self.remediation,
            "timestamp": self.timestamp,
        }


class CloudProvider(ABC):
    """Base class for cloud providers."""

    def __init__(self, credentials: Dict[str, Any], regions: Optional[List[str]] = None):
        """
        Initialize cloud provider.

        Args:
            credentials: Provider-specific credentials
            regions: List of regions to scan (None = all)
        """
        self.credentials = credentials
        self.regions = regions or []
        self.provider_name = self.__class__.__name__.replace("Provider", "").lower()

    @abstractmethod
    def authenticate(self) -> bool:
        """Authenticate with cloud provider."""
        pass

    @abstractmethod
    def scan_storage(self, region: Optional[str] = None) -> List[Finding]:
        """Scan storage resources for security issues."""
        pass

    @abstractmethod
    def scan_iam(self, region: Optional[str] = None) -> List[Finding]:
        """Scan IAM/identity resources for security issues."""
        pass

    @abstractmethod
    def scan_networking(self, region: Optional[str] = None) -> List[Finding]:
        """Scan networking resources for security issues."""
        pass

    @abstractmethod
    def scan_compute(self, region: Optional[str] = None) -> List[Finding]:
        """Scan compute resources for security issues."""
        pass

    def scan_all(self, check_types: Optional[List[str]] = None) -> List[Finding]:
        """
        Run all security scans.

        Args:
            check_types: List of check types to run (None = all)

        Returns:
            List of security findings
        """
        if check_types is None:
            check_types = ["storage", "iam", "networking", "compute"]

        findings = []
        regions = self.regions if self.regions else [None]  # None = default region

        for region in regions:
            if "storage" in check_types:
                findings.extend(self.scan_storage(region))
            if "iam" in check_types:
                findings.extend(self.scan_iam(region))
            if "networking" in check_types:
                findings.extend(self.scan_networking(region))
            if "compute" in check_types:
                findings.extend(self.scan_compute(region))

        return findings

    def get_regions(self) -> List[str]:
        """Get available regions for this provider."""
        # Default implementation - override in subclasses
        return self.regions or []
