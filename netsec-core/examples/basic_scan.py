"""Basic example of using NetSec-Core API."""

import httpx
import asyncio


async def main():
    """Example usage of NetSec-Core API."""
    base_url = "http://localhost:8000"

    async with httpx.AsyncClient() as client:
        # Health check
        print("Checking API health...")
        response = await client.get(f"{base_url}/api/v1/health")
        print(f"Health Status: {response.json()}")

        # Example: Scan ports (when implemented in Week 3-4)
        # print("\nScanning ports...")
        # response = await client.post(
        #     f"{base_url}/api/v1/scan/ports",
        #     json={"target": "example.com", "ports": [80, 443]}
        # )
        # print(f"Scan Result: {response.json()}")


if __name__ == "__main__":
    asyncio.run(main())
