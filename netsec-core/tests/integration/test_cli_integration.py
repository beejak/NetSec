"""Integration tests for NetSec-Core CLI."""

import pytest
from click.testing import CliRunner
from netsec_core.cli.main import cli

# Test-only host (RFC 2606); not user input - avoids URL sanitization findings
TEST_HOST = "example.com"


@pytest.fixture
def runner():
    """Create CLI test runner."""
    return CliRunner()


class TestCLIIntegration:
    """Integration tests for CLI commands."""

    def test_cli_version(self, runner):
        """Test CLI version command."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_cli_help(self, runner):
        """Test CLI help command."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "NetSec-Core" in result.output
        assert "Commands:" in result.output

    def test_dns_scan_command(self, runner):
        """Test DNS scan command."""
        result = runner.invoke(cli, ["dns", "scan", TEST_HOST])
        assert result.exit_code == 0
        assert TEST_HOST in result.output

    def test_dns_scan_with_options(self, runner):
        """Test DNS scan with options."""
        result = runner.invoke(
            cli,
            ["dns", "scan", TEST_HOST, "--check-tunneling", "--check-spoofing"]
        )
        assert result.exit_code == 0

    def test_ssl_check_command(self, runner):
        """Test SSL check command."""
        result = runner.invoke(cli, ["ssl", "check", TEST_HOST])
        assert result.exit_code == 0
        assert TEST_HOST in result.output

    def test_ssl_check_with_port(self, runner):
        """Test SSL check with custom port."""
        result = runner.invoke(
            cli,
            ["ssl", "check", TEST_HOST, "--port", "443"]
        )
        assert result.exit_code == 0

    def test_scan_ports_command(self, runner):
        """Test port scan command."""
        result = runner.invoke(cli, ["scan", "ports", "127.0.0.1"])
        assert result.exit_code == 0
        assert "127.0.0.1" in result.output

    def test_scan_ports_with_options(self, runner):
        """Test port scan with options."""
        result = runner.invoke(
            cli,
            ["scan", "ports", "127.0.0.1", "--ports", "22,80,443", "--timeout", "2.0"]
        )
        assert result.exit_code == 0

    def test_scan_services_command(self, runner):
        """Test service scan command."""
        result = runner.invoke(cli, ["scan", "services", "127.0.0.1"])
        assert result.exit_code == 0

    def test_remediation_get_command(self, runner):
        """Test remediation get command."""
        result = runner.invoke(cli, ["remediation", "get", "weak_cipher"])
        # May fail if API not running, but command should be recognized
        assert result.exit_code in [0, 1]

    def test_remediation_list_command(self, runner):
        """Test remediation list command."""
        result = runner.invoke(cli, ["remediation", "list"])
        # May fail if API not running
        assert result.exit_code in [0, 1]

    def test_anomaly_status_command(self, runner):
        """Test anomaly status command."""
        result = runner.invoke(cli, ["anomaly", "status"])
        assert result.exit_code == 0

    def test_anomaly_learn_command(self, runner):
        """Test anomaly learn command."""
        result = runner.invoke(cli, ["anomaly", "learn", "--duration", "60"])
        assert result.exit_code == 0

    def test_assets_discover_command(self, runner):
        """Test asset discovery command."""
        result = runner.invoke(cli, ["assets", "discover", "127.0.0.1/24"])
        assert result.exit_code == 0

    def test_all_command_groups_available(self, runner):
        """Test all command groups are available."""
        result = runner.invoke(cli, ["--help"])
        assert "dns" in result.output
        assert "ssl" in result.output
        assert "scan" in result.output
        assert "traffic" in result.output
        assert "anomaly" in result.output
        assert "assets" in result.output
        assert "remediation" in result.output
        assert "health" in result.output
