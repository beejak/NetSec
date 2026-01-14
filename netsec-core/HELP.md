# NetSec-Core Help Guide

Complete help documentation for NetSec-Core CLI commands and API usage.

## Table of Contents

- [CLI Commands](#cli-commands)
- [API Endpoints](#api-endpoints)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## CLI Commands

### Main Command

```bash
netsec-core [OPTIONS] COMMAND [ARGS]...
```

**Options:**
- `-h, --help` - Show help message
- `-v, --verbose` - Enable verbose output
- `--version` - Show version
- `--config PATH` - Path to configuration file

### Health Commands

#### Check API Health

```bash
netsec-core health [OPTIONS]
```

**Options:**
- `--api-url TEXT` - API base URL (default: http://localhost:8000)

**Example:**
```bash
netsec-core health
netsec-core health --api-url http://api.example.com:8000
```

### DNS Security Commands

#### Scan DNS Security

```bash
netsec-core dns scan DOMAIN [OPTIONS]
```

**Options:**
- `--check-tunneling / --no-check-tunneling` - Check for DNS tunneling (default: True)
- `--check-spoofing / --no-check-spoofing` - Check for DNS spoofing (default: True)
- `--analyze-patterns / --no-analyze-patterns` - Analyze query patterns (default: True)

**Example:**
```bash
netsec-core dns scan example.com
netsec-core dns scan example.com --no-check-tunneling
```

#### Monitor DNS Queries

```bash
netsec-core dns monitor [OPTIONS]
```

**Options:**
- `--duration INTEGER` - Monitoring duration in seconds (default: 60)

**Example:**
```bash
netsec-core dns monitor --duration 120
```

### SSL/TLS Commands

#### Check SSL Certificate

```bash
netsec-core ssl check HOSTNAME [OPTIONS]
```

**Options:**
- `--port INTEGER` - Port to check (default: 443)
- `--check-expiration / --no-check-expiration` - Check certificate expiration (default: True)
- `--check-ciphers / --no-check-ciphers` - Check for weak ciphers (default: True)
- `--check-chain / --no-check-chain` - Validate certificate chain (default: True)

**Example:**
```bash
netsec-core ssl check example.com
netsec-core ssl check example.com --port 8443
netsec-core ssl check example.com --no-check-ciphers
```

#### List Certificates

```bash
netsec-core ssl list
```

### Network Scanner Commands

#### Scan Ports

```bash
netsec-core scan ports TARGET [OPTIONS]
```

**Options:**
- `-p, --ports TEXT` - Ports to scan (comma-separated, e.g., 80,443,8080)
- `--scan-type [tcp|udp|syn]` - Type of scan (default: tcp)
- `--timeout FLOAT` - Timeout in seconds (default: 5.0)

**Example:**
```bash
netsec-core scan ports 127.0.0.1
netsec-core scan ports example.com --ports 22,80,443,8080
netsec-core scan ports 192.168.1.1 --scan-type tcp --timeout 3.0
```

#### Scan Services

```bash
netsec-core scan services TARGET [OPTIONS]
```

**Options:**
- `-p, --ports TEXT` - Ports to scan (comma-separated)

**Example:**
```bash
netsec-core scan services 127.0.0.1
netsec-core scan services example.com --ports 22,80,443
```

### Traffic Analysis Commands

#### Capture Traffic

```bash
netsec-core traffic capture [OPTIONS]
```

**Options:**
- `-i, --interface TEXT` - Network interface to capture on
- `--count INTEGER` - Number of packets to capture
- `--timeout INTEGER` - Capture timeout in seconds
- `--filter TEXT` - BPF filter string

**Example:**
```bash
netsec-core traffic capture
netsec-core traffic capture --interface eth0 --count 100
netsec-core traffic capture --filter "tcp port 80"
```

#### Analyze Traffic

```bash
netsec-core traffic analyze [OPTIONS]
```

**Options:**
- `--pcap-file TEXT` - PCAP file to analyze

**Example:**
```bash
netsec-core traffic analyze --pcap-file capture.pcap
```

### Anomaly Detection Commands

#### Learn Baseline

```bash
netsec-core anomaly learn [OPTIONS]
```

**Options:**
- `--duration INTEGER` - Learning duration in seconds (default: 3600)

**Example:**
```bash
netsec-core anomaly learn --duration 7200
```

#### Detect Anomalies

```bash
netsec-core anomaly detect METRIC VALUE [OPTIONS]
```

**Options:**
- `--real-time / --no-real-time` - Enable real-time detection (default: False)

**Example:**
```bash
netsec-core anomaly detect packets_per_second 1000
```

#### Get Status

```bash
netsec-core anomaly status
```

### Asset Discovery Commands

#### Discover Assets

```bash
netsec-core assets discover NETWORK [OPTIONS]
```

**Options:**
- `-p, --ports TEXT` - Ports to scan (comma-separated)

**Example:**
```bash
netsec-core assets discover 192.168.1.0/24
netsec-core assets discover 10.0.0.1-10.0.0.10 --ports 22,80,443
```

### Remediation Commands

#### Get Remediation

```bash
netsec-core remediation get FINDING_TYPE [OPTIONS]
```

**Options:**
- `--api-url TEXT` - API base URL (default: http://localhost:8000)

**Example:**
```bash
netsec-core remediation get weak_cipher
netsec-core remediation get certificate_expired
netsec-core remediation get dns_tunneling
```

#### List Remediations

```bash
netsec-core remediation list [OPTIONS]
```

**Options:**
- `--api-url TEXT` - API base URL (default: http://localhost:8000)

**Example:**
```bash
netsec-core remediation list
```

#### Search Remediations

```bash
netsec-core remediation search KEYWORD [OPTIONS]
```

**Options:**
- `--api-url TEXT` - API base URL (default: http://localhost:8000)

**Example:**
```bash
netsec-core remediation search dns
netsec-core remediation search certificate
```

## API Endpoints

### Base URL

Default: `http://localhost:8000`

### Health

- `GET /api/v1/health` - Health check

### DNS Security

- `POST /api/v1/dns/scan` - Scan DNS security
- `GET /api/v1/dns/monitor` - Monitor DNS queries
- `POST /api/v1/dns/detect-tunneling` - Detect DNS tunneling
- `GET /api/v1/dns/anomalies?domain=example.com` - Get DNS anomalies

### SSL/TLS

- `POST /api/v1/ssl/check-certificate` - Check certificate
- `GET /api/v1/ssl/certificates` - List certificates
- `POST /api/v1/ssl/detect-weak-ciphers` - Detect weak ciphers
- `GET /api/v1/ssl/expiring-soon?hostname=example.com&port=443` - Get expiring certificates

### Network Scanner

- `POST /api/v1/scan/ports` - Scan ports
- `POST /api/v1/scan/services` - Scan services
- `GET /api/v1/scan/results/{scan_id}` - Get scan results

### Traffic Analysis

- `POST /api/v1/traffic/capture` - Capture traffic
- `POST /api/v1/traffic/analyze` - Analyze traffic
- `GET /api/v1/traffic/flows` - Get network flows

### Anomaly Detection

- `POST /api/v1/anomaly/learn-baseline` - Learn baseline
- `POST /api/v1/anomaly/detect` - Detect anomalies
- `GET /api/v1/anomaly/status` - Get status

### Asset Discovery

- `POST /api/v1/assets/discover` - Discover assets
- `POST /api/v1/assets/inventory` - Generate inventory

### LLM Analysis

- `POST /api/v1/llm/analyze-traffic` - Analyze traffic
- `POST /api/v1/llm/reduce-false-positives` - Reduce false positives
- `POST /api/v1/llm/generate-remediation` - Generate remediation
- `POST /api/v1/llm/explain-finding` - Explain finding

### Remediation

- `GET /api/v1/remediation/{finding_type}` - Get remediation
- `POST /api/v1/remediation/` - Get remediation for finding
- `GET /api/v1/remediation/` - List all remediations
- `GET /api/v1/remediation/search/{keyword}` - Search remediations

## Examples

### Complete Security Scan

```bash
# 1. Check API health
netsec-core health

# 2. Scan DNS security
netsec-core dns scan example.com

# 3. Check SSL certificate
netsec-core ssl check example.com

# 4. Scan ports
netsec-core scan ports example.com --ports 22,80,443,8080

# 5. Get remediation for findings
netsec-core remediation get weak_cipher
```

### Using API

```bash
# Health check
curl http://localhost:8000/api/v1/health

# DNS scan
curl -X POST "http://localhost:8000/api/v1/dns/scan" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com", "check_tunneling": true}'

# SSL check
curl -X POST "http://localhost:8000/api/v1/ssl/check-certificate" \
  -H "Content-Type: application/json" \
  -d '{"hostname": "example.com", "port": 443}'
```

## Troubleshooting

### Command Not Found

```bash
# Make sure package is installed
pip install -e .

# Check installation
which netsec-core  # Linux/Mac
where netsec-core  # Windows
```

### API Not Running

```bash
# Start API server
python run_api.py
# or
uvicorn netsec_core.api.main:app --reload
```

### Permission Errors

```bash
# Traffic capture may need elevated permissions
sudo netsec-core traffic capture  # Linux/Mac
```

### Network Errors

- Check network connectivity
- Verify DNS resolution
- Check firewall settings
- Verify target is reachable

### LLM Not Working

- Check API keys are set: `export OPENAI_API_KEY=your-key`
- Verify network connectivity
- Check API quotas

## Getting More Help

- Check [README.md](README.md) for overview
- Check [TESTING_GUIDE.md](TESTING_GUIDE.md) for testing
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment
- Open an issue on GitHub
- Check API docs at `/api/docs`
