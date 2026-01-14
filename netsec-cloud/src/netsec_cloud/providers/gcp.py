"""GCP provider implementation."""

from typing import List, Dict, Any, Optional

try:
    from google.cloud import resource_manager
    from google.cloud import storage
    from google.cloud import compute_v1
    from google.oauth2 import service_account
    from google.auth.exceptions import GoogleAuthError
    GCP_AVAILABLE = True
except ImportError:
    GCP_AVAILABLE = False

from netsec_cloud.providers.base import CloudProvider, Finding


class GCPProvider(CloudProvider):
    """GCP cloud provider implementation."""

    def __init__(self, credentials: Dict[str, Any], regions: Optional[List[str]] = None):
        """Initialize GCP provider."""
        super().__init__(credentials, regions)
        self.project_id = credentials.get("project_id")
        self.credential = None
        self.authenticated = False

    def authenticate(self) -> bool:
        """Authenticate with GCP."""
        if not GCP_AVAILABLE:
            return False

        try:
            # Support service account key file
            if "service_account_file" in self.credentials:
                self.credential = service_account.Credentials.from_service_account_file(
                    self.credentials["service_account_file"]
                )
            elif "service_account_info" in self.credentials:
                self.credential = service_account.Credentials.from_service_account_info(
                    self.credentials["service_account_info"]
                )
            else:
                # Use default credentials (gcloud, environment, etc.)
                from google.auth import default
                self.credential, _ = default()

            # Test authentication
            client = resource_manager.Client(credentials=self.credential)
            list(client.list_projects())
            self.authenticated = True
            return True

        except Exception:
            self.authenticated = False
            return False

    def scan_storage(self, region: Optional[str] = None) -> List[Finding]:
        """Scan GCP Cloud Storage buckets for security issues."""
        findings = []

        if not GCP_AVAILABLE:
            return findings

        if not self.authenticated:
            if not self.authenticate():
                return findings

        try:
            storage_client = storage.Client(
                project=self.project_id,
                credentials=self.credential,
            )

            # List all buckets
            buckets = storage_client.list_buckets()

            for bucket in buckets:
                bucket_name = bucket.name

                # Check 1: Public access
                policy = bucket.get_iam_policy()
                public_access = False

                for binding in policy.bindings:
                    if "allUsers" in binding.get("members", []) or "allAuthenticatedUsers" in binding.get("members", []):
                        if "roles/storage.objectViewer" in binding.get("role") or "roles/storage.legacyBucketReader" in binding.get("role"):
                            public_access = True
                            break

                if public_access:
                    findings.append(
                        Finding(
                            finding_id=f"gcp-storage-public-{bucket_name}",
                            type="storage_public_access",
                            severity="high",
                            title=f"GCP Storage Bucket '{bucket_name}' has public access",
                            description=f"Bucket {bucket_name} allows public read access, which may expose sensitive data",
                            resource=f"gs://{bucket_name}",
                            region=bucket.location or region or "global",
                            provider="gcp",
                        )
                    )

                # Check 2: Encryption
                if not bucket.default_kms_key_name:
                    # Check if bucket encryption is enabled (bucket-level encryption)
                    # Note: GCP encrypts by default, but we check for customer-managed keys
                    pass  # Default encryption is enabled in GCP

                # Check 3: Versioning
                if not bucket.versioning_enabled:
                    findings.append(
                        Finding(
                            finding_id=f"gcp-storage-no-versioning-{bucket_name}",
                            type="storage_no_versioning",
                            severity="low",
                            title=f"GCP Storage Bucket '{bucket_name}' does not have versioning enabled",
                            description=f"Bucket {bucket_name} does not have versioning enabled",
                            resource=f"gs://{bucket_name}",
                            region=bucket.location or region or "global",
                            provider="gcp",
                        )
                    )

        except Exception as e:
            findings.append(
                Finding(
                    finding_id=f"gcp-scan-error-storage",
                    type="scan_error",
                    severity="info",
                    title="Error scanning GCP storage",
                    description=f"Error occurred while scanning storage: {str(e)}",
                    resource="gcp",
                    region=region or "global",
                    provider="gcp",
                )
            )

        return findings

    def scan_iam(self, region: Optional[str] = None) -> List[Finding]:
        """Scan GCP IAM for security issues."""
        findings = []

        if not GCP_AVAILABLE:
            return findings

        if not self.authenticated:
            if not self.authenticate():
                return findings

        try:
            # GCP IAM scanning requires Cloud Asset API or Resource Manager API
            # This is a placeholder for future implementation
            # Would check for:
            # - Overprivileged IAM bindings
            # - Service accounts with excessive permissions
            # - Organization-level policies

            pass

        except Exception as e:
            findings.append(
                Finding(
                    finding_id=f"gcp-scan-error-iam",
                    type="scan_error",
                    severity="info",
                    title="Error scanning GCP IAM",
                    description=f"Error occurred while scanning IAM: {str(e)}",
                    resource="gcp",
                    region="global",
                    provider="gcp",
                )
            )

        return findings

    def scan_networking(self, region: Optional[str] = None) -> List[Finding]:
        """Scan GCP networking resources."""
        findings = []

        if not GCP_AVAILABLE:
            return findings

        if not self.authenticated:
            if not self.authenticate():
                return findings

        try:
            compute_client = compute_v1.FirewallsClient(credentials=self.credential)

            # List firewall rules
            firewall_rules = compute_client.list(project=self.project_id)

            for rule in firewall_rules:
                rule_name = rule.name

                # Check for overly permissive rules
                if rule.direction == "INGRESS":
                    # Check source ranges
                    for source_range in rule.source_ranges:
                        if source_range == "0.0.0.0/0":
                            # Check if it's not a necessary service (like HTTP/HTTPS)
                            if not any(port in ["80", "443"] for port in rule.allowed[0].ports if rule.allowed):
                                findings.append(
                                    Finding(
                                        finding_id=f"gcp-firewall-open-{rule_name}",
                                        type="firewall_open_rule",
                                        severity="high",
                                        title=f"GCP Firewall Rule '{rule_name}' allows open access",
                                        description=f"Firewall rule {rule_name} allows inbound access from 0.0.0.0/0",
                                        resource=f"projects/{self.project_id}/global/firewalls/{rule_name}",
                                        region="global",
                                        provider="gcp",
                                    )
                                )

        except Exception as e:
            findings.append(
                Finding(
                    finding_id=f"gcp-scan-error-networking",
                    type="scan_error",
                    severity="info",
                    title="Error scanning GCP networking",
                    description=f"Error occurred while scanning networking: {str(e)}",
                    resource="gcp",
                    region=region or "global",
                    provider="gcp",
                )
            )

        return findings

    def scan_compute(self, region: Optional[str] = None) -> List[Finding]:
        """Scan GCP compute resources."""
        findings = []

        if not GCP_AVAILABLE:
            return findings

        # Placeholder for compute scanning
        # Would include Compute Engine instances, GKE clusters, etc.
        return findings

    def get_regions(self) -> List[str]:
        """Get available GCP regions."""
        if self.regions:
            return self.regions

        # Common GCP regions
        return [
            "us-central1",
            "us-east1",
            "us-west1",
            "europe-west1",
            "asia-east1",
            "asia-southeast1",
        ]
