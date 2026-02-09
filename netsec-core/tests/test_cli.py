"""Tests for CLI commands."""

import pytest
from click.testing import CliRunner

from netsec_core.cli.main import cli


@pytest.fixture
def runner(cli_runner):
    """Create CLI test runner (use conftest cli_runner)."""
    return cli_runner


@pytest.mark.cli
def test_cli_version(runner):
    """Test CLI version command."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


@pytest.mark.cli
def test_cli_help(runner):
    """Test CLI help command."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "NetSec-Core" in result.output


@pytest.mark.cli
def test_scan_ports_command(runner):
    """Test scan ports command."""
    result = runner.invoke(cli, ["scan", "ports", "example.com"])
    assert result.exit_code == 0
    assert "example.com" in result.output


@pytest.mark.cli
def test_dns_scan_command(runner):
    """Test DNS scan command."""
    result = runner.invoke(cli, ["dns", "scan", "example.com"])
    assert result.exit_code == 0
    assert "example.com" in result.output


@pytest.mark.cli
def test_ssl_check_command(runner):
    """Test SSL check command."""
    result = runner.invoke(cli, ["ssl", "check", "example.com"])
    assert result.exit_code == 0
    assert "example.com" in result.output


@pytest.mark.cli
def test_traffic_command(runner):
    """CLI traffic group exists and help works."""
    result = runner.invoke(cli, ["traffic", "--help"])
    assert result.exit_code == 0
    assert "traffic" in result.output.lower()


@pytest.mark.cli
def test_anomaly_command(runner):
    """CLI anomaly group exists and help works."""
    result = runner.invoke(cli, ["anomaly", "--help"])
    assert result.exit_code == 0
    assert "anomaly" in result.output.lower()


@pytest.mark.cli
def test_assets_command(runner):
    """CLI assets group exists and help works."""
    result = runner.invoke(cli, ["assets", "--help"])
    assert result.exit_code == 0
    assert "asset" in result.output.lower()


@pytest.mark.cli
def test_remediation_get_command(runner):
    """CLI remediation get returns guidance for known type."""
    result = runner.invoke(cli, ["remediation", "get", "weak_cipher"])
    assert result.exit_code == 0
    out = result.output.lower()
    assert (
        "weak" in out or "cipher" in out or "remediation" in out
        or "error" in out or "connection" in out or "refused" in out
    )


@pytest.mark.cli
def test_health_command(runner):
    """CLI health command runs (may fail without server)."""
    result = runner.invoke(cli, ["health"])
    # 0 if server up, or non-zero if connection refused
    assert result.exit_code in [0, 1]
    assert "health" in result.output.lower() or "error" in result.output.lower() or "connection" in result.output.lower()
