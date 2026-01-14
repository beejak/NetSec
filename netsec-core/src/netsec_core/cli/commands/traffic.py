"""Traffic analysis CLI commands."""

import click
from netsec_core.core.traffic_analyzer import TrafficAnalyzer


@click.group("traffic")
def traffic_group():
    """Traffic analysis commands."""
    pass


@traffic_group.command("capture")
@click.option(
    "--interface",
    "-i",
    help="Network interface to capture on",
)
@click.option(
    "--count",
    type=int,
    help="Number of packets to capture",
)
@click.option(
    "--timeout",
    type=int,
    help="Capture timeout in seconds",
)
@click.option(
    "--filter",
    help="BPF filter string",
)
def capture_traffic(interface: str, count: int, timeout: int, filter: str):
    """Capture network traffic."""
    try:
        analyzer = TrafficAnalyzer()
        click.echo("Capturing network traffic...")
        click.echo("Press Ctrl+C to stop")

        result = analyzer.capture_traffic(
            interface=interface,
            count=count,
            timeout=timeout,
            filter_str=filter,
        )

        if "error" in result:
            click.echo(f"Error: {result['error']}", err=True)
        else:
            click.echo(f"\nCaptured {result.get('packets_captured', 0)} packets")
            click.echo(f"Detected {result.get('flows_detected', 0)} flows")

    except ImportError:
        click.echo("Error: scapy is required for traffic capture. Install with: pip install scapy", err=True)
    except KeyboardInterrupt:
        analyzer.stop_capture()
        click.echo("\nCapture stopped")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@traffic_group.command("analyze")
@click.option(
    "--pcap-file",
    help="PCAP file to analyze",
)
def analyze_traffic(pcap_file: str):
    """Analyze captured traffic."""
    try:
        analyzer = TrafficAnalyzer()
        click.echo("Analyzing traffic...")

        result = analyzer.analyze_traffic(pcap_file=pcap_file)

        if "error" in result:
            click.echo(f"Error: {result['error']}", err=True)
        else:
            click.echo(f"\nTotal packets: {result.get('total_packets', 0)}")
            click.echo(f"Total flows: {result.get('total_flows', 0)}")
            click.echo(f"\nProtocols:")
            for protocol, count in result.get("protocols", {}).items():
                click.echo(f"  {protocol}: {count}")

            if result.get("top_flows"):
                click.echo(f"\nTop flows:")
                for flow in result["top_flows"][:5]:
                    click.echo(f"  {flow['src_ip']}:{flow['src_port']} -> {flow['dst_ip']}:{flow['dst_port']} ({flow['protocol']}) - {flow['packets']} packets")

    except ImportError:
        click.echo("Error: scapy is required. Install with: pip install scapy", err=True)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
