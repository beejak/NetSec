"""Network scanning CLI commands."""

import click
from typing import Optional, List
from netsec_core.core.network_scanner import NetworkScanner


@click.group("scan")
def scan_group():
    """Network scanning commands."""
    pass


@scan_group.command("ports")
@click.argument("target")
@click.option(
    "--ports",
    "-p",
    help="Ports to scan (comma-separated, e.g., 80,443,8080)",
)
@click.option(
    "--scan-type",
    type=click.Choice(["tcp", "udp", "syn"]),
    default="tcp",
    help="Type of scan",
)
@click.option(
    "--timeout",
    type=float,
    default=5.0,
    help="Timeout in seconds",
)
def scan_ports(target: str, ports: Optional[str], scan_type: str, timeout: float):
    """Scan target for open ports."""
    scanner = NetworkScanner()

    # Parse ports
    port_list = None
    if ports:
        try:
            port_list = [int(p.strip()) for p in ports.split(",")]
        except ValueError:
            click.echo(f"Error: Invalid port format: {ports}", err=True)
            return

    click.echo(f"Scanning {target} for open ports...")
    click.echo(f"Scan type: {scan_type}, Timeout: {timeout}s")

    try:
        result = scanner.scan_ports(
            target=target,
            ports=port_list,
            scan_type=scan_type,
            timeout=timeout,
        )

        click.echo(f"\nScan ID: {result['scan_id']}")
        click.echo(f"Open ports: {', '.join(map(str, result['open_ports'])) if result['open_ports'] else 'None'}")

        if result.get("services"):
            click.echo("\nDetected services:")
            for service in result["services"]:
                click.echo(f"  Port {service['port']}: {service.get('service', 'unknown')}")
                if service.get("banner"):
                    click.echo(f"    Banner: {service['banner'][:100]}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@scan_group.command("services")
@click.argument("target")
@click.option(
    "--ports",
    "-p",
    help="Ports to scan (comma-separated)",
)
def scan_services(target: str, ports: Optional[str]):
    """Scan target for services."""
    scanner = NetworkScanner()

    # Parse ports
    port_list = None
    if ports:
        try:
            port_list = [int(p.strip()) for p in ports.split(",")]
        except ValueError:
            click.echo(f"Error: Invalid port format: {ports}", err=True)
            return

    click.echo(f"Scanning {target} for services...")

    try:
        result = scanner.scan_services(target=target, ports=port_list)

        click.echo(f"\nScan ID: {result['scan_id']}")
        click.echo(f"Open ports: {', '.join(map(str, result['open_ports'])) if result['open_ports'] else 'None'}")

        if result.get("services"):
            click.echo("\nDetected services:")
            for service in result["services"]:
                click.echo(f"  Port {service['port']}: {service.get('service', 'unknown')} ({service.get('protocol', 'tcp')})")
                if service.get("banner"):
                    click.echo(f"    Banner: {service['banner'][:100]}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
