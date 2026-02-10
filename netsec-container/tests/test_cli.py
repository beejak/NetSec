"""CLI tests for NetSec-Container."""

import pytest
from netsec_container.cli.main import cli


@pytest.mark.cli
def test_cli_help(cli_runner):
    """CLI --help shows scan."""
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "scan" in result.output or "Scan" in result.output


@pytest.mark.cli
def test_cli_scan_help(cli_runner):
    """scan --help shows options."""
    result = cli_runner.invoke(cli, ["scan", "--help"])
    assert result.exit_code == 0
    assert "image" in result.output or "format" in result.output


@pytest.mark.cli
def test_cli_scan_smoke(cli_runner):
    """CLI scan runs (may fail without Docker/image); checks command exists."""
    result = cli_runner.invoke(cli, ["scan", "nonexistent:999", "--no-vuln", "--no-secrets", "--no-sbom"])
    # Exit 0 if scan completed (empty image), 1 if failed (no Docker/pull error)
    assert result.exit_code in (0, 1)
    assert "Scanning" in result.output or "Scan" in result.output or "failed" in result.output.lower() or "error" in result.output.lower()


@pytest.mark.cli
def test_cli_serve_help(cli_runner):
    """serve --help shows host/port options."""
    result = cli_runner.invoke(cli, ["serve", "--help"])
    assert result.exit_code == 0
    assert "host" in result.output.lower() or "port" in result.output.lower()
