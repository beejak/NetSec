# Secrets Scanning Design
## Comprehensive Secrets Detection for NetSec-Container

---

## Overview

**YES, we are incorporating secrets scanning** as a **PRIMARY FEATURE** in NetSec-Container. This document outlines the design and implementation approach.

---

## Why Secrets Scanning is Critical

### Statistics:
- **70%+ of breaches** involve exposed credentials
- **Millions of secrets** exposed in public repositories
- **Container images** often contain hardcoded secrets
- **Kubernetes secrets** frequently misconfigured

### Attack Vectors:
1. **Secrets in Container Images** → Image scanning
2. **Secrets in Kubernetes Resources** → K8s scanning
3. **Secrets in Git Repositories** → Git scanning
4. **Secrets in CI/CD Pipelines** → Pipeline scanning
5. **Secrets at Runtime** → Runtime detection

---

## Secrets Scanning Architecture

### Module: `netsec_container.secrets`

```
secrets/
├── __init__.py
├── scanner.py          # Main secrets scanner
├── detectors/          # Secret detection engines
│   ├── pattern.py      # Pattern-based detection
│   ├── entropy.py      # Entropy-based detection
│   ├── cloud.py        # Cloud provider secrets
│   ├── api_keys.py     # API key detection
│   └── generic.py      # Generic secret patterns
├── validators/         # Secret validation
│   ├── aws.py          # AWS key validation
│   ├── github.py       # GitHub token validation
│   └── generic.py      # Generic validation
└── reporters/          # Reporting
    ├── json.py         # JSON reporter
    ├── sarif.py        # SARIF reporter
    └── cli.py          # CLI reporter
```

---

## Secret Types Detected

### 1. Cloud Provider Secrets

#### AWS:
- Access Key IDs: `AKIA[0-9A-Z]{16}`
- Secret Access Keys: Pattern matching
- Session Tokens: `temporary credentials`
- IAM Keys: Various formats

#### Azure:
- Connection Strings: `DefaultEndpointsProtocol=...`
- Service Principals: `client_id`, `client_secret`
- Storage Account Keys: Base64 patterns
- AD Application Secrets

#### GCP:
- Service Account Keys: JSON format
- API Keys: `AIza[0-9A-Z_-]{35}`
- OAuth Credentials: JSON format

### 2. API Keys & Tokens

#### Common APIs:
- GitHub: `ghp_[0-9a-zA-Z]{36}`
- GitLab: `glpat-[0-9a-zA-Z_-]{20}`
- Slack: `xox[baprs]-[0-9a-zA-Z-]{10,48}`
- Stripe: `sk_live_[0-9a-zA-Z]{24,32}`
- PayPal: `access_token$production$`
- Twilio: `SK[0-9a-f]{32}`
- SendGrid: `SG\.[0-9a-zA-Z_-]{22}\.[0-9a-zA-Z_-]{43}`
- Mailgun: `key-[0-9a-f]{32}`

### 3. Database Credentials

- MySQL: `mysql://user:pass@host`
- PostgreSQL: `postgresql://user:pass@host`
- MongoDB: `mongodb://user:pass@host`
- Redis: `redis://:password@host`
- Elasticsearch: `http://user:pass@host`

### 4. Authentication Tokens

- JWT: `eyJ[a-zA-Z0-9_-]{5,}\.eyJ[a-zA-Z0-9_-]{5,}\.[a-zA-Z0-9_-]{5,}`
- OAuth: Various formats
- Session Tokens: Pattern matching
- Bearer Tokens: `Bearer [a-zA-Z0-9_-]+`

### 5. Private Keys

- SSH: `-----BEGIN [EDDSA|RSA|DSA|EC] PRIVATE KEY-----`
- SSL/TLS: `-----BEGIN PRIVATE KEY-----`
- GPG: `-----BEGIN PGP PRIVATE KEY BLOCK-----`
- PGP: Various formats

### 6. Container Registry Credentials

- Docker Hub: Various formats
- AWS ECR: AWS credentials
- Azure ACR: Azure credentials
- GCP GCR: GCP credentials
- Harbor: Various formats

### 7. Kubernetes Secrets

- Base64 encoded secrets in YAML
- Secrets in ConfigMaps (wrong practice)
- Secrets in environment variables
- Secrets in pod specifications

### 8. Generic Secrets

- Passwords: Common patterns
- API Keys: Generic patterns
- Connection Strings: Various formats
- Credentials: Pattern matching

---

## Detection Methods

### 1. Pattern-Based Detection

**Approach**: Regex patterns for known secret formats

**Advantages**:
- Fast
- Accurate for known formats
- Low false positives

**Examples**:
```python
AWS_ACCESS_KEY_PATTERN = r'AKIA[0-9A-Z]{16}'
GITHUB_TOKEN_PATTERN = r'ghp_[0-9a-zA-Z]{36}'
```

### 2. Entropy-Based Detection

**Approach**: High entropy indicates randomness (likely secrets)

**Advantages**:
- Catches unknown formats
- Finds generic secrets
- Good for passwords

**Implementation**:
- Shannon entropy calculation
- Threshold-based detection
- Context-aware filtering

### 3. Context-Based Detection

**Approach**: Look for secret indicators in context

**Examples**:
- Variable names: `password`, `secret`, `key`, `token`
- File names: `.env`, `secrets.yaml`, `config.json`
- Comments: `# TODO: remove secret`

### 4. Validation-Based Detection

**Approach**: Validate detected secrets against APIs

**Examples**:
- AWS: Validate access key format
- GitHub: Validate token format
- Generic: Check entropy and format

**Note**: Only validate format, NOT actual secrets (security)

---

## Scanning Targets

### 1. Container Images

**What to Scan**:
- Dockerfile
- Layer contents
- Environment variables
- Configuration files
- Application code
- Build artifacts

**How**:
- Extract image layers
- Scan each layer
- Check environment variables
- Parse configuration files
- Scan application code

### 2. Kubernetes Resources

**What to Scan**:
- Pod specifications
- Deployment YAMLs
- ConfigMaps
- Secrets (if accessible)
- Helm charts
- Kustomize files

**How**:
- Parse YAML files
- Check environment variables
- Decode base64 secrets
- Scan ConfigMaps
- Check mounted secrets

### 3. Git Repositories

**What to Scan**:
- All files in repository
- Git history (optional)
- Configuration files
- Environment files
- Application code

**How**:
- Clone repository
- Scan all files
- Optionally scan git history
- Check .gitignore patterns
- Scan CI/CD configs

### 4. CI/CD Pipelines

**What to Scan**:
- GitHub Actions workflows
- GitLab CI configs
- Jenkinsfiles
- CircleCI configs
- Azure DevOps pipelines

**How**:
- Parse pipeline configs
- Check environment variables
- Scan secret references
- Check secret management

### 5. Runtime Detection

**What to Detect**:
- Secrets in environment variables
- Secrets in mounted volumes
- Secrets in process memory (advanced)

**How**:
- Monitor container environment
- Check mounted volumes
- Scan process environment
- Detect secret usage

---

## API Design

### REST API Endpoints

```python
# Scan container image
POST /api/v1/container/secrets/scan/image
{
    "image": "nginx:latest",
    "registry": "docker.io"
}

# Scan Kubernetes resources
POST /api/v1/container/secrets/scan/kubernetes
{
    "namespace": "default",
    "resources": ["pods", "configmaps", "secrets"]
}

# Scan Git repository
POST /api/v1/container/secrets/scan/git
{
    "repository": "https://github.com/user/repo",
    "branch": "main",
    "scan_history": false
}

# Scan CI/CD pipeline
POST /api/v1/container/secrets/scan/cicd
{
    "pipeline_file": ".github/workflows/deploy.yml"
}
```

### Response Format

```json
{
    "scan_id": "uuid",
    "status": "completed",
    "secrets_found": 5,
    "secrets": [
        {
            "type": "aws_access_key",
            "severity": "critical",
            "location": {
                "file": "Dockerfile",
                "line": 42,
                "column": 10
            },
            "secret": "AKIAIOSFODNN7EXAMPLE",
            "masked": "AKIA****************",
            "context": "ENV AWS_ACCESS_KEY_ID=...",
            "recommendation": "Use AWS Secrets Manager"
        }
    ],
    "scan_time": "2024-01-01T12:00:00Z",
    "duration_ms": 1234
}
```

---

## Integration with Other Modules

### NetSec-Container Integration:

1. **Image Scanner** → Secrets scanning
2. **Kubernetes Scanner** → Secrets scanning
3. **Compliance Checker** → Secrets policy violations
4. **Risk Assessor** → Secrets exposure risk

### CI/CD Integration:

```yaml
# GitHub Actions Example
- name: Scan for Secrets
  uses: netsec-container/secrets-scan@v1
  with:
    scan-type: 'all'
    fail-on-secrets: true
```

---

## Performance Considerations

### Optimization Strategies:

1. **Parallel Scanning**: Scan multiple files/layers in parallel
2. **Caching**: Cache scan results
3. **Incremental Scanning**: Only scan changed files
4. **Pattern Compilation**: Pre-compile regex patterns
5. **Early Exit**: Stop on first critical secret (optional)

### Performance Targets:

- **Image Scan**: < 30 seconds for typical image
- **K8s Scan**: < 5 seconds per namespace
- **Git Scan**: < 60 seconds for medium repo
- **CI/CD Scan**: < 10 seconds per pipeline

---

## Security Considerations

### What We Do:
- ✅ Mask secrets in output
- ✅ Validate formats only (not actual secrets)
- ✅ Secure storage of scan results
- ✅ Audit logging

### What We DON'T Do:
- ❌ Validate secrets against APIs (security risk)
- ❌ Store actual secrets
- ❌ Transmit secrets over network
- ❌ Expose secrets in logs

---

## False Positive Reduction

### Strategies:

1. **Whitelisting**: Known false positives
2. **Context Analysis**: Check surrounding code
3. **Format Validation**: Validate secret formats
4. **Entropy Thresholds**: Tune entropy detection
5. **Machine Learning**: Optional ML-based filtering

---

## Reporting & Alerts

### Report Formats:

1. **JSON**: Machine-readable
2. **SARIF**: Security tool integration
3. **CLI**: Human-readable
4. **HTML**: Web dashboard
5. **CSV**: Spreadsheet import

### Alert Channels:

1. **Email**: Critical secrets
2. **Webhook**: Integration with other tools
3. **Slack**: Team notifications
4. **GitHub Issues**: Auto-create issues
5. **API**: Programmatic access

---

## Implementation Priority

### Phase 1 (MVP):
1. ✅ Pattern-based detection
2. ✅ Cloud provider secrets
3. ✅ API keys detection
4. ✅ Container image scanning
5. ✅ Basic reporting

### Phase 2:
1. ✅ Entropy-based detection
2. ✅ Kubernetes secrets scanning
3. ✅ Git repository scanning
4. ✅ CI/CD integration
5. ✅ Advanced reporting

### Phase 3:
1. ✅ Runtime detection
2. ✅ Machine learning (optional)
3. ✅ Advanced validation
4. ✅ Dashboard
5. ✅ Advanced analytics

---

## Tools to Reference

### Open-Source Tools:
- **TruffleHog**: Pattern + entropy detection
- **git-secrets**: Git secrets prevention
- **detect-secrets**: Yelp's detection tool
- **Gitleaks**: Fast Git secrets scanner
- **Secretlint**: Secrets linting

### What We'll Build:
- Unified secrets scanner
- Container-focused
- Kubernetes-integrated
- API-first design
- Lightweight and fast

---

## Success Criteria

1. ✅ Detect 20+ secret types
2. ✅ < 5% false positive rate
3. ✅ < 30 seconds per image scan
4. ✅ API-first design
5. ✅ CI/CD integration
6. ✅ Comprehensive reporting

---

## Conclusion

**Secrets scanning is a PRIMARY FEATURE** of NetSec-Container and will be implemented from the start. It's critical for container security and addresses a major attack vector.

**Ready to implement!** 🔐
