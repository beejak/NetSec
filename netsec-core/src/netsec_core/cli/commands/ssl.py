"""SSL/TLS security CLI commands."""

import click
from netsec_core.core.ssl_scanner import SSLScanner


@click.group("ssl")
def ssl_group():
    """SSL/TLS security commands."""
    pass


@ssl_group.command("check")
@click.argument("hostname")
@click.option(
    "--port",
    type=int,
    default=443,
    help="Port to check",
)
@click.option(
    "--check-expiration/--no-check-expiration",
    default=True,
    help="Check certificate expiration",
)
@click.option(
    "--check-ciphers/--no-check-ciphers",
    default=True,
    help="Check for weak ciphers",
)
@click.option(
    "--check-chain/--no-check-chain",
    default=True,
    help="Validate certificate chain",
)
def check_ssl(
    hostname: str, port: int, check_expiration: bool, check_ciphers: bool, check_chain: bool
):
    """Check SSL/TLS certificate."""
    scanner = SSLScanner()

    click.echo(f"Checking SSL/TLS certificate for {hostname}:{port}...")

    try:
        result = scanner.check_certificate(
            hostname=hostname,
            port=port,
            check_expiration=check_expiration,
            check_ciphers=check_ciphers,
            check_chain=check_chain,
        )

        # Display certificate info
        if result.get("certificate_info"):
            cert_info = result["certificate_info"]
            if not cert_info.get("error"):
                click.echo(f"\nCertificate Information:")
                click.echo(f"  Common Name: {cert_info.get('common_name', 'Unknown')}")
                click.echo(f"  Issuer: {cert_info.get('issuer_name', 'Unknown')}")
                click.echo(f"  Valid From: {cert_info.get('not_valid_before', 'Unknown')}")
                click.echo(f"  Valid To: {cert_info.get('not_valid_after', 'Unknown')}")

        # Display findings
        findings = result.get("findings", [])
        if findings:
            click.echo(f"\nFound {len(findings)} security issue(s):")
            for finding in findings:
                severity = finding.get("severity", "info").upper()
                click.echo(f"  [{severity}] {finding.get('type', 'unknown')}: {finding.get('description', '')}")
        else:
            click.echo("\n✓ No security issues detected")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@ssl_group.command("list")
def list_certificates():
    """List monitored certificates."""
    scanner = SSLScanner()

    click.echo("Listing monitored certificates...")
    click.echo("Note: Certificate monitoring requires database storage (to be implemented)")

    try:
        result = scanner.list_certificates()
        click.echo(f"\n{result.get('message', 'No certificates stored')}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
