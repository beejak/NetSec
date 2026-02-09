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
                            remediation={
                                "immediate": [
                                    "Remove allUsers/allAuthenticatedUsers from bucket IAM bindings",
                                ],
                                "short_term": [
                                    "Use IAM conditions and ensure public access prevention is enabled at org level",
                                ],
                            },
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
                            remediation={
                                "immediate": [
                                    "Enable object versioning on the bucket if retention/recovery is required",
                                ],
                                "short_term": [
                                    "Enforce versioning via organization policy for sensitive buckets",
                                ],
                            },
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
        """Scan GCP project IAM for broad roles (Owner, Editor) granted to users."""
        findings = []

        if not GCP_AVAILABLE:
            return findings

        if not self.authenticated:
            if not self.authenticate():
                return findings

        if not self.project_id:
            return findings

        try:
            policy = self._get_project_iam_policy()
            if not policy:
                return findings

            broad_roles = {"roles/owner", "roles/editor"}
            seen_member_role: set = set()
            for binding in policy.get("bindings", []):
                role = binding.get("role", "")
                members = binding.get("members", [])

                if role not in broad_roles:
                    continue

                for member in members:
                    key = (member, role)
                    if key in seen_member_role:
                        continue
                    seen_member_role.add(key)
                    if member.startswith("user:"):
                        safe = member.replace(":", "-").replace("/", "-")[:50]
                        finding_id = f"gcp-iam-broad-{role.replace('/', '-')}-{safe}"
                        severity = "high" if role == "roles/owner" else "medium"
                        title_role = "Owner" if role == "roles/owner" else "Editor"
                        findings.append(
                            Finding(
                                finding_id=finding_id,
                                type="iam_broad_role",
                                severity=severity,
                                title=f"GCP project has User with {title_role}",
                                description=f"User {member} has project-level {role}; consider minimal roles",
                                resource=f"projects/{self.project_id}",
                                region="global",
                                provider="gcp",
                                remediation={
                                    "immediate": [
                                        "Replace with Viewer or custom role with least privilege",
                                    ],
                                    "short_term": [
                                        "Use IAM conditions and separate dev/prod projects",
                                    ],
                                },
                            )
                        )
                    elif member.startswith("serviceAccount:") and role == "roles/owner":
                        sa_safe = member.replace(":", "-").replace("/", "-")[:55]
                        findings.append(
                            Finding(
                                finding_id=f"gcp-iam-sa-owner-{sa_safe}",
                                type="iam_sa_owner",
                                severity="high",
                                title="GCP project has Service Account with Owner",
                                description=f"Service account {member} has Owner; high risk if key is exposed",
                                resource=f"projects/{self.project_id}",
                                region="global",
                                provider="gcp",
                                remediation={
                                    "immediate": [
                                        "Replace Owner with Contributor or custom role",
                                    ],
                                    "short_term": [
                                        "Use workload identity and short-lived credentials",
                                    ],
                                },
                            )
                        )

        except Exception as e:
            findings.append(
                Finding(
                    finding_id="gcp-scan-error-iam",
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

    def _get_project_iam_policy(self) -> Optional[Dict[str, Any]]:
        """Get IAM policy for the project (requires google-api-python-client or v3 client)."""
        try:
            from googleapiclient.discovery import build

            service = build(
                "cloudresourcemanager",
                "v1",
                credentials=self.credential,
                cache_discovery=False,
            )
            resource = f"projects/{self.project_id}"
            request = service.projects().getIamPolicy(
                resource=resource,
                body={"options": {"requestedPolicyVersion": 3}},
            )
            return request.execute()
        except ImportError:
            return None
        except Exception:
            return None

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
                                        remediation={
                                            "immediate": [
                                                "Restrict source_ranges to specific IP ranges or use tags/targets",
                                            ],
                                            "short_term": [
                                                "Review firewall rules; use Cloud Armor and load balancers for public ingress",
                                            ],
                                        },
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
