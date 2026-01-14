"""DNS security CLI commands."""

import click
from netsec_core.core.dns_scanner import DNSScanner


@click.group("dns")
def dns_group():
    """DNS security commands."""
    pass


@dns_group.command("scan")
@click.argument("domain")
@click.option(
    "--check-tunneling/--no-check-tunneling",
    default=True,
    help="Check for DNS tunneling",
)
@click.option(
    "--check-spoofing/--no-check-spoofing",
    default=True,
    help="Check for DNS spoofing",
)
@click.option(
    "--analyze-patterns/--no-analyze-patterns",
    default=True,
    help="Analyze query patterns",
)
def scan_dns(domain: str, check_tunneling: bool, check_spoofing: bool, analyze_patterns: bool):
    """Scan domain for DNS security issues."""
    scanner = DNSScanner()

    click.echo(f"Scanning {domain} for DNS security issues...")

    try:
        result = scanner.scan_domain(
            domain=domain,
            check_tunneling=check_tunneling,
            check_spoofing=check_spoofing,
            analyze_patterns=analyze_patterns,
        )

        click.echo(f"\nDomain: {result['domain']}")

        # Display DNS records
        if result.get("domain_info"):
            info = result["domain_info"]
            if info.get("a_records"):
                click.echo(f"A records: {', '.join(info['a_records'])}")
            if info.get("mx_records"):
                click.echo(f"MX records: {len(info['mx_records'])}")

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


@dns_group.command("monitor")
@click.option(
    "--duration",
    type=int,
    default=60,
    help="Monitoring duration in seconds",
)
def monitor_dns(duration: int):
    """Monitor DNS queries in real-time."""
    scanner = DNSScanner()

    click.echo(f"Monitoring DNS queries for {duration} seconds...")
    click.echo("Note: Full DNS monitoring requires packet capture (to be implemented)")

    try:
        result = scanner.monitor_dns_queries(duration=duration)
        click.echo(f"\n{result.get('message', 'Monitoring complete')}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
