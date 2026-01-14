"""Asset discovery CLI commands."""

import click
from typing import List
from netsec_core.core.asset_discovery import AssetDiscovery


@click.group("assets")
def assets_group():
    """Asset discovery commands."""
    pass


@assets_group.command("discover")
@click.argument("network")
@click.option(
    "--ports",
    "-p",
    help="Ports to scan (comma-separated)",
)
def discover_assets(network: str, ports: str):
    """Discover assets on a network."""
    discovery = AssetDiscovery()

    # Parse ports
    port_list = None
    if ports:
        try:
            port_list = [int(p.strip()) for p in ports.split(",")]
        except ValueError:
            click.echo(f"Error: Invalid port format: {ports}", err=True)
            return

    click.echo(f"Discovering assets on {network}...")
    click.echo("This may take a while...")

    try:
        result = discovery.discover_network(network=network, ports=port_list)

        click.echo(f"\nDiscovered {result.get('assets_discovered', 0)} assets")

        for asset in result.get("assets", []):
            click.echo(f"\n  IP: {asset.get('ip')}")
            if asset.get("hostname"):
                click.echo(f"    Hostname: {asset['hostname']}")
            if asset.get("open_ports"):
                click.echo(f"    Open ports: {', '.join(map(str, asset['open_ports']))}")
            if asset.get("services"):
                click.echo(f"    Services:")
                for service in asset["services"]:
                    click.echo(f"      Port {service['port']}: {service['service']}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
