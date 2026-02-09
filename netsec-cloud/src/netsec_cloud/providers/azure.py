"""Azure provider implementation."""

from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    from azure.identity import DefaultAzureCredential, ClientSecretCredential
    from azure.mgmt.resource import ResourceManagementClient
    from azure.mgmt.storage import StorageManagementClient
    from azure.mgmt.network import NetworkManagementClient
    from azure.core.exceptions import AzureError
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

try:
    from azure.mgmt.authorization import AuthorizationManagementClient
    AZURE_AUTH_AVAILABLE = True
except ImportError:
    AZURE_AUTH_AVAILABLE = False

from netsec_cloud.providers.base import CloudProvider, Finding


class AzureProvider(CloudProvider):
    """Azure cloud provider implementation."""

    def __init__(self, credentials: Dict[str, Any], regions: Optional[List[str]] = None):
        """Initialize Azure provider."""
        super().__init__(credentials, regions)
        self.credential = None
        self.subscription_id = credentials.get("subscription_id")
        self.authenticated = False

    def authenticate(self) -> bool:
        """Authenticate with Azure."""
        if not AZURE_AVAILABLE:
            return False

        try:
            # Support multiple authentication methods
            if "client_id" in self.credentials and "client_secret" in self.credentials:
                self.credential = ClientSecretCredential(
                    tenant_id=self.credentials.get("tenant_id"),
                    client_id=self.credentials["client_id"],
                    client_secret=self.credentials["client_secret"],
                )
            else:
                # Use default credential (Managed Identity, Azure CLI, etc.)
                self.credential = DefaultAzureCredential()

            # Test authentication
            resource_client = ResourceManagementClient(
                self.credential,
                self.subscription_id or "test",
            )
            # Try to list resource groups (lightweight operation)
            list(resource_client.resource_groups.list())
            self.authenticated = True
            return True

        except Exception:
            self.authenticated = False
            return False

    def scan_storage(self, region: Optional[str] = None) -> List[Finding]:
        """Scan Azure Storage accounts for security issues."""
        findings = []

        if not AZURE_AVAILABLE:
            return findings

        if not self.authenticated:
            if not self.authenticate():
                return findings

        try:
            storage_client = StorageManagementClient(
                self.credential,
                self.subscription_id,
            )

            # List storage accounts
            storage_accounts = storage_client.storage_accounts.list()

            for account in storage_accounts:
                account_name = account.name
                resource_group = account.id.split("/")[4]

                # Check 1: Public access
                try:
                    properties = storage_client.storage_accounts.get_properties(
                        resource_group,
                        account_name,
                    )

                    # Check if blob public access is enabled
                    if hasattr(properties, "allow_blob_public_access") and properties.allow_blob_public_access:
                        findings.append(
                            Finding(
                                finding_id=f"azure-storage-public-{account_name}",
                                type="storage_public_access",
                                severity="high",
                                title=f"Azure Storage Account '{account_name}' allows public blob access",
                                description=f"Storage account {account_name} has public blob access enabled, which may expose sensitive data",
                                resource=f"/subscriptions/{self.subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Storage/storageAccounts/{account_name}",
                                region=account.location or region or "global",
                                provider="azure",
                                remediation={
                                    "immediate": [
                                        "Disable 'Allow Blob public access' on the storage account",
                                    ],
                                    "short_term": [
                                        "Use Azure Policy to enforce deny public blob access across subscriptions",
                                    ],
                                },
                            )
                        )

                    # Check 2: Encryption
                    if hasattr(properties, "encryption"):
                        encryption = properties.encryption
                        if not encryption or not encryption.services or not encryption.services.blob or not encryption.services.blob.enabled:
                            findings.append(
                                Finding(
                                    finding_id=f"azure-storage-no-encryption-{account_name}",
                                    type="storage_no_encryption",
                                    severity="medium",
                                    title=f"Azure Storage Account '{account_name}' does not have encryption enabled",
                                    description=f"Storage account {account_name} does not have blob encryption enabled",
                                    resource=f"/subscriptions/{self.subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Storage/storageAccounts/{account_name}",
                                    region=account.location or region or "global",
                                    provider="azure",
                                    remediation={
                                        "immediate": [
                                            "Enable default encryption (Microsoft-managed keys) or use customer-managed keys",
                                        ],
                                        "short_term": [
                                            "Apply encryption to existing blobs if needed; enforce via Azure Policy",
                                        ],
                                    },
                                )
                            )

                except Exception:
                    continue

        except Exception as e:
            findings.append(
                Finding(
                    finding_id=f"azure-scan-error-storage",
                    type="scan_error",
                    severity="info",
                    title="Error scanning Azure storage",
                    description=f"Error occurred while scanning storage: {str(e)}",
                    resource="azure",
                    region=region or "global",
                    provider="azure",
                )
            )

        return findings

    def scan_iam(self, region: Optional[str] = None) -> List[Finding]:
        """Scan Azure RBAC for security issues (subscription-level broad roles)."""
        findings = []

        if not AZURE_AVAILABLE or not AZURE_AUTH_AVAILABLE:
            return findings

        if not self.authenticated:
            if not self.authenticate():
                return findings

        if not self.subscription_id:
            return findings

        try:
            auth_client = AuthorizationManagementClient(
                self.credential,
                self.subscription_id,
            )
            scope = f"/subscriptions/{self.subscription_id}"

            # Broad roles at subscription scope (CIS-style)
            broad_role_names = {"Owner", "Contributor", "User Access Administrator"}
            role_def_cache: Dict[str, str] = {}

            for assignment in auth_client.role_assignments.list(scope=scope):
                role_def_id = getattr(assignment, "role_definition_id", None)
                principal_id = getattr(assignment, "principal_id", "") or ""
                principal_type = getattr(assignment, "principal_type", None) or "Unknown"
                assignment_id = getattr(assignment, "id", "") or ""

                if not role_def_id:
                    continue

                # Resolve role definition ID to role name (role_def_id is full ID; extract GUID)
                if role_def_id not in role_def_cache:
                    try:
                        guid = role_def_id.split("/")[-1] if role_def_id else ""
                        role_def = auth_client.role_definitions.get(
                            scope=scope,
                            role_definition_id=guid,
                        )
                        role_def_cache[role_def_id] = getattr(role_def, "role_name", "") or ""
                    except Exception:
                        role_def_cache[role_def_id] = ""
                role_name = role_def_cache[role_def_id]

                if role_name not in broad_role_names:
                    continue

                # Flag subscription-level broad role for Users (and optionally ServicePrincipal)
                if principal_type == "User":
                    findings.append(
                        Finding(
                            finding_id=f"azure-rbac-broad-{assignment_id.replace('/', '-')}"[:120],
                            type="rbac_broad_role",
                            severity="medium",
                            title=f"Azure subscription has User with broad role '{role_name}'",
                            description=f"User has subscription-level {role_name}; consider scope reduction or custom roles",
                            resource=assignment_id,
                            region=region or "global",
                            provider="azure",
                            remediation={
                                "immediate": [
                                    "Review if subscription scope is required; reduce to resource group or resource scope",
                                ],
                                "short_term": [
                                    "Use custom roles with least privilege; prefer managed identity for automation",
                                ],
                            },
                        )
                    )
                elif principal_type == "ServicePrincipal" and role_name == "Owner":
                    findings.append(
                        Finding(
                            finding_id=f"azure-rbac-sp-owner-{assignment_id.replace('/', '-')}"[:120],
                            type="rbac_sp_owner",
                            severity="high",
                            title="Azure subscription has Service Principal with Owner",
                            description="Service Principal has subscription-level Owner; high blast radius if compromised",
                            resource=assignment_id,
                            region=region or "global",
                            provider="azure",
                            remediation={
                                "immediate": [
                                    "Replace Owner with Contributor or custom role with minimal permissions",
                                ],
                                "short_term": [
                                    "Use federated identity and scope roles to specific resource groups",
                                ],
                            },
                        )
                    )

        except Exception as e:
            findings.append(
                Finding(
                    finding_id="azure-scan-error-iam",
                    type="scan_error",
                    severity="info",
                    title="Error scanning Azure RBAC",
                    description=f"Error occurred while scanning RBAC: {str(e)}",
                    resource="azure",
                    region=region or "global",
                    provider="azure",
                )
            )

        return findings

    def scan_networking(self, region: Optional[str] = None) -> List[Finding]:
        """Scan Azure networking resources."""
        findings = []

        if not AZURE_AVAILABLE:
            return findings

        if not self.authenticated:
            if not self.authenticate():
                return findings

        try:
            network_client = NetworkManagementClient(
                self.credential,
                self.subscription_id,
            )

            # List Network Security Groups
            nsgs = network_client.network_security_groups.list_all()

            for nsg in nsgs:
                nsg_name = nsg.name
                resource_group = nsg.id.split("/")[4]

                # Check for overly permissive rules
                if nsg.security_rules:
                    for rule in nsg.security_rules:
                        if rule.direction == "Inbound" and rule.access == "Allow":
                            # Check for open access (0.0.0.0/0)
                            if rule.source_address_prefix == "*" or rule.source_address_prefix == "0.0.0.0/0":
                                findings.append(
                                    Finding(
                                        finding_id=f"azure-nsg-open-{nsg_name}-{rule.name}",
                                        type="nsg_open_rule",
                                        severity="high",
                                        title=f"NSG '{nsg_name}' has open inbound rule",
                                        description=f"Network Security Group {nsg_name} allows inbound access from 0.0.0.0/0 on port {rule.destination_port_range}",
                                        resource=nsg.id,
                                        region=nsg.location or region or "global",
                                        provider="azure",
                                        remediation={
                                            "immediate": [
                                                "Restrict source_address_prefix to specific IP ranges or VNets",
                                            ],
                                            "short_term": [
                                                "Review all NSG rules; use Azure Firewall or WAF for public ingress",
                                            ],
                                        },
                                    )
                                )

        except Exception as e:
            findings.append(
                Finding(
                    finding_id=f"azure-scan-error-networking",
                    type="scan_error",
                    severity="info",
                    title="Error scanning Azure networking",
                    description=f"Error occurred while scanning networking: {str(e)}",
                    resource="azure",
                    region=region or "global",
                    provider="azure",
                )
            )

        return findings

    def scan_compute(self, region: Optional[str] = None) -> List[Finding]:
        """Scan Azure compute resources."""
        findings = []

        if not AZURE_AVAILABLE:
            return findings

        # Placeholder for compute scanning
        # Would include VMs, App Services, etc.
        return findings

    def get_regions(self) -> List[str]:
        """Get available Azure regions."""
        if self.regions:
            return self.regions

        # Common Azure regions
        return [
            "eastus",
            "eastus2",
            "westus",
            "westus2",
            "westeurope",
            "northeurope",
            "southeastasia",
        ]
