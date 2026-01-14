"""Tests for CLI commands."""

import pytest
from click.testing import CliRunner

from netsec_core.cli.main import cli


@pytest.fixture
def runner():
    """Create CLI test runner."""
    return CliRunner()


def test_cli_version(runner):
    """Test CLI version command."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_cli_help(runner):
    """Test CLI help command."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "NetSec-Core" in result.output


def test_scan_ports_command(runner):
    """Test scan ports command."""
    result = runner.invoke(cli, ["scan", "ports", "example.com"])
    assert result.exit_code == 0
    assert "example.com" in result.output


def test_dns_scan_command(runner):
    """Test DNS scan command."""
    result = runner.invoke(cli, ["dns", "scan", "example.com"])
    assert result.exit_code == 0
    assert "example.com" in result.output


def test_ssl_check_command(runner):
    """Test SSL check command."""
    result = runner.invoke(cli, ["ssl", "check", "example.com"])
    assert result.exit_code == 0
    assert "example.com" in result.output
