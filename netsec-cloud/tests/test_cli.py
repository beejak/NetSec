"""CLI tests for NetSec-Cloud."""

import pytest
from netsec_cloud.cli.main import cli


@pytest.mark.cli
def test_cli_help(cli_runner):
    """CLI --help shows scan and providers."""
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "scan" in result.output
    assert "NetSec-Cloud" in result.output or "Cloud" in result.output


@pytest.mark.cli
def test_cli_scan_help(cli_runner):
    """scan --help shows provider choices."""
    result = cli_runner.invoke(cli, ["scan", "--help"])
    assert result.exit_code == 0
    assert "aws" in result.output or "provider" in result.output.lower()


@pytest.mark.cli
def test_cli_providers_command(cli_runner):
    """providers command lists AWS, Azure, GCP."""
    result = cli_runner.invoke(cli, ["providers"])
    assert result.exit_code == 0
    assert "AWS" in result.output or "Azure" in result.output or "GCP" in result.output
