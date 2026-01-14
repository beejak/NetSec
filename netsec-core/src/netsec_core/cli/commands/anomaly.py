"""Anomaly detection CLI commands."""

import click
from netsec_core.core.anomaly_detector import AnomalyDetector


@click.group("anomaly")
def anomaly_group():
    """Anomaly detection commands."""
    pass


@anomaly_group.command("learn")
@click.option(
    "--duration",
    type=int,
    default=3600,
    help="Learning duration in seconds",
)
def learn_baseline(duration: int):
    """Learn baseline for anomaly detection."""
    detector = AnomalyDetector()

    click.echo(f"Learning baseline for {duration} seconds...")
    click.echo("Note: Feed traffic data to the detector to build baseline")

    try:
        result = detector.learn_baseline(duration=duration)
        click.echo(f"Status: {result.get('status')}")
        click.echo(f"Start time: {result.get('start_time')}")
        click.echo(f"Duration: {result.get('duration')} seconds")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@anomaly_group.command("detect")
@click.argument("metric")
@click.argument("value", type=float)
def detect_anomalies(metric: str, value: float):
    """Detect anomalies in network traffic."""
    detector = AnomalyDetector()

    click.echo(f"Checking {metric} = {value} for anomalies...")

    try:
        result = detector.detect_anomalies(metric=metric, value=value)

        if result.get("anomaly_detected"):
            click.echo(f"⚠️  ANOMALY DETECTED!")
            click.echo(f"  Severity: {result.get('severity', 'unknown').upper()}")
            click.echo(f"  Z-score: {result.get('z_score', 0):.2f}")
            click.echo(f"  Description: {result.get('description', '')}")
        else:
            click.echo(f"✓ No anomaly detected")
            click.echo(f"  Baseline mean: {result.get('baseline_mean', 0):.2f}")
            click.echo(f"  Baseline std: {result.get('baseline_std', 0):.2f}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@anomaly_group.command("status")
def get_status():
    """Get anomaly detection status."""
    detector = AnomalyDetector()

    try:
        status = detector.get_status()
        click.echo(f"Learning: {status.get('learning', False)}")
        click.echo(f"Baseline metrics: {', '.join(status.get('baseline_metrics', []))}")
        click.echo(f"Threshold: {status.get('threshold', 3.0)}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
