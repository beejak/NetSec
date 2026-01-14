"""Main CLI entry point for NetSec-Core."""

import click
import sys
from typing import Optional

from netsec_core.cli.commands import (
    scan,
    dns,
    ssl,
    traffic,
    anomaly,
    health,
    assets,
    remediation,
)


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version="0.1.0", prog_name="netsec-core")
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
)
@click.option(
    "--config",
    type=click.Path(exists=True),
    help="Path to configuration file",
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool, config: str):
    """
    NetSec-Core - Network Security Foundation Toolkit CLI.
    
    A comprehensive network security toolkit providing:
    - Network scanning and service detection
    - DNS security analysis
    - SSL/TLS certificate monitoring
    - Traffic analysis and anomaly detection
    - Asset discovery
    - LLM-powered analysis
    - Remediation guidance
    
    \b
    Examples:
        # Check API health
        netsec-core health
        
        # Scan DNS security
        netsec-core dns scan example.com
        
        # Check SSL certificate
        netsec-core ssl check example.com
        
        # Scan ports
        netsec-core scan ports 127.0.0.1 --ports 22,80,443
        
        # Get remediation guidance
        netsec-core remediation get weak_cipher
    
    \b
    For more information, visit:
    https://github.com/your-org/netsec-core
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["config"] = config

    if verbose:
        click.echo("Verbose mode enabled", err=True)
    
    # Show help if no command provided
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# Register command groups
cli.add_command(scan.scan_group)
cli.add_command(dns.dns_group)
cli.add_command(ssl.ssl_group)
cli.add_command(traffic.traffic_group)
cli.add_command(anomaly.anomaly_group)
cli.add_command(assets.assets_group)
cli.add_command(remediation.remediation_group)
cli.add_command(health.health_command)


if __name__ == "__main__":
    cli()
