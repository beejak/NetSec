"""CLI interface for netsec-container"""

import click
import asyncio
import sys
from pathlib import Path

from netsec_container import ContainerScanner


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """NetSec-Container: Lightweight Container Security Scanner"""
    pass


@cli.command()
@click.argument("image")
@click.option("--image-file", type=click.Path(exists=True), help="Path to saved image tar file")
@click.option("--dockerfile", type=click.Path(exists=True), help="Path to Dockerfile")
@click.option("--format", type=click.Choice(["pdf", "csv", "json"]), default="pdf", help="Report format")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option("--llm", is_flag=True, help="Enable LLM-powered remediation")
@click.option("--llm-provider", type=click.Choice(["openai", "anthropic"]), default="openai", help="LLM provider")
@click.option("--llm-model", default="gpt-4", help="LLM model name")
@click.option("--fail-on", type=click.Choice(["critical", "high", "medium", "low"]), help="Exit with error if issues found")
@click.option("--no-vuln", is_flag=True, help="Disable vulnerability scanning")
@click.option("--no-secrets", is_flag=True, help="Disable secrets scanning")
@click.option("--no-sbom", is_flag=True, help="Disable SBOM generation")
def scan(
    image,
    image_file,
    dockerfile,
    format,
    output,
    llm,
    llm_provider,
    llm_model,
    fail_on,
    no_vuln,
    no_secrets,
    no_sbom,
):
    """Scan container image for security issues"""
    click.echo(f"🔍 Scanning container image: {image}")
    
    scanner = ContainerScanner(
        enable_vulnerability=not no_vuln,
        enable_secrets=not no_secrets,
        enable_sbom=not no_sbom,
        enable_dockerfile=dockerfile is not None,
        enable_llm=llm,
        llm_provider=llm_provider if llm else None,
        llm_model=llm_model if llm else None,
    )
    
    try:
        results = scanner.scan_image(
            image=image,
            image_file=image_file,
            dockerfile_path=dockerfile,
        )
        
        # Display summary
        click.echo(f"\n📊 Scan Results:")
        click.echo(f"  Risk Score: {results.risk_score:.1f}/100 ({results.risk_level.upper()})")
        click.echo(f"  Vulnerabilities: {len(results.vulnerabilities)}")
        click.echo(f"  Secrets: {len(results.secrets)}")
        click.echo(f"  Scan Duration: {results.scan_duration:.2f}s")
        
        # Generate report
        if format:
            report_path = scanner.generate_report(results, format=format, output=output)
            click.echo(f"\n📄 Report generated: {report_path}")
        
        # Check fail-on
        if fail_on:
            if results.risk_level == fail_on or (
                fail_on == "high" and results.risk_level in ["critical", "high"]
            ) or (
                fail_on == "medium" and results.risk_level in ["critical", "high", "medium"]
            ):
                click.echo(f"\n❌ Found {results.risk_level} issues. Failing build.")
                sys.exit(1)
        
        click.echo("\n✅ Scan completed successfully!")
    
    except Exception as e:
        click.echo(f"\n❌ Scan failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=8080, type=int, help="Port to bind to")
def serve(host, port):
    """Start web interface server"""
    click.echo(f"🌐 Starting web interface on http://{host}:{port}")
    
    try:
        import uvicorn
        from netsec_container.api.main import app
        uvicorn.run(app, host=host, port=port)
    except ImportError:
        click.echo("❌ Web interface requires uvicorn. Install with: pip install uvicorn", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
