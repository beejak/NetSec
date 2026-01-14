"""Advanced usage examples for NetSec-Core."""

import asyncio
import httpx
from typing import List, Dict, Any


class NetSecCoreClient:
    """Client for interacting with NetSec-Core API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize client."""
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)

    async def health_check(self) -> Dict[str, Any]:
        """Check API health."""
        response = await self.client.get("/api/v1/health")
        response.raise_for_status()
        return response.json()

    async def scan_domain_comprehensive(self, domain: str) -> Dict[str, Any]:
        """Comprehensive domain security scan."""
        results = {}

        # DNS scan
        dns_response = await self.client.post(
            "/api/v1/dns/scan",
            json={
                "domain": domain,
                "check_tunneling": True,
                "check_spoofing": True,
                "analyze_patterns": True,
            }
        )
        results["dns"] = dns_response.json()

        # SSL check
        ssl_response = await self.client.post(
            "/api/v1/ssl/check-certificate",
            json={
                "hostname": domain,
                "port": 443,
                "check_expiration": True,
                "check_ciphers": True,
                "check_chain": True,
            }
        )
        results["ssl"] = ssl_response.json()

        return results

    async def scan_network_ports(self, target: str, ports: List[int]) -> Dict[str, Any]:
        """Scan network ports."""
        response = await self.client.post(
            "/api/v1/scan/ports",
            json={
                "target": target,
                "ports": ports,
                "scan_type": "tcp",
                "timeout": 5.0,
            }
        )
        response.raise_for_status()
        return response.json()

    async def get_remediation(self, finding_type: str) -> Dict[str, Any]:
        """Get remediation guidance."""
        response = await self.client.get(f"/api/v1/remediation/{finding_type}")
        response.raise_for_status()
        return response.json()

    async def reduce_false_positives(
        self,
        findings: List[Dict[str, Any]],
        context: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Reduce false positives using LLM."""
        response = await self.client.post(
            "/api/v1/llm/reduce-false-positives",
            json={
                "findings": findings,
                "context": context or {},
            }
        )
        response.raise_for_status()
        return response.json()

    async def generate_remediation_llm(
        self,
        finding: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate remediation using LLM."""
        response = await self.client.post(
            "/api/v1/llm/generate-remediation",
            json={"finding": finding}
        )
        response.raise_for_status()
        return response.json()

    async def close(self):
        """Close client."""
        await self.client.aclose()


async def example_comprehensive_scan():
    """Example: Comprehensive security scan."""
    client = NetSecCoreClient()

    try:
        # Health check
        health = await client.health_check()
        print(f"API Status: {health['status']}")

        # Comprehensive domain scan
        domain = "example.com"
        print(f"\nScanning {domain}...")
        results = await client.scan_domain_comprehensive(domain)

        # Display DNS results
        if "dns" in results:
            dns = results["dns"]
            print(f"\nDNS Scan Results:")
            print(f"  Findings: {len(dns.get('findings', []))}")
            for finding in dns.get("findings", []):
                print(f"    [{finding.get('severity', 'unknown').upper()}] {finding.get('type')}: {finding.get('description')}")

        # Display SSL results
        if "ssl" in results:
            ssl = results["ssl"]
            print(f"\nSSL/TLS Scan Results:")
            if ssl.get("certificate_info"):
                cert = ssl["certificate_info"]
                print(f"  Common Name: {cert.get('common_name', 'Unknown')}")
                print(f"  Valid To: {cert.get('not_valid_after', 'Unknown')}")
            print(f"  Findings: {len(ssl.get('findings', []))}")
            for finding in ssl.get("findings", []):
                print(f"    [{finding.get('severity', 'unknown').upper()}] {finding.get('type')}: {finding.get('description')}")

        # Get remediation for findings
        if results.get("ssl", {}).get("findings"):
            first_finding = results["ssl"]["findings"][0]
            finding_type = first_finding.get("type", "")
            if finding_type:
                remediation = await client.get_remediation(finding_type)
                print(f"\nRemediation for {finding_type}:")
                for step in remediation.get("remediation", {}).get("immediate", [])[:3]:
                    print(f"  • {step}")

    finally:
        await client.close()


async def example_port_scan_with_remediation():
    """Example: Port scan with remediation."""
    client = NetSecCoreClient()

    try:
        target = "127.0.0.1"
        ports = [22, 80, 443, 8080]

        print(f"Scanning {target} ports {ports}...")
        result = await client.scan_network_ports(target, ports)

        print(f"\nScan Results:")
        print(f"  Open Ports: {result.get('open_ports', [])}")
        print(f"  Services: {len(result.get('services', []))}")

        # If open ports found, get remediation
        if result.get("open_ports"):
            remediation = await client.get_remediation("open_port")
            print(f"\nRemediation for open ports:")
            for step in remediation.get("remediation", {}).get("immediate", []):
                print(f"  • {step}")

    finally:
        await client.close()


async def example_false_positive_reduction():
    """Example: Reduce false positives using LLM."""
    client = NetSecCoreClient()

    try:
        # Sample findings (may include false positives)
        findings = [
            {
                "finding_id": "1",
                "type": "dns_tunneling",
                "severity": "medium",
                "description": "Suspicious DNS pattern detected",
            },
            {
                "finding_id": "2",
                "type": "dns_pattern",
                "severity": "low",
                "description": "Unusual DNS query pattern",
            },
        ]

        print("Original findings:", len(findings))
        result = await client.reduce_false_positives(findings)

        print(f"\nAfter false positive reduction:")
        print(f"  Original: {result.get('original_count', 0)}")
        print(f"  Filtered: {result.get('filtered_count', 0)}")
        print(f"  Removed: {result.get('original_count', 0) - result.get('filtered_count', 0)}")

    finally:
        await client.close()


async def main():
    """Run examples."""
    print("=" * 60)
    print("NetSec-Core Advanced Usage Examples")
    print("=" * 60)

    # Example 1: Comprehensive scan
    print("\n1. Comprehensive Domain Scan")
    print("-" * 60)
    await example_comprehensive_scan()

    # Example 2: Port scan with remediation
    print("\n\n2. Port Scan with Remediation")
    print("-" * 60)
    await example_port_scan_with_remediation()

    # Example 3: False positive reduction
    print("\n\n3. False Positive Reduction")
    print("-" * 60)
    await example_false_positive_reduction()

    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
