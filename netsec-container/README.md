# NetSec-Container 🐳

**Lightweight, Fast Container Security Scanner with LLM-Powered Remediation**

A comprehensive container security scanner that integrates seamlessly into CI/CD pipelines, scans container images for vulnerabilities and secrets, and provides intelligent remediation guidance powered by LLMs.

## Features

### 🔍 Core Scanning Capabilities
- **Vulnerability Scanning** - Fast CVE scanning using multiple databases
- **Secrets Detection** - 20+ secret types (API keys, passwords, tokens, etc.)
- **SBOM Generation** - Software Bill of Materials for supply chain security
- **Dockerfile Analysis** - Security best practices checking
- **Kubernetes Manifest Scanning** - K8s security configuration analysis
- **Base Image Analysis** - Identify outdated or vulnerable base images

### 🤖 LLM-Powered Features
- **Intelligent Remediation** - Context-aware fix suggestions
- **Code Analysis** - Security vulnerability detection in code
- **False Positive Reduction** - Smart filtering of false alarms
- **Natural Language Explanations** - Clear, actionable guidance

### 📊 Reporting & Scoring
- **Risk Scoring System** - CVSS-based with exploitability scoring
- **PDF Reports** - Beautiful, comprehensive security reports
- **CSV Export** - Machine-readable vulnerability data
- **CI/CD Integration** - GitHub Actions, GitLab CI, Jenkins, CircleCI

### 🚀 Performance
- **Lightweight** - Minimal resource footprint (< 100MB memory)
- **Fast** - Optimized for CI/CD speed (< 30 seconds for most images)
- **Parallel Scanning** - Multi-threaded vulnerability detection

### 🌐 Web Interface
- **Drag-and-Drop** - Easy image upload and scanning
- **Real-time Results** - Live scanning progress
- **Report Download** - Instant PDF/CSV generation

## Quick Start

### Installation

```bash
pip install netsec-container
```

### CLI Usage

```bash
# Scan a container image
netsec-container scan docker.io/library/nginx:latest

# Scan with LLM remediation
netsec-container scan --llm docker.io/library/nginx:latest

# Generate PDF report
netsec-container scan --format pdf docker.io/library/nginx:latest

# Scan local image file
netsec-container scan --image-file nginx.tar

# CI/CD mode (exit code on vulnerabilities)
netsec-container scan --fail-on high docker.io/library/nginx:latest
```

### Python API

```python
from netsec_container import ContainerScanner

scanner = ContainerScanner()

# Scan image
results = scanner.scan_image("docker.io/library/nginx:latest")

# Get vulnerabilities
vulnerabilities = results.get_vulnerabilities()

# Get secrets
secrets = results.get_secrets()

# Get risk score
risk_score = results.get_risk_score()

# Generate report
scanner.generate_report(results, format="pdf", output="report.pdf")
```

### Web Interface

```bash
# Start web server
netsec-container serve --host 0.0.0.0 --port 8080

# Access at http://localhost:8080
```

### CI/CD Integration

#### GitHub Actions

```yaml
name: Container Security Scan

on: [push, pull_request]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Scan container image
        uses: netsec-container/action@v1
        with:
          image: ${{ env.IMAGE }}
          fail-on: high
          format: pdf
          output: security-report.pdf
```

#### GitLab CI

```yaml
container-security:
  image: netsec-container:latest
  script:
    - netsec-container scan --fail-on high $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  artifacts:
    paths:
      - security-report.pdf
```

## Architecture

```
netsec-container/
├── core/
│   ├── scanner.py          # Main scanner engine
│   ├── vulnerability.py    # CVE database and scanning
│   ├── secrets.py          # Secrets detection
│   └── scoring.py          # Risk scoring system
├── llm/
│   ├── analyzer.py         # LLM-powered analysis
│   ├── remediation.py     # Remediation generation
│   └── prompts.py         # Prompt templates
├── api/
│   ├── main.py             # FastAPI application
│   └── routes/             # API endpoints
├── web/
│   ├── app.py              # Web interface
│   └── static/             # Frontend assets
├── reports/
│   ├── pdf.py              # PDF report generator
│   └── csv.py              # CSV export
└── cicd/
    ├── github/             # GitHub Actions
    ├── gitlab/             # GitLab CI
    └── jenkins/            # Jenkins pipeline
```

## Security Coverage

### Vulnerability Scanning
- **CVE Database** - NVD, GitHub Advisory, OSV
- **Package Managers** - npm, pip, maven, go, etc.
- **OS Packages** - Debian, Ubuntu, Alpine, RHEL, etc.

### Secrets Detection
- API Keys (AWS, Azure, GCP, etc.)
- Passwords and tokens
- Private keys (SSH, RSA, etc.)
- Database credentials
- OAuth tokens
- And 15+ more types

### Compliance
- CIS Docker Benchmark
- CIS Kubernetes Benchmark
- OWASP Container Security
- NIST SP 800-190

## Configuration

```yaml
# .netsec-container.yml
scanner:
  vulnerability:
    enabled: true
    databases:
      - nvd
      - github
      - osv
  secrets:
    enabled: true
    patterns:
      - aws_key
      - api_key
      - password
  llm:
    enabled: true
    provider: openai  # or anthropic, local
    model: gpt-4
  reporting:
    formats:
      - pdf
      - csv
    scoring:
      enabled: true
      weights:
        critical: 10
        high: 7
        medium: 4
        low: 1
```

## License

MIT License

## Contributing

Contributions welcome! Please see CONTRIBUTING.md for guidelines.
