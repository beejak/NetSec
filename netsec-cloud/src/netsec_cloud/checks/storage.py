"""Storage security checks."""

from typing import List
from netsec_cloud.checks.base import SecurityCheck
from netsec_cloud.providers.base import CloudProvider, Finding


class StorageSecurityCheck(SecurityCheck):
    """Storage security check implementation."""

    def __init__(self):
        """Initialize storage security check."""
        super().__init__(
            name="storage_security",
            description="Check storage resources for security issues",
        )

    def check(self, provider: CloudProvider, region: str = None) -> List[Finding]:
        """Run storage security check."""
        return provider.scan_storage(region=region)
