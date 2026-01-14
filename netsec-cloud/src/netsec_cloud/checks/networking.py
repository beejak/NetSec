"""Networking security checks."""

from typing import List
from netsec_cloud.checks.base import SecurityCheck
from netsec_cloud.providers.base import CloudProvider, Finding


class NetworkingSecurityCheck(SecurityCheck):
    """Networking security check implementation."""

    def __init__(self):
        """Initialize networking security check."""
        super().__init__(
            name="networking_security",
            description="Check networking resources for security issues",
        )

    def check(self, provider: CloudProvider, region: str = None) -> List[Finding]:
        """Run networking security check."""
        return provider.scan_networking(region=region)
