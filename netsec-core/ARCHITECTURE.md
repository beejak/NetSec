# NetSec-Core Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        NetSec-Core System                        │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼────┐          ┌────▼────┐          ┌────▼────┐
   │   API   │          │   CLI   │          │  Core   │
   │  Layer  │          │  Layer  │          │ Modules │
   └────┬────┘          └────┬────┘          └────┬────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Scanner Modules   │
                    ├────────────────────┤
                    │ • DNS Scanner      │
                    │ • SSL Scanner      │
                    │ • Network Scanner  │
                    │ • Traffic Analyzer │
                    │ • Anomaly Detector │
                    │ • Asset Discovery  │
                    └─────────┬─────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼────┐          ┌────▼────┐          ┌────▼────┐
   │   LLM   │          │Remediation│         │  Config │
   │Analyzer │          │  System  │         │ Manager │
   └─────────┘          └──────────┘         └─────────┘
```

## Component Architecture

### API Layer (FastAPI)

```
┌─────────────────────────────────────────────┐
│              FastAPI Application             │
├─────────────────────────────────────────────┤
│  • CORS Middleware                           │
│  • Error Handling                            │
│  • Request Validation                        │
│  • Response Formatting                       │
└──────────────┬──────────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐ ┌───▼───┐ ┌───▼───┐
│Routes │ │Models │ │Utils  │
└───┬───┘ └───┬───┘ └───┬───┘
    │          │          │
    └──────────┼──────────┘
               │
    ┌──────────▼──────────┐
    │   Core Scanners      │
    └─────────────────────┘
```

### Core Scanner Modules

```
┌─────────────────────────────────────────────────┐
│            Core Scanner Architecture             │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐    ┌──────────────┐          │
│  │ DNS Scanner  │    │ SSL Scanner  │          │
│  │              │    │              │          │
│  │ • Resolution │    │ • Cert Check │          │
│  │ • Tunneling  │    │ • Expiration │          │
│  │ • Spoofing   │    │ • Weak Ciphers│         │
│  └──────────────┘    └──────────────┘          │
│                                                 │
│  ┌──────────────┐    ┌──────────────┐          │
│  │   Network    │    │   Traffic    │          │
│  │   Scanner    │    │   Analyzer   │          │
│  │              │    │              │          │
│  │ • Port Scan  │    │ • Capture    │          │
│  │ • Services   │    │ • Analysis   │          │
│  │ • Banners    │    │ • Flows      │          │
│  └──────────────┘    └──────────────┘          │
│                                                 │
│  ┌──────────────┐    ┌──────────────┐          │
│  │   Anomaly    │    │    Asset     │          │
│  │   Detector   │    │  Discovery   │          │
│  │              │    │              │          │
│  │ • Baseline   │    │ • Network    │          │
│  │ • Detection  │    │ • Services   │          │
│  │ • Patterns   │    │ • Inventory  │          │
│  └──────────────┘    └──────────────┘          │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Network Architecture

### Deployment Architecture

```
                    Internet
                       │
                       ▼
            ┌──────────────────────┐
            │   Load Balancer      │
            │   (Nginx/HAProxy)     │
            └──────────┬───────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
   │ API      │   │ API      │   │ API      │
   │ Instance │   │ Instance │   │ Instance │
   │ 1        │   │ 2        │   │ 3        │
   └────┬────┘   └────┬────┘   └────┬────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
            ┌──────────▼──────────┐
            │   Shared Services    │
            ├──────────────────────┤
            │ • Redis (Cache)     │
            │ • Database (Results)│
            │ • Message Queue     │
            └──────────────────────┘
```

### Data Flow Architecture

```
┌──────────┐
│  Client  │
│ (CLI/API)│
└────┬─────┘
     │
     │ Request
     ▼
┌─────────────────┐
│  API Gateway     │
│  (FastAPI)       │
└────┬────────────┘
     │
     │ Route to Handler
     ▼
┌─────────────────┐
│  Route Handler   │
│  (Validation)    │
└────┬────────────┘
     │
     │ Call Scanner
     ▼
┌─────────────────┐
│  Scanner Module  │
│  (Core Logic)    │
└────┬────────────┘
     │
     │ Process
     ▼
┌─────────────────┐
│  Result          │
│  Processing      │
└────┬────────────┘
     │
     │ Format Response
     ▼
┌─────────────────┐
│  Response       │
│  (JSON)         │
└─────────────────┘
```

## Security Architecture

### Security Layers

```
┌─────────────────────────────────────────┐
│         Security Architecture            │
├─────────────────────────────────────────┤
│                                         │
│  Layer 1: Network Security              │
│  • Firewall Rules                       │
│  • DDoS Protection                      │
│  • Rate Limiting                        │
│                                         │
│  Layer 2: Application Security          │
│  • Authentication                       │
│  • Authorization                        │
│  • Input Validation                     │
│  • Output Encoding                      │
│                                         │
│  Layer 3: Data Security                 │
│  • Encryption at Rest                   │
│  • Encryption in Transit                │
│  • Secure Credential Storage            │
│                                         │
│  Layer 4: Operational Security          │
│  • Audit Logging                        │
│  • Monitoring                           │
│  • Incident Response                    │
│                                         │
└─────────────────────────────────────────┘
```

## Integration Architecture

### CI/CD Integration

```
┌─────────────────┐
│  Git Repository  │
└────────┬────────┘
         │
         │ Push/PR
         ▼
┌─────────────────┐
│  GitHub Actions  │
│  / GitLab CI    │
└────────┬────────┘
         │
         │ Trigger
         ▼
┌─────────────────┐
│  NetSec-Core     │
│  Security Scan   │
└────────┬────────┘
         │
         │ Results
         ▼
┌─────────────────┐
│  Report/Alert    │
└─────────────────┘
```

### External Integrations

```
┌─────────────────────────────────────────┐
│      NetSec-Core Integration Hub        │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┐  ┌──────────┐             │
│  │   SIEM   │  │ Ticketing│             │
│  │ (Splunk) │  │ (Jira)   │             │
│  └──────────┘  └──────────┘             │
│                                         │
│  ┌──────────┐  ┌──────────┐             │
│  │  Threat  │  │  Cloud   │             │
│  │  Intel   │  │ Providers│             │
│  └──────────┘  └──────────┘             │
│                                         │
│  ┌──────────┐  ┌──────────┐             │
│  │  LLM     │  │  Webhooks│             │
│  │  APIs    │  │ (Slack)  │             │
│  └──────────┘  └──────────┘             │
│                                         │
└─────────────────────────────────────────┘
```

## Future: Cloud Security Architecture

### Cloud Scanner Architecture (Planned)

```
┌─────────────────────────────────────────┐
│      Cloud Security Scanner              │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │   AWS    │  │  Azure   │  │   GCP   ││
│  │ Provider │  │ Provider │  │Provider ││
│  └────┬─────┘  └────┬─────┘  └────┬───┘│
│       │             │             │     │
│       └─────────────┼─────────────┘     │
│                     │                   │
│            ┌────────▼────────┐          │
│            │  Unified Scanner │          │
│            │  (Common Checks) │          │
│            └────────┬────────┘          │
│                     │                   │
│            ┌────────▼────────┐          │
│            │  Findings Engine  │          │
│            └──────────────────┘          │
│                                         │
└─────────────────────────────────────────┘
```

## Technology Stack

### Current Stack

```
Application Layer:
  • FastAPI (API Framework)
  • Click (CLI Framework)
  • Pydantic (Data Validation)

Core Libraries:
  • scapy (Packet Capture)
  • dnspython (DNS)
  • cryptography (SSL/TLS)
  • socket (Network)

Support:
  • pytest (Testing)
  • black (Formatting)
  • ruff (Linting)
```

### Future Stack (Cloud Security)

```
Cloud Providers:
  • boto3 (AWS SDK)
  • azure-mgmt-* (Azure SDK)
  • google-cloud-* (GCP SDK)

Minimal Dependencies:
  • Use native SDKs only
  • No heavy frameworks
  • Lightweight implementation
```

## Deployment Patterns

### Pattern 1: Standalone

```
┌─────────────────┐
│  NetSec-Core    │
│  (Single Node)  │
└─────────────────┘
```

### Pattern 2: Distributed

```
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Scanner │  │ Scanner │  │ Scanner │
│ Node 1  │  │ Node 2  │  │ Node 3  │
└────┬────┘  └────┬────┘  └────┬────┘
     │            │            │
     └────────────┼────────────┘
                  │
         ┌────────▼────────┐
         │  Coordinator    │
         │  (API Server)   │
         └─────────────────┘
```

### Pattern 3: Containerized

```
┌─────────────────────────┐
│   Docker Compose        │
├─────────────────────────┤
│  • API Container        │
│  • Scanner Workers      │
│  • Redis (Cache)        │
│  • Database (Optional)  │
└─────────────────────────┘
```

## Performance Characteristics

### Resource Usage

```
Memory:
  • Base: ~50MB
  • With Scans: ~100-200MB
  • With Traffic Capture: ~200-500MB

CPU:
  • Idle: <1%
  • Active Scanning: 20-50%
  • Traffic Capture: 30-70%

Network:
  • Minimal (API calls only)
  • Scanning: Variable
  • Traffic Capture: High
```

## Scalability

### Horizontal Scaling

```
Single Instance → Multiple Instances
  • Load balancer required
  • Shared state (Redis/DB)
  • Stateless API design
```

### Vertical Scaling

```
Small → Medium → Large
  • More CPU for scanning
  • More memory for traffic
  • More workers
```
