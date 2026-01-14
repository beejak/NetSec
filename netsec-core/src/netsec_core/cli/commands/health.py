"""Health check CLI command."""

import sys
import click
import httpx
from typing import Optional


@click.command("health")
@click.option(
    "--api-url",
    default="http://localhost:8000",
    help="API base URL",
)
def health_command(api_url: str):
    """Check API health status."""
    try:
        response = httpx.get(f"{api_url}/api/v1/health", timeout=5.0)
        response.raise_for_status()
        data = response.json()
        click.echo(f"✓ API Status: {data['status']}")
        click.echo(f"✓ Version: {data['version']}")
        click.echo(f"✓ Timestamp: {data['timestamp']}")
    except httpx.RequestError as e:
        click.echo(f"✗ Error connecting to API: {e}", err=True)
        sys.exit(1)
    except httpx.HTTPStatusError as e:
        click.echo(f"✗ API returned error: {e.response.status_code}", err=True)
        sys.exit(1)
