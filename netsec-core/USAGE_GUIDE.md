# NetSec-Core Usage Guide

Complete syntax reference and usage examples for NetSec-Core.

## Table of Contents

- [Quick Reference](#quick-reference)
- [Command Syntax](#command-syntax)
- [What NetSec-Core Does](#what-netsec-core-does)
- [What NetSec-Core Does NOT Do](#what-netsec-core-does-not-do)
- [Common Use Cases](#common-use-cases)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

## Quick Reference

### CLI Commands

```bash
# Health Check
netsec-core health [--api-url URL]

# DNS Security
netsec-core dns scan DOMAIN [OPTIONS]
netsec-core dns monitor [--duration SECONDS]

# SSL/TLS
netsec-core ssl check HOSTNAME [OPTIONS]
netsec-core ssl list

# Network Scanning
netsec-core scan ports TARGET [--ports PORTS] [OPTIONS]
netsec-core scan services TARGET [--ports PORTS]

# Traffic Analysis
netsec-core traffic capture [OPTIONS]
netsec-core traffic analyze [--pcap-file FILE]

# Anomaly Detection
netsec-core anomaly learn [--duration SECONDS]
netsec-core anomaly detect METRIC VALUE
netsec-core anomaly status

# Asset Discovery
netsec-core assets discover NETWORK [--ports PORTS]

# Remediation
netsec-core remediation get FINDING_TYPE
netsec-core remediation list
netsec-core remediation search KEYWORD
```

### API Endpoints

```bash
# Health
GET /api/v1/health

# DNS
POST /api/v1/dns/scan
GET /api/v1/dns/monitor
POST /api/v1/dns/detect-tunneling
GET /api/v1/dns/anomalies?domain=DOMAIN

# SSL/TLS
POST /api/v1/ssl/check-certificate
GET /api/v1/ssl/certificates
POST /api/v1/ssl/detect-weak-ciphers
GET /api/v1/ssl/expiring-soon?hostname=HOST&port=PORT

# Network Scanner
POST /api/v1/scan/ports
POST /api/v1/scan/services
GET /api/v1/scan/results/{scan_id}

# Traffic
POST /api/v1/traffic/capture
POST /api/v1/traffic/analyze
GET /api/v1/traffic/flows

# Anomaly
POST /api/v1/anomaly/learn-baseline
POST /api/v1/anomaly/detect
GET /api/v1/anomaly/status

# Assets
POST /api/v1/assets/discover
POST /api/v1/assets/inventory

# LLM
POST /api/v1/llm/analyze-traffic
POST /api/v1/llm/reduce-false-positives
POST /api/v1/llm/generate-remediation
POST /api/v1/llm/explain-finding

# Remediation
GET /api/v1/remediation/{finding_type}
POST /api/v1/remediation/
GET /api/v1/remediation/
GET /api/v1/remediation/search/{keyword}
```

## Command Syntax

### DNS Scan

```bash
# Basic scan
netsec-core dns scan example.com

# With options
netsec-core dns scan example.com \
  --check-tunneling \
  --check-spoofing \
  --analyze-patterns

# Disable specific checks
netsec-core dns scan example.com \
  --no-check-tunneling \
  --no-check-spoofing
```

**API:**
```json
POST /api/v1/dns/scan
{
  "domain": "example.com",
  "check_tunneling": true,
  "check_spoofing": true,
  "analyze_patterns": true
}
```

### SSL Check

```bash
# Basic check
netsec-core ssl check example.com

# Custom port
netsec-core ssl check example.com --port 8443

# Disable specific checks
netsec-core ssl check example.com \
  --no-check-ciphers \
  --no-check-chain
```

**API:**
```json
POST /api/v1/ssl/check-certificate
{
  "hostname": "example.com",
  "port": 443,
  "check_expiration": true,
  "check_ciphers": true,
  "check_chain": true
}
```

### Port Scanning

```bash
# Scan common ports
netsec-core scan ports 127.0.0.1

# Specific ports
netsec-core scan ports 192.168.1.1 --ports 22,80,443,8080

# With options
netsec-core scan ports example.com \
  --ports 80,443 \
  --scan-type tcp \
  --timeout 3.0
```

**API:**
```json
POST /api/v1/scan/ports
{
  "target": "127.0.0.1",
  "ports": [22, 80, 443],
  "scan_type": "tcp",
  "timeout": 5.0
}
```

### Traffic Capture

```bash
# Basic capture
netsec-core traffic capture

# With interface
netsec-core traffic capture --interface eth0

# With filter
netsec-core traffic capture \
  --interface eth0 \
  --filter "tcp port 80" \
  --count 100 \
  --timeout 60
```

### Remediation

```bash
# Get remediation
netsec-core remediation get weak_cipher
netsec-core remediation get certificate_expired
netsec-core remediation get dns_tunneling

# List all
netsec-core remediation list

# Search
netsec-core remediation search dns
netsec-core remediation search certificate
```

## What NetSec-Core Does

### ✅ Core Capabilities

1. **Network Security Scanning**
   - Port scanning (TCP/UDP)
   - Service detection
   - Banner grabbing
   - Network asset discovery

2. **DNS Security Analysis**
   - DNS record resolution
   - DNS tunneling detection
   - DNS spoofing detection
   - Query pattern analysis
   - Malicious domain indicators

3. **SSL/TLS Monitoring**
   - Certificate validation
   - Expiration tracking
   - Weak cipher detection
   - TLS version checking
   - Certificate chain validation

4. **Traffic Analysis**
   - Packet capture
   - Protocol analysis
   - Flow tracking
   - Traffic statistics

5. **Anomaly Detection**
   - Baseline learning
   - Statistical anomaly detection
   - Pattern-based detection
   - Real-time monitoring

6. **Remediation Guidance**
   - Security finding remediation
   - Step-by-step guidance
   - Immediate/short-term/long-term actions

7. **LLM-Powered Analysis**
   - Traffic analysis
   - False positive reduction
   - Remediation generation
   - Natural language explanations

## What NetSec-Core Does NOT Do

### ❌ Limitations and Exclusions

1. **Not a Full-Featured IDS/IPS**
   - Does NOT block or prevent attacks
   - Does NOT replace dedicated IDS/IPS systems
   - Does NOT provide real-time intrusion prevention
   - Does NOT have signature-based detection

2. **Not a Vulnerability Scanner**
   - Does NOT perform deep vulnerability scanning
   - Does NOT exploit vulnerabilities
   - Does NOT provide CVE database lookups
   - Does NOT perform authenticated scans

3. **Not a Firewall**
   - Does NOT manage firewall rules
   - Does NOT block network traffic
   - Does NOT provide network segmentation
   - Does NOT enforce network policies

4. **Not a SIEM**
   - Does NOT aggregate logs from multiple sources
   - Does NOT provide long-term log storage
   - Does NOT correlate events across systems
   - Does NOT provide compliance reporting

5. **Not a Cloud Security Platform (Separate Module)**
   - Cloud security is in NetSec-Cloud (separate module)
   - NetSec-Core focuses on network security
   - See [NetSec-Cloud](../netsec-cloud/) for cloud scanning

6. **Not a Web Application Scanner**
   - Does NOT perform web application security testing
   - Does NOT test for OWASP Top 10 vulnerabilities
   - Does NOT perform SQL injection testing
   - Does NOT test for XSS vulnerabilities

7. **Not a Malware Scanner**
   - Does NOT detect malware
   - Does NOT perform antivirus scanning
   - Does NOT analyze file contents
   - Does NOT provide malware removal

8. **Not a Network Performance Monitor**
   - Does NOT measure network performance metrics
   - Does NOT provide bandwidth monitoring
   - Does NOT track network utilization
   - Does NOT provide QoS management

9. **Not a Configuration Management Tool**
   - Does NOT manage device configurations
   - Does NOT enforce configuration standards
   - Does NOT provide configuration backups
   - Does NOT track configuration changes

10. **Not a Compliance Automation Platform**
    - Does NOT provide automated compliance checks
    - Does NOT generate compliance reports
    - Does NOT track compliance over time
    - Does NOT provide compliance dashboards

### ⚠️ Important Notes

- **Network Access Required**: Most features require network connectivity
- **Permissions**: Traffic capture may require elevated permissions
- **LLM Features**: Require API keys (OpenAI/Anthropic) for full functionality
- **No Persistent Storage**: Results are not stored by default (future feature)
- **No Authentication**: API does not include authentication (add in production)
- **No Rate Limiting**: API does not include rate limiting (add in production)

## Common Use Cases

### Use Case 1: Security Assessment

```bash
# 1. Check API health
netsec-core health

# 2. Scan DNS security
netsec-core dns scan example.com

# 3. Check SSL certificates
netsec-core ssl check example.com

# 4. Scan network ports
netsec-core scan ports 192.168.1.0/24 --ports 22,80,443

# 5. Get remediation for findings
netsec-core remediation get weak_cipher
```

### Use Case 2: Continuous Monitoring

```bash
# Monitor DNS queries
netsec-core dns monitor --duration 3600

# Learn anomaly baseline
netsec-core anomaly learn --duration 7200

# Detect anomalies
netsec-core anomaly detect packets_per_second 1000
```

### Use Case 3: Incident Response

```bash
# Capture traffic during incident
netsec-core traffic capture --interface eth0 --filter "host 192.168.1.100"

# Analyze captured traffic
netsec-core traffic analyze --pcap-file incident.pcap

# Discover affected assets
netsec-core assets discover 192.168.1.0/24
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install NetSec-Core
        run: |
          pip install netsec-core
      
      - name: Scan DNS Security
        run: |
          netsec-core dns scan ${{ secrets.TARGET_DOMAIN }}
      
      - name: Check SSL Certificates
        run: |
          netsec-core ssl check ${{ secrets.TARGET_HOSTNAME }}
      
      - name: Scan Ports
        run: |
          netsec-core scan ports ${{ secrets.TARGET_IP }} --ports 22,80,443
      
      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: security-scan-results
          path: logs/
```

### GitLab CI

```yaml
security_scan:
  stage: test
  image: python:3.11
  before_script:
    - pip install netsec-core
  script:
    - netsec-core dns scan $TARGET_DOMAIN
    - netsec-core ssl check $TARGET_HOSTNAME
    - netsec-core scan ports $TARGET_IP
  artifacts:
    paths:
      - logs/
    expire_in: 1 week
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    stages {
        stage('Security Scan') {
            steps {
                sh '''
                    pip install netsec-core
                    netsec-core dns scan ${TARGET_DOMAIN}
                    netsec-core ssl check ${TARGET_HOSTNAME}
                    netsec-core scan ports ${TARGET_IP}
                '''
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'logs/**/*', fingerprint: true
        }
    }
}
```

### Docker in CI/CD

```yaml
# .github/workflows/security-scan.yml
- name: Run Security Scan
  run: |
    docker run --rm \
      -v $(pwd):/workspace \
      -w /workspace \
      netsec-core:latest \
      netsec-core dns scan example.com
```

### API Integration in CI/CD

```bash
#!/bin/bash
# ci-security-scan.sh

API_URL="http://localhost:8000"

# Start API server in background
docker-compose up -d

# Wait for API
sleep 5

# Run scans via API
curl -X POST "$API_URL/api/v1/dns/scan" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}' \
  > dns-scan-results.json

curl -X POST "$API_URL/api/v1/ssl/check-certificate" \
  -H "Content-Type: application/json" \
  -d '{"hostname": "example.com", "port": 443}' \
  > ssl-check-results.json

# Check for critical findings
if grep -q '"severity": "critical"' *.json; then
  echo "Critical security findings detected!"
  exit 1
fi
```

## Troubleshooting

### Command Not Found

```bash
# Verify installation
pip show netsec-core

# Reinstall if needed
pip install -e .
```

### API Not Responding

```bash
# Check if API is running
curl http://localhost:8000/api/v1/health

# Start API if not running
python run_api.py
```

### Permission Errors

```bash
# Traffic capture may need sudo
sudo netsec-core traffic capture

# Or set capabilities (Linux)
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)
```

### Network Errors

- Check network connectivity
- Verify DNS resolution
- Check firewall rules
- Verify target is reachable

## Getting Help

- 📖 [Complete Help Guide](HELP.md)
- 🚀 [Quick Start](QUICKSTART.md)
- 🧪 [Testing Guide](TESTING_GUIDE.md)
- 📝 [API Documentation](http://localhost:8000/api/docs)
