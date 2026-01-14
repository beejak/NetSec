# NetSec-Core Architecture Diagrams

## System Overview

```
                    ┌─────────────────────────────┐
                    │     NetSec-Core System      │
                    └─────────────┬───────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
   ┌────▼────┐              ┌────▼────┐              ┌────▼────┐
   │   API   │              │   CLI   │              │  Web    │
   │  Layer  │              │  Layer  │              │  UI     │
   │(FastAPI)│              │ (Click) │              │(Future) │
   └────┬────┘              └────┬────┘              └────┬────┘
        │                         │                         │
        └─────────────────────────┼─────────────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │    Core Scanner Modules   │
                    ├───────────────────────────┤
                    │ • DNS Security Scanner    │
                    │ • SSL/TLS Monitor         │
                    │ • Network Scanner         │
                    │ • Traffic Analyzer        │
                    │ • Anomaly Detector        │
                    │ • Asset Discovery         │
                    └─────────────┬─────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
   ┌────▼────┐              ┌────▼────┐              ┌────▼────┐
   │   LLM   │              │Remediation│            │  Config │
   │Analyzer │              │  System  │            │ Manager │
   └─────────┘              └──────────┘            └─────────┘
```

## Request Flow

```
Client Request
      │
      ▼
┌─────────────┐
│  API Router │  (Route to appropriate handler)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Validation │  (Pydantic models)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Scanner    │  (Core logic execution)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Processing │  (Result formatting)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Response   │  (JSON/Error handling)
└─────────────┘
```

## Module Dependencies

```
netsec_core/
├── api/
│   ├── main.py ──────┐
│   ├── models.py      │
│   └── routes/        │
│       ├── dns.py ────┼──► core/dns_scanner.py
│       ├── ssl.py ────┼──► core/ssl_scanner.py
│       └── scan.py ───┼──► core/network_scanner.py
│
├── cli/
│   └── commands/ ──────┼──► Same core modules
│
├── core/
│   ├── dns_scanner.py ──► dnspython
│   ├── ssl_scanner.py ──► cryptography
│   ├── network_scanner.py ─► socket
│   └── traffic_analyzer.py ─► scapy
│
├── llm/
│   └── analyzer.py ────► openai/anthropic (optional)
│
└── remediation/
    └── guide.py ──────► (standalone)
```

## Data Flow: DNS Scan Example

```
User Request: "Scan example.com"
      │
      ▼
┌─────────────────┐
│  CLI/API Input  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  DNS Route      │  POST /api/v1/dns/scan
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  DNSScanner     │
│  .scan_domain() │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│Resolve │ │Detect  │
│Records │ │Tunneling│
└───┬────┘ └───┬────┘
    │          │
    └────┬─────┘
         │
         ▼
┌─────────────────┐
│  Findings       │
│  Aggregation    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Response       │
│  (JSON)         │
└─────────────────┘
```

## Security Architecture

```
┌─────────────────────────────────────┐
│      Security Layers                 │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Network Layer Security      │  │
│  │  • Firewall                  │  │
│  │  • DDoS Protection           │  │
│  │  • Rate Limiting            │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Application Layer Security  │  │
│  │  • Authentication            │  │
│  │  • Authorization             │  │
│  │  • Input Validation          │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Data Layer Security         │  │
│  │  • Encryption at Rest        │  │
│  │  • Encryption in Transit     │  │
│  │  • Secure Storage            │  │
│  └──────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

## CI/CD Integration Flow

```
Developer
    │
    │ git push
    ▼
┌─────────────┐
│  Git Repo   │
└──────┬──────┘
       │
       │ Webhook
       ▼
┌─────────────┐
│  CI/CD      │  (GitHub Actions/GitLab CI)
│  Pipeline   │
└──────┬──────┘
       │
       │ Trigger
       ▼
┌─────────────┐
│ NetSec-Core │
│  Security   │
│  Scan       │
└──────┬──────┘
       │
       │ Results
       ▼
┌─────────────┐
│  Report/    │
│  Alert      │
└─────────────┘
```

## Future: Cloud Security Architecture

```
┌─────────────────────────────────────────────┐
│         Cloud Security Scanner               │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   AWS    │  │  Azure   │  │   GCP    │  │
│  │  SDK     │  │  SDK     │  │  SDK     │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │             │             │        │
│       └─────────────┼─────────────┘        │
│                     │                      │
│            ┌────────▼────────┐             │
│            │  Cloud Scanner  │             │
│            │  Core Engine    │             │
│            └────────┬────────┘             │
│                     │                      │
│            ┌────────▼────────┐             │
│            │  Security Checks │             │
│            │  • S3 Buckets    │             │
│            │  • IAM Policies  │             │
│            │  • Security Groups│            │
│            │  • Compliance    │             │
│            └────────┬────────┘             │
│                     │                      │
│            ┌────────▼────────┐             │
│            │  Findings       │             │
│            │  Engine         │             │
│            └─────────────────┘             │
│                                             │
└─────────────────────────────────────────────┘
```
