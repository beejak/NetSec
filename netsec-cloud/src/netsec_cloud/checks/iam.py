"""IAM security checks."""

from typing import List
from netsec_cloud.checks.base import SecurityCheck
from netsec_cloud.providers.base import CloudProvider, Finding


class IAMSecurityCheck(SecurityCheck):
    """IAM security check implementation."""

    def __init__(self):
        """Initialize IAM security check."""
        super().__init__(
            name="iam_security",
            description="Check IAM/identity resources for security issues",
        )

    def check(self, provider: CloudProvider, region: str = None) -> List[Finding]:
        """Run IAM security check."""
        return provider.scan_iam(region=region)
