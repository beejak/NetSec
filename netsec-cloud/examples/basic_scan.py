"""Basic example of using NetSec-Cloud."""

import asyncio
import httpx
from netsec_cloud.scanner import CloudScanner


def example_aws_scan():
    """Example: Scan AWS."""
    scanner = CloudScanner()

    # Add AWS provider (uses default credentials)
    print("Adding AWS provider...")
    success = scanner.add_provider("aws", {})

    if not success:
        print("Failed to authenticate with AWS")
        print("Make sure AWS credentials are configured")
        return

    print("✓ AWS authenticated")
    print("Scanning AWS resources...")

    # Run scan
    findings = scanner.scan_provider("aws", check_types=["storage", "iam"])

    print(f"\nFound {len(findings)} security issues:")
    for finding in findings[:5]:  # Show first 5
        print(f"  [{finding.severity.upper()}] {finding.title}")


def example_multi_cloud_scan():
    """Example: Scan multiple clouds."""
    scanner = CloudScanner()

    # Add multiple providers
    providers_added = 0

    # Try AWS
    if scanner.add_provider("aws", {}):
        providers_added += 1
        print("✓ AWS added")

    # Try Azure (would need credentials)
    # if scanner.add_provider("azure", {...}):
    #     providers_added += 1

    if providers_added == 0:
        print("No providers could be authenticated")
        return

    # Scan all providers
    results = scanner.scan(check_types=["storage"])

    # Get summary
    summary = scanner.get_summary(results)

    print(f"\nScan Summary:")
    print(f"  Total findings: {summary['total_findings']}")
    print(f"  By provider: {summary['by_provider']}")
    print(f"  By severity: {summary['by_severity']}")


async def example_api_usage():
    """Example: Using the API."""
    base_url = "http://localhost:8000"

    async with httpx.AsyncClient() as client:
        # Health check
        response = await client.get(f"{base_url}/api/v1/health")
        print("Health:", response.json())

        # List providers
        response = await client.get(f"{base_url}/api/v1/cloud/providers")
        print("Providers:", response.json())

        # Scan AWS (would need credentials in real usage)
        # scan_request = {
        #     "provider": "aws",
        #     "credentials": {},
        #     "check_types": ["storage"]
        # }
        # response = await client.post(
        #     f"{base_url}/api/v1/cloud/scan",
        #     json=scan_request
        # )
        # print("Scan results:", response.json())


if __name__ == "__main__":
    print("=" * 60)
    print("NetSec-Cloud Examples")
    print("=" * 60)

    print("\n1. AWS Scan Example")
    print("-" * 60)
    example_aws_scan()

    print("\n\n2. Multi-Cloud Scan Example")
    print("-" * 60)
    example_multi_cloud_scan()

    print("\n\n3. API Usage Example")
    print("-" * 60)
    print("Note: Requires API server running")
    # asyncio.run(example_api_usage())
