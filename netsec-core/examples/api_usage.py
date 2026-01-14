"""Example of using NetSec-Core API with different endpoints."""

import httpx


def health_check():
    """Example health check."""
    response = httpx.get("http://localhost:8000/api/v1/health")
    return response.json()


def example_scan_request():
    """Example scan request (placeholder for Week 3-4)."""
    # This will work once port scanning is implemented
    # response = httpx.post(
    #     "http://localhost:8000/api/v1/scan/ports",
    #     json={
    #         "target": "example.com",
    #         "ports": [80, 443, 8080],
    #         "scan_type": "tcp",
    #         "timeout": 5.0
    #     }
    # )
    # return response.json()
    return {"message": "Port scanning will be available in Week 3-4"}


if __name__ == "__main__":
    print("Health Check:", health_check())
    print("\nExample Scan Request:", example_scan_request())
