# NetSec-Core Testing Guide

This guide will help you test the current implementation of NetSec-Core.

## Prerequisites

1. **Python 3.10+** installed
2. **Virtual environment** (recommended)
3. **Dependencies** installed

## Setup

### 1. Create Virtual Environment

```bash
cd netsec-core
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies (for testing)
pip install -r requirements-dev.txt

# Install package in development mode
pip install -e .
```

## Testing Methods

### Method 1: Run Test Suite

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=netsec_core --cov-report=term-missing

# Run specific test file
pytest tests/test_api_health.py -v
```

### Method 2: Test API Server

#### Start the API Server

```bash
# Option 1: Using uvicorn directly
uvicorn netsec_core.api.main:app --reload

# Option 2: Using the run script
python run_api.py
```

The API will be available at `http://localhost:8000`

#### Test API Endpoints

**Using curl:**

```bash
# Health check
curl http://localhost:8000/api/v1/health

# DNS scan
curl -X POST "http://localhost:8000/api/v1/dns/scan" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com", "check_tunneling": true, "check_spoofing": true, "analyze_patterns": true}'

# SSL check
curl -X POST "http://localhost:8000/api/v1/ssl/check-certificate" \
  -H "Content-Type: application/json" \
  -d '{"hostname": "example.com", "port": 443, "check_expiration": true, "check_ciphers": true, "check_chain": true}'

# Port scan
curl -X POST "http://localhost:8000/api/v1/scan/ports" \
  -H "Content-Type: application/json" \
  -d '{"target": "127.0.0.1", "ports": [22, 80, 443], "scan_type": "tcp", "timeout": 2.0}'
```

**Using Python:**

```python
import httpx

# Health check
response = httpx.get("http://localhost:8000/api/v1/health")
print(response.json())

# DNS scan
response = httpx.post(
    "http://localhost:8000/api/v1/dns/scan",
    json={
        "domain": "example.com",
        "check_tunneling": True,
        "check_spoofing": True,
        "analyze_patterns": True
    }
)
print(response.json())

# SSL check
response = httpx.post(
    "http://localhost:8000/api/v1/ssl/check-certificate",
    json={
        "hostname": "example.com",
        "port": 443,
        "check_expiration": True,
        "check_ciphers": True,
        "check_chain": True
    }
)
print(response.json())
```

**Using API Documentation:**

Visit `http://localhost:8000/api/docs` in your browser for interactive API testing.

### Method 3: Test CLI Commands

```bash
# Check CLI is installed
netsec-core --help

# Health check (requires API server running)
netsec-core health

# DNS scan
netsec-core dns scan example.com

# SSL check
netsec-core ssl check example.com

# Port scan
netsec-core scan ports 127.0.0.1 --ports 22,80,443

# Service scan
netsec-core scan services 127.0.0.1 --ports 22,80

# Anomaly detection status
netsec-core anomaly status

# Asset discovery (may take time)
netsec-core assets discover 127.0.0.1/24 --ports 22,80,443
```

## Test Scenarios

### Scenario 1: Basic Functionality Test

```bash
# 1. Start API server
uvicorn netsec_core.api.main:app --reload

# 2. In another terminal, test health
curl http://localhost:8000/api/v1/health

# 3. Test DNS scanning
netsec-core dns scan google.com

# 4. Test SSL checking
netsec-core ssl check google.com

# 5. Test port scanning (localhost)
netsec-core scan ports 127.0.0.1 --ports 22,80,443
```

### Scenario 2: API Integration Test

```python
# test_integration.py
import httpx
import json

base_url = "http://localhost:8000"

# Test health
response = httpx.get(f"{base_url}/api/v1/health")
print("Health:", response.json())

# Test DNS scan
response = httpx.post(
    f"{base_url}/api/v1/dns/scan",
    json={"domain": "example.com", "check_tunneling": True}
)
print("DNS Scan:", json.dumps(response.json(), indent=2))

# Test SSL check
response = httpx.post(
    f"{base_url}/api/v1/ssl/check-certificate",
    json={"hostname": "example.com", "port": 443}
)
print("SSL Check:", json.dumps(response.json(), indent=2))
```

Run with: `python test_integration.py`

### Scenario 3: Error Handling Test

```bash
# Test invalid domain
netsec-core dns scan invalid-domain-that-does-not-exist-12345.com

# Test invalid hostname
netsec-core ssl check invalid-hostname-12345.com

# Test unreachable target
netsec-core scan ports 192.168.255.255 --ports 80
```

## Expected Results

### DNS Scanner
- Should resolve DNS records
- Should detect potential tunneling (if suspicious patterns)
- Should return findings with severity levels

### SSL Scanner
- Should retrieve certificate information
- Should check expiration dates
- Should detect weak ciphers (if present)
- Should return certificate details

### Network Scanner
- Should scan specified ports
- Should detect open ports
- Should identify services
- Should return scan results

### Traffic Analyzer
- Requires scapy: `pip install scapy`
- Requires appropriate permissions (may need sudo/Admin)
- Should capture packets on specified interface

### Anomaly Detector
- Should learn baseline when started
- Should detect anomalies based on z-score
- Should return severity levels

### Asset Discovery
- Should discover hosts on network
- Should identify open ports
- Should detect services
- May take time for large networks

## Troubleshooting

### Issue: Module not found
**Solution:** Make sure you installed the package:
```bash
pip install -e .
```

### Issue: scapy not available
**Solution:** Install scapy for traffic analysis:
```bash
pip install scapy
```

### Issue: Permission denied (traffic capture)
**Solution:** On Linux/Mac, may need sudo:
```bash
sudo netsec-core traffic capture
```

### Issue: DNS resolution fails
**Solution:** Check network connectivity and DNS settings

### Issue: SSL certificate check fails
**Solution:** 
- Check if hostname is reachable
- Verify port 443 is open
- Check firewall settings

### Issue: Port scan shows no open ports
**Solution:**
- Verify target is reachable
- Check firewall settings
- Try scanning common ports (80, 443, 22)

## Performance Testing

### Load Test API

```python
# load_test.py
import httpx
import asyncio
import time

async def test_endpoint(url, data=None):
    async with httpx.AsyncClient() as client:
        if data:
            response = await client.post(url, json=data)
        else:
            response = await client.get(url)
        return response.status_code

async def load_test():
    base_url = "http://localhost:8000"
    tasks = []
    
    # Create 10 concurrent requests
    for i in range(10):
        tasks.append(test_endpoint(f"{base_url}/api/v1/health"))
    
    start = time.time()
    results = await asyncio.gather(*tasks)
    end = time.time()
    
    print(f"10 requests completed in {end - start:.2f} seconds")
    print(f"Success rate: {sum(1 for r in results if r == 200) / len(results) * 100:.1f}%")

asyncio.run(load_test())
```

## Next Steps

After testing:
1. Review test results
2. Check for any errors or warnings
3. Verify all features work as expected
4. Report any issues found
5. Proceed to Week 7-8 implementation if all tests pass

## Test Checklist

- [ ] API server starts successfully
- [ ] Health endpoint returns 200
- [ ] DNS scanner works for valid domains
- [ ] SSL scanner works for valid hostnames
- [ ] Network scanner works for localhost
- [ ] CLI commands execute without errors
- [ ] Test suite passes (pytest)
- [ ] API documentation accessible at /api/docs
- [ ] Error handling works for invalid inputs
- [ ] All modules import correctly
