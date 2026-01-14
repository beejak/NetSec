# NetSec-Cloud: Network Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│              NetSec-Cloud System                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐         ┌──────────────┐             │
│  │   API Layer  │         │   CLI Layer  │             │
│  │  (FastAPI)   │         │   (Click)    │             │
│  └──────┬───────┘         └──────┬───────┘             │
│         │                        │                     │
│         └───────────┬─────────────┘                     │
│                     │                                   │
│            ┌────────▼────────┐                          │
│            │  Cloud Scanner  │                          │
│            │   (Unified)     │                          │
│            └────────┬────────┘                          │
│                     │                                   │
│    ┌────────────────┼────────────────┐                │
│    │                │                │                │
│ ┌──▼──┐        ┌───▼───┐        ┌───▼───┐            │
│ │ AWS │        │ Azure │        │  GCP  │            │
│ │ SDK │        │  SDK  │        │  SDK  │            │
│ └──┬──┘        └───┬───┘        └───┬───┘            │
│    │               │                │                 │
│    └───────────────┼────────────────┘                 │
│                    │                                   │
│            ┌───────▼────────┐                         │
│            │  Cloud APIs     │                         │
│            │  (Internet)     │                         │
│            └─────────────────┘                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Data Flow: Cloud Scan

```
User Request
    │
    ▼
┌─────────────┐
│  API/CLI    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Scanner    │
│  Engine     │
└──────┬──────┘
       │
       │ Select Provider
       ▼
┌─────────────┐
│  Provider   │
│  (AWS/Azure/GCP)│
└──────┬──────┘
       │
       │ Authenticate
       ▼
┌─────────────┐
│  Cloud SDK  │
└──────┬──────┘
       │
       │ API Calls
       ▼
┌─────────────┐
│  Cloud APIs │
│  (Internet) │
└──────┬──────┘
       │
       │ Responses
       ▼
┌─────────────┐
│  Findings   │
│  Processing │
└──────┬──────┘
       │
       │ Format
       ▼
┌─────────────┐
│  Results    │
└─────────────┘
```

## Network Topology

### Deployment Scenarios

#### Scenario 1: On-Premise Deployment

```
┌─────────────────┐
│  On-Premise      │
│  Network         │
│                  │
│  ┌────────────┐  │
│  │ NetSec-    │  │
│  │ Cloud      │  │
│  └─────┬──────┘  │
│        │         │
│        │ Internet│
│        ▼         │
│  ┌────────────┐  │
│  │  Cloud     │  │
│  │  Providers │  │
│  │  (AWS/     │  │
│  │   Azure/   │  │
│  │   GCP)     │  │
│  └────────────┘  │
└──────────────────┘
```

#### Scenario 2: Cloud Deployment

```
┌─────────────────────────────────┐
│  Cloud Environment (AWS/Azure/GCP)│
│                                   │
│  ┌────────────┐                   │
│  │ NetSec-    │                   │
│  │ Cloud      │                   │
│  │ (Container)│                   │
│  └─────┬──────┘                   │
│        │                          │
│        │ Cloud APIs               │
│        ▼                          │
│  ┌────────────┐                   │
│  │  Same Cloud│                   │
│  │  Resources │                   │
│  └────────────┘                   │
│                                   │
│  ┌────────────┐                   │
│  │  Other     │                   │
│  │  Clouds    │                   │
│  │  (Internet)│                   │
│  └────────────┘                   │
└───────────────────────────────────┘
```

## Security Architecture

### Credential Flow

```
┌─────────────┐
│  Credentials│
│  (Secure)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Provider   │
│  Auth      │
└──────┬──────┘
       │
       │ Token/Session
       ▼
┌─────────────┐
│  Cloud SDK  │
└──────┬──────┘
       │
       │ Authenticated
       │ Requests
       ▼
┌─────────────┐
│  Cloud APIs  │
└─────────────┘
```

### Network Security

```
┌─────────────────────────────────────┐
│      Security Layers                 │
├─────────────────────────────────────┤
│                                     │
│  Layer 1: Network                   │
│  • TLS/HTTPS for all API calls      │
│  • No credentials in URLs           │
│  • Secure credential storage        │
│                                     │
│  Layer 2: Authentication            │
│  • Provider-specific auth           │
│  • Token-based access               │
│  • Credential rotation support      │
│                                     │
│  Layer 3: Authorization             │
│  • Least privilege access           │
│  • Read-only operations             │
│  • Audit logging                    │
│                                     │
└─────────────────────────────────────┘
```

## Integration Architecture

### With NetSec-Core

```
┌─────────────────┐
│  NetSec-Core    │
│  (Network)      │
└────────┬────────┘
         │
         │ API Call
         ▼
┌─────────────────┐
│  NetSec-Cloud   │
│  (Cloud)        │
└────────┬────────┘
         │
         │ Cloud APIs
         ▼
┌─────────────────┐
│  Cloud          │
│  Providers      │
└─────────────────┘
```

### Standalone

```
┌─────────────────┐
│  User/CI/CD     │
└────────┬────────┘
         │
         │ Direct API/CLI
         ▼
┌─────────────────┐
│  NetSec-Cloud   │
└────────┬────────┘
         │
         │ Cloud APIs
         ▼
┌─────────────────┐
│  Cloud          │
│  Providers      │
└─────────────────┘
```

## Performance Architecture

### Concurrent Scanning

```
┌─────────────────┐
│  Scanner        │
│  Orchestrator   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│ Thread │ │ Thread │
│ Pool   │ │ Pool   │
└───┬────┘ └───┬────┘
    │          │
    ▼          ▼
┌────────┐ ┌────────┐
│ AWS    │ │ Azure  │
│ Scan   │ │ Scan   │
└────────┘ └────────┘
```

### Rate Limiting

```
┌─────────────────┐
│  Rate Limiter   │
│  (Per Provider)  │
└────────┬────────┘
         │
         │ Throttled
         ▼
┌─────────────────┐
│  Cloud APIs     │
└─────────────────┘
```

## Deployment Architecture

### Docker Deployment

```
┌─────────────────────────┐
│  Docker Container       │
├─────────────────────────┤
│  • NetSec-Cloud         │
│  • Python Runtime       │
│  • Cloud SDKs          │
└───────────┬─────────────┘
            │
            │ Network
            ▼
┌─────────────────────────┐
│  Cloud Provider APIs     │
└─────────────────────────┘
```

### Kubernetes Deployment

```
┌─────────────────────────┐
│  Kubernetes Cluster     │
├─────────────────────────┤
│                         │
│  ┌──────────────┐      │
│  │  NetSec-     │      │
│  │  Cloud Pod   │      │
│  └──────┬───────┘      │
│         │              │
│         │ Service      │
│         ▼              │
│  ┌──────────────┐      │
│  │  Service     │      │
│  │  (LoadBal)   │      │
│  └──────────────┘      │
│                         │
└─────────────────────────┘
```

## Network Requirements

### Outbound Connections

- **AWS**: `*.amazonaws.com` (HTTPS)
- **Azure**: `*.azure.com`, `*.microsoft.com` (HTTPS)
- **GCP**: `*.googleapis.com`, `*.google.com` (HTTPS)

### Ports

- **API Server**: 8000 (configurable)
- **Outbound**: 443 (HTTPS) only

### Firewall Rules

```
Allow outbound HTTPS (443) to:
  - *.amazonaws.com (AWS)
  - *.azure.com (Azure)
  - *.googleapis.com (GCP)
```

## Security Considerations

1. **Credential Security**
   - Never log credentials
   - Use secure storage (Vault, Secrets Manager)
   - Rotate credentials regularly

2. **Network Security**
   - All API calls over HTTPS
   - Verify SSL certificates
   - Use VPN if required

3. **Access Control**
   - Least privilege IAM roles
   - Read-only access recommended
   - Audit all API calls

4. **Data Security**
   - Encrypt findings at rest
   - Secure transmission
   - No sensitive data in logs
