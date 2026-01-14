# Repository Setup Guide
## Step-by-Step Guide to Create Individual Repositories

This guide walks through setting up each project repository.

---

## Prerequisites

- GitHub account
- Git installed
- Python 3.10+ installed
- Basic knowledge of Git/GitHub

---

## Step 1: Create GitHub Repositories

### Option A: Via GitHub Web Interface

1. Go to GitHub.com
2. Click "New repository"
3. Create three repositories:
   - `netsec-core`
   - `netsec-cloud`
   - `netsec-container`

### Option B: Via GitHub CLI

```bash
# Install GitHub CLI if not installed
# gh auth login

# Create repositories
gh repo create netsec-core --public --description "Network Security Foundation Toolkit"
gh repo create netsec-cloud --public --description "Cloud Security, Compliance, Governance & Risk Toolkit"
gh repo create netsec-container --public --description "Container & Kubernetes Security Toolkit"
```

---

## Step 2: Clone and Initialize NetSec-Core

```bash
# Clone repository
git clone https://github.com/your-org/netsec-core.git
cd netsec-core

# Initialize project structure
mkdir -p src/netsec_core/{api,core,llm,remediation,cli}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p docs/{api,guides,examples}
mkdir -p examples
mkdir -p .github/workflows

# Create initial files (see templates below)
```

---

## Step 3: Project Structure Templates

### NetSec-Core Structure

```
netsec-core/
├── README.md
├── LICENSE
├── requirements.txt
├── setup.py
├── pyproject.toml
├── .gitignore
├── .github/
│   └── workflows/
│       ├── test.yml
│       ├── lint.yml
│       └── release.yml
├── src/
│   └── netsec_core/
│       ├── __init__.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── models.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── scanner.py
│       │   ├── dns_security.py
│       │   ├── ssl_monitor.py
│       │   └── anomaly_detector.py
│       ├── llm/
│       │   ├── __init__.py
│       │   └── analyzer.py
│       ├── remediation/
│       │   ├── __init__.py
│       │   └── guide.py
│       └── cli/
│           ├── __init__.py
│           └── main.py
├── tests/
├── docs/
└── examples/
```

---

## Step 4: Initial File Templates

### README.md Template

```markdown
# NetSec-Core 🛡️

Network Security Foundation Toolkit - Lightweight, API-first network security scanning.

## Features

- Network scanning
- DNS security analysis
- SSL/TLS monitoring
- Traffic analysis
- Anomaly detection

## Quick Start

\`\`\`bash
pip install netsec-core
netsec-core scan --target example.com
\`\`\`

## Documentation

See [docs/](docs/) for detailed documentation.

## License

MIT License
```

### setup.py Template

```python
from setuptools import setup, find_packages

setup(
    name="netsec-core",
    version="0.1.0",
    description="Network Security Foundation Toolkit",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "scapy>=2.5.0",
        "dnspython>=2.4.0",
    ],
    extras_require={
        "llm": ["openai>=1.0.0", "anthropic>=0.7.0"],
        "dev": ["pytest>=7.4.0", "black>=23.0.0", "ruff>=0.1.0"],
    },
)
```

### .gitignore Template

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/

# Virtual Environment
venv/
env/
.venv

# IDE
.vscode/
.idea/
*.swp

# Testing
.pytest_cache/
.coverage
htmlcov/

# Logs
*.log

# Environment
.env
.env.local

# Project specific
*.pcap
scan_results/
```

---

## Step 5: Initialize Each Repository

### NetSec-Core Initialization Script

Create `scripts/init_core.sh`:

```bash
#!/bin/bash
# Initialize NetSec-Core repository

# Create directory structure
mkdir -p src/netsec_core/{api,core,llm,remediation,cli}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p docs/{api,guides,examples}
mkdir -p examples

# Create __init__.py files
find src tests -type d -exec touch {}/__init__.py \;

# Create basic files
touch src/netsec_core/__init__.py
touch src/netsec_core/core/scanner.py
touch src/netsec_core/core/dns_security.py
touch src/netsec_core/core/ssl_monitor.py
touch src/netsec_core/api/routes.py
touch src/netsec_core/cli/main.py

echo "NetSec-Core initialized!"
```

### NetSec-Container Initialization Script

Create `scripts/init_container.sh`:

```bash
#!/bin/bash
# Initialize NetSec-Container repository

mkdir -p src/netsec_container/{api,core,secrets,llm,remediation,cli}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p docs/{api,guides,examples}
mkdir -p examples

find src tests -type d -exec touch {}/__init__.py \;

touch src/netsec_container/core/image_scanner.py
touch src/netsec_container/core/secrets_scanner.py
touch src/netsec_container/core/k8s_scanner.py

echo "NetSec-Container initialized!"
```

### NetSec-Cloud Initialization Script

Create `scripts/init_cloud.sh`:

```bash
#!/bin/bash
# Initialize NetSec-Cloud repository

mkdir -p src/netsec_cloud/{api,core,compliance,governance,risk,llm,remediation,cli}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p docs/{api,guides,examples}
mkdir -p examples

find src tests -type d -exec touch {}/__init__.py \;

touch src/netsec_cloud/core/cspm.py
touch src/netsec_cloud/compliance/checker.py
touch src/netsec_cloud/governance/policy.py

echo "NetSec-Cloud initialized!"
```

---

## Step 6: GitHub Actions CI/CD

### Test Workflow (.github/workflows/test.yml)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    - name: Run tests
      run: pytest tests/ --cov=src --cov-report=xml
```

### Lint Workflow (.github/workflows/lint.yml)

```yaml
name: Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.11"
    - name: Install linting tools
      run: |
        pip install black ruff mypy
    - name: Run black
      run: black --check src tests
    - name: Run ruff
      run: ruff check src tests
    - name: Run mypy
      run: mypy src
```

---

## Step 7: Initial Commit

```bash
# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Project structure and setup"

# Push to GitHub
git push -u origin main
```

---

## Step 8: Create Project Documentation

### For Each Repository:

1. **README.md** - Overview and quick start
2. **CONTRIBUTING.md** - Contribution guidelines
3. **CHANGELOG.md** - Version history
4. **docs/API.md** - API documentation
5. **docs/GUIDE.md** - User guide

---

## Step 9: Set Up Development Environment

### For Each Project:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .  # Install in development mode

# Install development dependencies
pip install -r requirements-dev.txt
```

---

## Step 10: Create First Feature

### Example: NetSec-Core DNS Scanner

```python
# src/netsec_core/core/dns_security.py
"""DNS Security Scanner"""

class DNSSecurityScanner:
    def __init__(self):
        self.name = "DNS Security Scanner"
    
    def scan(self, target):
        """Scan target for DNS security issues"""
        # Implementation
        pass
    
    def detect_tunneling(self, queries):
        """Detect DNS tunneling attempts"""
        # Implementation
        pass
```

---

## Repository URLs

After setup, repositories will be:

- `https://github.com/your-org/netsec-core`
- `https://github.com/your-org/netsec-cloud`
- `https://github.com/your-org/netsec-container`

---

## Next Steps

1. ✅ Create GitHub repositories
2. ✅ Clone and initialize each repository
3. ✅ Set up project structure
4. ✅ Create initial files
5. ✅ Set up CI/CD
6. ✅ Create first feature
7. ✅ Start development!

---

## Ready to Create Repositories!

**Let's start with NetSec-Core!** 🚀
