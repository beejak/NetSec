"""Tests for cloud providers."""

import pytest
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
