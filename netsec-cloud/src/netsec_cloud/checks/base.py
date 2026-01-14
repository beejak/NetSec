"""Base security check interface."""

from abc import ABC, abstractmethod
from typing import List
from netsec_cloud.providers.base import CloudProvider, Finding


class SecurityCheck(ABC):
    """Base class for security checks."""

    def __init__(self, name: str, description: str):
        """Initialize security check."""
        self.name = name
        self.description = description

    @abstractmethod
    def check(self, provider: CloudProvider, region: str = None) -> List[Finding]:
        """
        Run security check.

        Args:
            provider: Cloud provider instance
            region: Region to check (None = default/all)

        Returns:
            List of security findings
        """
        pass

    def get_name(self) -> str:
        """Get check name."""
        return self.name

    def get_description(self) -> str:
        """Get check description."""
        return self.description
