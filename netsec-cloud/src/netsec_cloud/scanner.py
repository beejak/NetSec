"""Unified cloud security scanner."""

from typing import List, Dict, Any, Optional
from datetime import datetime

from netsec_cloud.providers.base import CloudProvider, Finding
from netsec_cloud.providers.aws import AWSProvider
from netsec_cloud.providers.azure import AzureProvider
from netsec_cloud.providers.gcp import GCPProvider


class CloudScanner:
    """Unified cloud security scanner supporting multiple providers."""

    def __init__(self):
        """Initialize cloud scanner."""
        self.providers: Dict[str, CloudProvider] = {}

    def add_provider(
        self,
        provider_name: str,
        credentials: Dict[str, Any],
        regions: Optional[List[str]] = None,
    ) -> bool:
        """
        Add a cloud provider to scan.

        Args:
            provider_name: Provider name ("aws", "azure", "gcp")
            credentials: Provider-specific credentials
            regions: List of regions to scan

        Returns:
            True if provider added successfully
        """
        provider_name = provider_name.lower()

        try:
            if provider_name == "aws":
                provider = AWSProvider(credentials, regions)
            elif provider_name == "azure":
                provider = AzureProvider(credentials, regions)
            elif provider_name == "gcp":
                provider = GCPProvider(credentials, regions)
            else:
                return False

            # Authenticate
            if provider.authenticate():
                self.providers[provider_name] = provider
                return True
            else:
                return False

        except Exception:
            return False

    def scan(
        self,
        check_types: Optional[List[str]] = None,
        providers: Optional[List[str]] = None,
    ) -> Dict[str, List[Finding]]:
        """
        Scan all configured providers.

        Args:
            check_types: Types of checks to run (storage, iam, networking, compute)
            providers: List of providers to scan (None = all)

        Returns:
            Dictionary mapping provider names to findings
        """
        if check_types is None:
            check_types = ["storage", "iam", "networking", "compute"]

        if providers is None:
            providers = list(self.providers.keys())

        results = {}

        for provider_name in providers:
            if provider_name not in self.providers:
                continue

            provider = self.providers[provider_name]
            findings = provider.scan_all(check_types)
            results[provider_name] = findings

        return results

    def scan_provider(
        self,
        provider_name: str,
        check_types: Optional[List[str]] = None,
    ) -> List[Finding]:
        """
        Scan a specific provider.

        Args:
            provider_name: Provider to scan
            check_types: Types of checks to run

        Returns:
            List of findings
        """
        if provider_name not in self.providers:
            return []

        provider = self.providers[provider_name]
        return provider.scan_all(check_types)

    def get_summary(self, findings: Dict[str, List[Finding]]) -> Dict[str, Any]:
        """
        Get summary of scan results.

        Args:
            findings: Dictionary of provider findings

        Returns:
            Summary statistics
        """
        summary = {
            "total_findings": 0,
            "by_provider": {},
            "by_severity": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "info": 0,
            },
            "by_type": {},
            "timestamp": datetime.utcnow().isoformat(),
        }

        for provider_name, provider_findings in findings.items():
            summary["by_provider"][provider_name] = len(provider_findings)
            summary["total_findings"] += len(provider_findings)

            for finding in provider_findings:
                # Count by severity
                severity = finding.severity.lower()
                if severity in summary["by_severity"]:
                    summary["by_severity"][severity] += 1

                # Count by type
                finding_type = finding.type
                summary["by_type"][finding_type] = summary["by_type"].get(finding_type, 0) + 1

        return summary

    def list_providers(self) -> List[str]:
        """List configured providers."""
        return list(self.providers.keys())
