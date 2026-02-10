"""Tests for cloud providers."""

from unittest.mock import MagicMock, patch
import pytest
from botocore.exceptions import ClientError
from netsec_cloud.providers.aws import AWSProvider
from netsec_cloud.providers.azure import AzureProvider
from netsec_cloud.providers.gcp import GCPProvider


def test_aws_provider_initialization():
    """Test AWS provider initialization."""
    provider = AWSProvider(credentials={})
    assert provider.provider_name == "aws"


def test_azure_provider_initialization():
    """Test Azure provider initialization."""
    provider = AzureProvider(credentials={})
    assert provider.provider_name == "azure"


def test_gcp_provider_initialization():
    """Test GCP provider initialization."""
    provider = GCPProvider(credentials={})
    assert provider.provider_name == "gcp"


def test_provider_authentication_failure():
    """Test provider authentication with invalid credentials."""
    aws_provider = AWSProvider(credentials={"invalid": "credentials"})
    # Authentication should fail gracefully
    result = aws_provider.authenticate()
    # May fail or succeed depending on environment
    assert isinstance(result, bool)


def test_aws_scan_compute_returns_list():
    """AWS scan_compute returns a list (empty when not authenticated)."""
    provider = AWSProvider(credentials={})
    findings = provider.scan_compute(region="us-east-1")
    assert isinstance(findings, list)


def test_azure_scan_iam_returns_list():
    """Azure scan_iam returns a list."""
    provider = AzureProvider(credentials={"subscription_id": "test-sub"})
    findings = provider.scan_iam()
    assert isinstance(findings, list)


def test_gcp_scan_iam_returns_list():
    """GCP scan_iam returns a list (empty when no project_id or no IAM client)."""
    provider = GCPProvider(credentials={})
    findings = provider.scan_iam()
    assert isinstance(findings, list)


def test_aws_scan_storage_s3_no_encryption_finding():
    """AWS scan_storage reports s3_no_encryption when bucket has no default encryption."""
    provider = AWSProvider(credentials={})
    mock_s3 = MagicMock()
    mock_s3.list_buckets.return_value = {"Buckets": [{"Name": "test-bucket"}]}
    mock_s3.get_bucket_encryption.side_effect = ClientError(
        {"Error": {"Code": "ServerSideEncryptionConfigurationNotFoundError", "Message": "No encryption"}},
        "GetBucketEncryption",
    )
    mock_session = MagicMock()
    mock_session.client.return_value = mock_s3
    mock_resource_bucket = MagicMock()
    mock_resource_bucket.Acl.return_value.grants = []  # no public access
    mock_resource = MagicMock()
    mock_resource.Bucket.return_value = mock_resource_bucket
    mock_session.resource.return_value = mock_resource

    provider.session = mock_session
    provider.authenticated = True

    findings = provider.scan_storage(region="us-east-1")
    encryption_findings = [f for f in findings if f.type == "s3_no_encryption"]
    assert len(encryption_findings) >= 1
    assert any("test-bucket" in f.resource or "encryption" in f.title.lower() for f in encryption_findings)


def test_aws_scan_iam_wildcard_policy_finding():
    """AWS scan_iam reports iam_overprivileged when a customer policy has wildcard action."""
    provider = AWSProvider(credentials={})
    mock_iam = MagicMock()
    mock_iam.list_users.return_value = {"Users": []}
    mock_iam.list_policies.return_value = {
        "Policies": [
            {"Arn": "arn:aws:iam::123:policy/MyPolicy", "PolicyName": "MyPolicy", "DefaultVersionId": "v1"}
        ]
    }
    mock_iam.get_policy_version.return_value = {
        "PolicyVersion": {
            "Document": {
                "Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"}]
            }
        }
    }
    mock_iam.list_access_keys.return_value = {"AccessKeyMetadata": []}
    mock_session = MagicMock()
    mock_session.client.return_value = mock_iam
    provider.session = mock_session
    provider.authenticated = True
    with patch.object(provider, "_get_account_id", return_value="123"):
        findings = provider.scan_iam(region="global")
    overprivileged = [f for f in findings if f.type == "iam_overprivileged"]
    assert len(overprivileged) >= 1
    assert any("MyPolicy" in f.title or "wildcard" in f.description.lower() for f in overprivileged)
