"""Main CLI entry point for NetSec-Cloud."""

import click
import json
from typing import Optional
from netsec_cloud.scanner import CloudScanner
from netsec_cloud.providers.aws import AWSProvider
from netsec_cloud.providers.azure import AzureProvider
from netsec_cloud.providers.gcp import GCPProvider


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version="0.1.0", prog_name="netsec-cloud")
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool):
    """
    NetSec-Cloud - Cloud Security Scanner CLI.
    
    A lightweight, API-first cloud security scanner supporting:
    - AWS (Amazon Web Services)
    - Azure (Microsoft Azure)
    - GCP (Google Cloud Platform)
    
    \b
    Examples:
        # Scan AWS S3 buckets
        netsec-cloud scan aws --checks storage
        
        # Scan Azure storage accounts
        netsec-cloud scan azure --checks storage
        
        # Scan GCP storage buckets
        netsec-cloud scan gcp --checks storage
        
        # Multi-cloud scan
        netsec-cloud scan multi --providers aws,azure
    
    \b
    For more information, visit:
    https://github.com/your-org/netsec-cloud
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

    if verbose:
        click.echo("Verbose mode enabled", err=True)
    
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command("scan")
@click.argument("provider", type=click.Choice(["aws", "azure", "gcp"]))
@click.option(
    "--credentials",
    "-c",
    type=click.Path(exists=True),
    help="Path to credentials JSON file",
)
@click.option(
    "--regions",
    "-r",
    help="Comma-separated list of regions to scan",
)
@click.option(
    "--checks",
    help="Comma-separated list of check types (storage,iam,networking,compute)",
    default="storage,iam,networking",
)
@click.option(
    "--output",
    "-o",
    type=click.Choice(["json", "table", "summary"]),
    default="summary",
    help="Output format",
)
def scan_provider(provider: str, credentials: str, regions: str, checks: str, output: str):
    """Scan a cloud provider for security issues."""
    scanner = CloudScanner()

    # Load credentials
    if credentials:
        with open(credentials, "r") as f:
            creds = json.load(f)
    else:
        # Try environment variables or default credentials
        creds = {}
        if provider == "aws":
            # boto3 will use default credentials
            creds = {}
        elif provider == "azure":
            # Azure will use default credentials
            creds = {}
        elif provider == "gcp":
            # GCP will use default credentials
            creds = {"project_id": None}

    # Parse regions
    region_list = regions.split(",") if regions else None

    # Parse checks
    check_list = checks.split(",") if checks else None

    click.echo(f"Scanning {provider.upper()}...")
    click.echo("Authenticating...")

    # Add provider
    success = scanner.add_provider(
        provider_name=provider,
        credentials=creds,
        regions=region_list,
    )

    if not success:
        click.echo(f"Error: Failed to authenticate with {provider}", err=True)
        click.echo("Please check your credentials", err=True)
        return

    click.echo("✓ Authentication successful")
    click.echo(f"Running security checks: {', '.join(check_list or ['all'])}")

    # Run scan
    findings = scanner.scan_provider(
        provider_name=provider,
        check_types=check_list,
    )

    # Display results
    if output == "json":
        import json as json_lib
        click.echo(json_lib.dumps([f.to_dict() for f in findings], indent=2))
    elif output == "summary":
        _display_summary(findings, provider)
    else:
        _display_table(findings)


def _display_summary(findings, provider: str):
    """Display scan summary."""
    click.echo(f"\n{'='*60}")
    click.echo(f"Scan Results for {provider.upper()}")
    click.echo(f"{'='*60}")

    if not findings:
        click.echo("✓ No security issues found")
        return

    # Group by severity
    by_severity = {}
    for finding in findings:
        severity = finding.severity
        by_severity[severity] = by_severity.get(severity, 0) + 1

    click.echo(f"\nTotal Findings: {len(findings)}")
    click.echo(f"  Critical: {by_severity.get('critical', 0)}")
    click.echo(f"  High: {by_severity.get('high', 0)}")
    click.echo(f"  Medium: {by_severity.get('medium', 0)}")
    click.echo(f"  Low: {by_severity.get('low', 0)}")
    click.echo(f"  Info: {by_severity.get('info', 0)}")

    # Show critical and high findings
    critical_high = [f for f in findings if f.severity in ["critical", "high"]]
    if critical_high:
        click.echo(f"\n⚠️  Critical/High Findings ({len(critical_high)}):")
        for finding in critical_high[:10]:  # Show first 10
            click.echo(f"  [{finding.severity.upper()}] {finding.title}")
            click.echo(f"    Resource: {finding.resource}")
            if finding.remediation:
                click.echo(f"    Remediation: {finding.remediation.get('immediate', ['N/A'])[0]}")


def _display_table(findings):
    """Display findings in table format."""
    click.echo("\nFindings:")
    click.echo(f"{'Severity':<10} {'Type':<20} {'Resource':<40}")
    click.echo("-" * 70)
    for finding in findings:
        click.echo(
            f"{finding.severity:<10} {finding.type:<20} {finding.resource[:40]:<40}"
        )


@cli.command("providers")
def list_providers():
    """List supported cloud providers."""
    click.echo("Supported Cloud Providers:")
    click.echo("  • AWS (Amazon Web Services)")
    click.echo("  • Azure (Microsoft Azure)")
    click.echo("  • GCP (Google Cloud Platform)")
    click.echo("\nUse 'netsec-cloud scan <provider>' to scan a provider")


if __name__ == "__main__":
    cli()
