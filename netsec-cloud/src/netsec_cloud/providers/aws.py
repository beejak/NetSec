"""AWS provider implementation."""

import boto3
from typing import List, Dict, Any, Optional
from botocore.exceptions import ClientError, NoCredentialsError

from netsec_cloud.providers.base import CloudProvider, Finding


class AWSProvider(CloudProvider):
    """AWS cloud provider implementation."""

    def __init__(self, credentials: Dict[str, Any], regions: Optional[List[str]] = None):
        """Initialize AWS provider."""
        super().__init__(credentials, regions)
        self.session = None
        self.authenticated = False

    def authenticate(self) -> bool:
        """Authenticate with AWS."""
        try:
            # Support multiple credential methods
            if "access_key_id" in self.credentials and "secret_access_key" in self.credentials:
                self.session = boto3.Session(
                    aws_access_key_id=self.credentials["access_key_id"],
                    aws_secret_access_key=self.credentials["secret_access_key"],
                    region_name=self.credentials.get("region", "us-east-1"),
                )
            elif "profile" in self.credentials:
                self.session = boto3.Session(profile_name=self.credentials["profile"])
            else:
                # Use default credentials (environment, IAM role, etc.)
                self.session = boto3.Session()

            # Test authentication
            sts = self.session.client("sts")
            sts.get_caller_identity()
            self.authenticated = True
            return True

        except (NoCredentialsError, ClientError) as e:
            self.authenticated = False
            return False

    def scan_storage(self, region: Optional[str] = None) -> List[Finding]:
        """Scan AWS S3 buckets for security issues."""
        findings = []

        if not self.authenticated:
            if not self.authenticate():
                return findings

        try:
            s3_client = self.session.client("s3", region_name=region)
            s3_resource = self.session.resource("s3", region_name=region)

            # List all buckets
            buckets = s3_client.list_buckets()

            for bucket_info in buckets.get("Buckets", []):
                bucket_name = bucket_info["Name"]

                try:
                    bucket = s3_resource.Bucket(bucket_name)

                    # Check 1: Public access
                    try:
                        public_access = bucket.Acl().grants
                        public_read = any(
                            grant.get("Grantee", {}).get("Type") == "Group"
                            and grant.get("Grantee", {}).get("URI") == "http://acs.amazonaws.com/groups/global/AllUsers"
                            for grant in public_access
                        )

                        if public_read:
                            findings.append(
                                Finding(
                                    finding_id=f"aws-s3-public-{bucket_name}",
                                    type="s3_public_access",
                                    severity="high",
                                    title=f"S3 Bucket '{bucket_name}' has public read access",
                                    description=f"Bucket {bucket_name} allows public read access, which may expose sensitive data",
                                    resource=f"arn:aws:s3:::{bucket_name}",
                                    region=region or "global",
                                    provider="aws",
                                    remediation={
                                        "immediate": [
                                            "Remove public read access from bucket ACL",
                                            "Review bucket policy for public access",
                                        ],
                                        "short_term": [
                                            "Enable S3 Block Public Access",
                                            "Review and restrict bucket policies",
                                        ],
                                    },
                                )
                            )
                    except ClientError:
                        pass  # Cannot read ACL

                    # Check 2: Encryption
                    try:
                        encryption = s3_client.get_bucket_encryption(Bucket=bucket_name)
                        # Encryption is enabled
                    except ClientError as e:
                        if e.response["Error"]["Code"] == "ServerSideEncryptionConfigurationNotFoundError":
                            findings.append(
                                Finding(
                                    finding_id=f"aws-s3-no-encryption-{bucket_name}",
                                    type="s3_no_encryption",
                                    severity="medium",
                                    title=f"S3 Bucket '{bucket_name}' does not have encryption enabled",
                                    description=f"Bucket {bucket_name} does not have server-side encryption configured",
                                    resource=f"arn:aws:s3:::{bucket_name}",
                                    region=region or "global",
                                    provider="aws",
                                )
                            )
                    except Exception:
                        pass

                    # Check 3: Versioning
                    try:
                        versioning = s3_client.get_bucket_versioning(Bucket=bucket_name)
                        if versioning.get("Status") != "Enabled":
                            findings.append(
                                Finding(
                                    finding_id=f"aws-s3-no-versioning-{bucket_name}",
                                    type="s3_no_versioning",
                                    severity="low",
                                    title=f"S3 Bucket '{bucket_name}' does not have versioning enabled",
                                    description=f"Bucket {bucket_name} does not have versioning enabled, which may lead to data loss",
                                    resource=f"arn:aws:s3:::{bucket_name}",
                                    region=region or "global",
                                    provider="aws",
                                )
                            )
                    except Exception:
                        pass

                except ClientError as e:
                    # Skip buckets we can't access
                    continue

        except Exception as e:
            # Log error but continue
            findings.append(
                Finding(
                    finding_id=f"aws-scan-error-storage",
                    type="scan_error",
                    severity="info",
                    title="Error scanning AWS storage",
                    description=f"Error occurred while scanning storage: {str(e)}",
                    resource="aws",
                    region=region or "global",
                    provider="aws",
                )
            )

        return findings

    def scan_iam(self, region: Optional[str] = None) -> List[Finding]:
        """Scan AWS IAM for security issues."""
        findings = []

        if not self.authenticated:
            if not self.authenticate():
                return findings

        try:
            iam_client = self.session.client("iam")

            # Check 0: Root account access keys (CIS 1.4)
            try:
                root_keys = iam_client.list_access_keys(UserName="root")
                if root_keys.get("AccessKeyMetadata"):
                    findings.append(
                        Finding(
                            finding_id="aws-root-access-keys",
                            type="iam_root_access_keys",
                            severity="critical",
                            title="Root account has active access keys",
                            description="Root user should not have access keys; use IAM users/roles instead (CIS 1.4)",
                            resource=f"arn:aws:iam::{self._get_account_id()}:root",
                            region="global",
                            provider="aws",
                            remediation={
                                "immediate": ["Deactivate and delete root access keys"],
                                "short_term": ["Use IAM users or roles with least privilege for programmatic access"],
                            },
                        )
                    )
            except ClientError:
                pass

            # Check 1: Users without MFA
            users = iam_client.list_users()
            for user in users.get("Users", []):
                user_name = user["UserName"]

                # Check MFA devices
                mfa_devices = iam_client.list_mfa_devices(UserName=user_name)
                if not mfa_devices.get("MFADevices"):
                    # Check if user has access keys
                    access_keys = iam_client.list_access_keys(UserName=user_name)
                    if access_keys.get("AccessKeyMetadata"):
                        findings.append(
                            Finding(
                                finding_id=f"aws-iam-no-mfa-{user_name}",
                                type="iam_no_mfa",
                                severity="high",
                                title=f"IAM User '{user_name}' does not have MFA enabled",
                                description=f"User {user_name} has access keys but no MFA device configured",
                                resource=f"arn:aws:iam::{self._get_account_id()}:user/{user_name}",
                                region="global",
                                provider="aws",
                            )
                        )

            # Check 2: Overprivileged policies (simplified check)
            # This is a basic check - full analysis would be more complex
            policies = iam_client.list_policies(Scope="Local")
            for policy in policies.get("Policies", []):
                policy_arn = policy["Arn"]
                policy_name = policy["PolicyName"]

                # Check for overly permissive policies (simplified)
                if "*" in policy_name.lower() or "admin" in policy_name.lower():
                    # Get policy version
                    try:
                        policy_version = iam_client.get_policy_version(
                            PolicyArn=policy_arn,
                            VersionId=policy["DefaultVersionId"],
                        )
                        document = policy_version["PolicyVersion"]["Document"]

                        # Simple check for wildcard actions
                        if self._has_wildcard_action(document):
                            findings.append(
                                Finding(
                                    finding_id=f"aws-iam-wildcard-{policy_name}",
                                    type="iam_overprivileged",
                                    severity="medium",
                                    title=f"IAM Policy '{policy_name}' may be overprivileged",
                                    description=f"Policy {policy_name} contains wildcard actions which may grant excessive permissions",
                                    resource=policy_arn,
                                    region="global",
                                    provider="aws",
                                )
                            )
                    except Exception:
                        pass

        except Exception as e:
            findings.append(
                Finding(
                    finding_id=f"aws-scan-error-iam",
                    type="scan_error",
                    severity="info",
                    title="Error scanning AWS IAM",
                    description=f"Error occurred while scanning IAM: {str(e)}",
                    resource="aws",
                    region="global",
                    provider="aws",
                )
            )

        return findings

    def scan_networking(self, region: Optional[str] = None) -> List[Finding]:
        """Scan AWS networking resources."""
        findings = []

        if not self.authenticated:
            if not self.authenticate():
                return findings

        try:
            ec2_client = self.session.client("ec2", region_name=region or "us-east-1")

            # Check Security Groups
            security_groups = ec2_client.describe_security_groups()
            for sg in security_groups.get("SecurityGroups", []):
                sg_id = sg["GroupId"]
                sg_name = sg.get("GroupName", "")

                # Check for overly permissive rules
                for rule in sg.get("IpPermissions", []):
                    for ip_range in rule.get("IpRanges", []):
                        cidr = ip_range.get("CidrIp", "")
                        if cidr == "0.0.0.0/0":
                            port = rule.get("FromPort", "all")
                            protocol = rule.get("IpProtocol", "-1")
                            findings.append(
                                Finding(
                                    finding_id=f"aws-sg-open-{sg_id}-{port}",
                                    type="security_group_open",
                                    severity="high",
                                    title=f"Security Group '{sg_name}' allows open access",
                                    description=f"Security group {sg_id} allows access from 0.0.0.0/0 on port {port}/{protocol}",
                                    resource=f"arn:aws:ec2:{region}:security-group/{sg_id}",
                                    region=region or "us-east-1",
                                    provider="aws",
                                )
                            )

        except Exception as e:
            findings.append(
                Finding(
                    finding_id=f"aws-scan-error-networking",
                    type="scan_error",
                    severity="info",
                    title="Error scanning AWS networking",
                    description=f"Error occurred while scanning networking: {str(e)}",
                    resource="aws",
                    region=region or "us-east-1",
                    provider="aws",
                )
            )

        return findings

    def scan_compute(self, region: Optional[str] = None) -> List[Finding]:
        """Scan AWS compute resources (EC2 instances)."""
        findings = []

        if not self.authenticated:
            if not self.authenticate():
                return findings

        reg = region or "us-east-1"
        try:
            ec2_client = self.session.client("ec2", region_name=reg)
            ec2_resource = self.session.resource("ec2", region_name=reg)

            # EC2 instances
            paginator = ec2_client.get_paginator("describe_instances")
            for page in paginator.paginate():
                for reservation in page.get("Reservations", []):
                    for instance in reservation.get("Instances", []):
                        instance_id = instance.get("InstanceId", "")
                        if not instance_id:
                            continue

                        # Check 1: IMDSv2 required (CIS 4.2)
                        metadata_options = instance.get("MetadataOptions") or {}
                        if metadata_options.get("HttpTokens") != "required":
                            findings.append(
                                Finding(
                                    finding_id=f"aws-ec2-imdsv1-{instance_id}",
                                    type="ec2_imdsv1",
                                    severity="medium",
                                    title=f"EC2 instance '{instance_id}' does not require IMDSv2",
                                    description="Instance Metadata Service v1 is allowed; prefer IMDSv2 to reduce SSRF risk",
                                    resource=f"arn:aws:ec2:{reg}:instance/{instance_id}",
                                    region=reg,
                                    provider="aws",
                                    remediation={
                                        "immediate": [
                                            "Set instance metadata options to require IMDSv2",
                                        ],
                                        "short_term": [
                                            "Use AWS Systems Manager or modify instance attribute: HttpTokens=required",
                                        ],
                                    },
                                )
                            )

                        # Check 2: Public IP on instance (exposure)
                        public_ip = instance.get("PublicIpAddress")
                        if public_ip and instance.get("State", {}).get("Name") == "running":
                            # Only flag if no obvious bastion/load-balancer context
                            findings.append(
                                Finding(
                                    finding_id=f"aws-ec2-public-ip-{instance_id}",
                                    type="ec2_public_ip",
                                    severity="low",
                                    title=f"EC2 instance '{instance_id}' has a public IP",
                                    description=f"Instance {instance_id} has public IP {public_ip}; ensure it is intended and protected",
                                    resource=f"arn:aws:ec2:{reg}:instance/{instance_id}",
                                    region=reg,
                                    provider="aws",
                                    remediation={
                                        "immediate": [
                                            "Review whether this instance must be publicly reachable",
                                        ],
                                        "short_term": [
                                            "Prefer private instances behind a load balancer or bastion host",
                                        ],
                                    },
                                )
                            )

            # EBS volumes: unencrypted
            for page in ec2_client.get_paginator("describe_volumes").paginate():
                for vol in page.get("Volumes", []):
                    if vol.get("Encrypted") is False:
                        vol_id = vol.get("VolumeId", "")
                        findings.append(
                            Finding(
                                finding_id=f"aws-ebs-unencrypted-{vol_id}",
                                type="ebs_unencrypted",
                                severity="medium",
                                title=f"EBS volume '{vol_id}' is not encrypted",
                                description=f"Volume {vol_id} has server-side encryption disabled",
                                resource=f"arn:aws:ec2:{reg}:volume/{vol_id}",
                                region=reg,
                                provider="aws",
                                remediation={
                                    "immediate": [
                                        "Enable encryption on the volume or create an encrypted copy",
                                    ],
                                    "short_term": [
                                        "Use default EBS encryption at the account/region level",
                                    ],
                                },
                            )
                        )

        except Exception as e:
            findings.append(
                Finding(
                    finding_id="aws-scan-error-compute",
                    type="scan_error",
                    severity="info",
                    title="Error scanning AWS compute",
                    description=f"Error occurred while scanning compute: {str(e)}",
                    resource="aws",
                    region=reg,
                    provider="aws",
                )
            )

        return findings

    def scan_audit_logging(self, region: Optional[str] = None) -> List[Finding]:
        """Scan AWS CloudTrail for audit logging (CIS 3.x, NIST DE.CM)."""
        findings = []

        if not self.authenticated:
            if not self.authenticate():
                return findings

        reg = region or self.credentials.get("region", "us-east-1")
        try:
            cloudtrail = self.session.client("cloudtrail", region_name=reg)
            trails = cloudtrail.list_trails()
            trail_arns = [t.get("TrailARN") for t in trails.get("Trails", []) if t.get("TrailARN")]

            if not trail_arns:
                findings.append(
                    Finding(
                        finding_id="aws-cloudtrail-disabled",
                        type="cloudtrail_disabled",
                        severity="high",
                        title="CloudTrail is not enabled",
                        description="No CloudTrail trail found; enable at least one trail for audit logging (CIS 3.x)",
                        resource="arn:aws:cloudtrail",
                        region=reg,
                        provider="aws",
                        remediation={
                            "immediate": ["Enable CloudTrail in the AWS Console or via CloudFormation"],
                            "short_term": [
                                "Use a multi-region trail for broad coverage",
                                "Enable log file validation and encrypt logs",
                            ],
                        },
                    )
                )
                return findings

            # Check if at least one trail is logging
            any_logging = False
            for arn in trail_arns[:10]:
                try:
                    status = cloudtrail.get_trail_status(Name=arn)
                    if status.get("IsLogging"):
                        any_logging = True
                        break
                except ClientError:
                    continue

            if not any_logging:
                findings.append(
                    Finding(
                        finding_id="aws-cloudtrail-not-logging",
                        type="cloudtrail_not_logging",
                        severity="high",
                        title="CloudTrail is not logging",
                        description="CloudTrail trail(s) exist but none have logging enabled",
                        resource="arn:aws:cloudtrail",
                        region=reg,
                        provider="aws",
                        remediation={
                            "immediate": ["Start logging on at least one CloudTrail trail"],
                            "short_term": ["Enable log file validation and monitor trail status"],
                        },
                    )
                )
        except ClientError as e:
            code = e.response.get("Error", {}).get("Code", "")
            if code == "AccessDeniedException":
                findings.append(
                    Finding(
                        finding_id="aws-cloudtrail-access-denied",
                        type="scan_error",
                        severity="info",
                        title="Cannot read CloudTrail",
                        description="Insufficient permissions to list CloudTrail trails",
                        resource="arn:aws:cloudtrail",
                        region=reg,
                        provider="aws",
                    )
                )
            else:
                findings.append(
                    Finding(
                        finding_id="aws-cloudtrail-error",
                        type="scan_error",
                        severity="info",
                        title="Error scanning CloudTrail",
                        description=str(e),
                        resource="arn:aws:cloudtrail",
                        region=reg,
                        provider="aws",
                    )
                )
        except Exception as e:
            findings.append(
                Finding(
                    finding_id="aws-cloudtrail-error",
                    type="scan_error",
                    severity="info",
                    title="Error scanning CloudTrail",
                    description=str(e),
                    resource="arn:aws:cloudtrail",
                    region=reg,
                    provider="aws",
                )
            )

        return findings

    def _get_account_id(self) -> str:
        """Get AWS account ID."""
        try:
            sts = self.session.client("sts")
            identity = sts.get_caller_identity()
            return identity.get("Account", "unknown")
        except Exception:
            return "unknown"

    def _has_wildcard_action(self, policy_document: Dict[str, Any]) -> bool:
        """Check if policy document has wildcard actions."""
        if "Statement" not in policy_document:
            return False

        for statement in policy_document["Statement"]:
            if isinstance(statement, dict):
                action = statement.get("Action", [])
                if isinstance(action, str):
                    action = [action]
                if any("*" in a for a in action):
                    return True

        return False

    def get_regions(self) -> List[str]:
        """Get available AWS regions."""
        if self.regions:
            return self.regions

        try:
            if not self.authenticated:
                self.authenticate()

            ec2_client = self.session.client("ec2", region_name="us-east-1")
            regions = ec2_client.describe_regions()
            return [r["RegionName"] for r in regions.get("Regions", [])]
        except Exception:
            # Return common regions as fallback
            return [
                "us-east-1",
                "us-west-2",
                "eu-west-1",
                "ap-southeast-1",
            ]
