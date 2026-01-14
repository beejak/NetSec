"""Remediation guidance CLI commands."""

import click
import httpx
from typing import Optional


@click.group("remediation")
def remediation_group():
    """Remediation guidance commands."""
    pass


@remediation_group.command("get")
@click.argument("finding_type")
@click.option(
    "--api-url",
    default="http://localhost:8000",
    help="API base URL",
)
def get_remediation(finding_type: str, api_url: str):
    """Get remediation guidance for a finding type."""
    try:
        response = httpx.get(f"{api_url}/api/v1/remediation/{finding_type}")
        response.raise_for_status()
        data = response.json()

        click.echo(f"\nRemediation for: {data.get('finding_type', finding_type)}")
        click.echo("\nImmediate Actions:")
        for action in data.get("remediation", {}).get("immediate", []):
            click.echo(f"  • {action}")

        click.echo("\nShort-term Actions:")
        for action in data.get("remediation", {}).get("short_term", []):
            click.echo(f"  • {action}")

        click.echo("\nLong-term Actions:")
        for action in data.get("remediation", {}).get("long_term", []):
            click.echo(f"  • {action}")

        click.echo("\nVerification Steps:")
        for step in data.get("remediation", {}).get("verification", []):
            click.echo(f"  • {step}")

    except httpx.RequestError as e:
        click.echo(f"Error connecting to API: {e}", err=True)
    except httpx.HTTPStatusError as e:
        click.echo(f"API returned error: {e.response.status_code}", err=True)


@remediation_group.command("list")
@click.option(
    "--api-url",
    default="http://localhost:8000",
    help="API base URL",
)
def list_remediations(api_url: str):
    """List all available remediation types."""
    try:
        response = httpx.get(f"{api_url}/api/v1/remediation/")
        response.raise_for_status()
        data = response.json()

        click.echo(f"\nAvailable remediation types ({data.get('count', 0)}):")
        for rem_type in data.get("remediation_types", []):
            click.echo(f"  • {rem_type}")

    except httpx.RequestError as e:
        click.echo(f"Error connecting to API: {e}", err=True)
    except httpx.HTTPStatusError as e:
        click.echo(f"API returned error: {e.response.status_code}", err=True)


@remediation_group.command("search")
@click.argument("keyword")
@click.option(
    "--api-url",
    default="http://localhost:8000",
    help="API base URL",
)
def search_remediations(keyword: str, api_url: str):
    """Search remediations by keyword."""
    try:
        response = httpx.get(f"{api_url}/api/v1/remediation/search/{keyword}")
        response.raise_for_status()
        data = response.json()

        click.echo(f"\nSearch results for '{keyword}' ({data.get('count', 0)} found):")
        for result in data.get("results", []):
            click.echo(f"  • {result.get('finding_type', 'unknown')}")

    except httpx.RequestError as e:
        click.echo(f"Error connecting to API: {e}", err=True)
    except httpx.HTTPStatusError as e:
        click.echo(f"API returned error: {e.response.status_code}", err=True)
