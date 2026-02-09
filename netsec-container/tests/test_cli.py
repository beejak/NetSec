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
