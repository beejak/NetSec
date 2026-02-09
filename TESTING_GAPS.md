# Testing Gaps Report

This report maps **features** across NetSec-Core, NetSec-Cloud, and NetSec-Container to **existing tests** and calls out **gaps** (features with no or weak test coverage).

---

## NetSec-Core

| Feature | Type | Test file(s) | Covered? | Gap |
|--------|------|--------------|----------|-----|
| **API: root** | API | test_api_health | Yes | — |
| **API: /api/v1/health** | API | test_api_health | Yes | — |
| **API: /api/v1/dns/scan** | API | test_api_routes | Yes | — |
| **API: /api/v1/ssl/check-certificate** | API | test_api_routes | Yes | — |
| **API: /api/v1/scan/ports** | API | test_api_routes | Yes | — |
| **API: /api/v1/anomaly/status** | API | test_api_routes | Yes | — |
| **API: /api/v1/remediation/** (list, get) | API | test_api_routes | Yes | — |
| **API: /api/v1/traffic/** | API | test_api_routes | Yes | test_traffic_flows_endpoint, test_traffic_analyze_endpoint |
| **API: /api/v1/anomaly/learn-baseline, detect** | API | test_api_routes | Yes | test_anomaly_learn_baseline_endpoint; detect already tested |
| **API: /api/v1/assets/discover, inventory** | API | test_api_routes | Yes | test_assets_discover_endpoint; inventory already tested |
| **API: /api/v1/llm/** | API | test_api_routes | Yes | test_llm_analyze_traffic_endpoint (smoke) |
| **CLI: --version, --help** | CLI | test_cli | Yes | — |
| **CLI: scan ports, dns scan, ssl check** | CLI | test_cli | Yes | — |
| **CLI: traffic, anomaly, assets, remediation, health** | CLI | test_cli | Yes | test_traffic_command, test_anomaly_command, test_assets_command, test_remediation_get_command, test_health_command |
| **Core: DNSScanner** | Unit | test_dns_scanner | Yes | — |
| **Core: SSLScanner** | Unit | test_ssl_scanner | Yes | — |
| **Core: NetworkScanner** | Unit | test_network_scanner | Yes | — |
| **Core: RemediationGuide** | Unit | test_remediation_guide | Yes | — |
| **Core: TrafficAnalyzer** | Unit | — | **No** | Requires scapy; no unit test |
| **Core: AnomalyDetector** | Unit | — | **No** | No unit test for detector logic |
| **Core: AssetDiscovery** | Unit | — | **No** | No unit test (may need network) |
| **Core: LLMAnalyzer** | Unit | — | **No** | No unit test (mock API or skip) |
| **Integration: API flows** | Integration | integration/test_api_integration | Yes | — |
| **Integration: CLI flows** | Integration | integration/test_cli_integration | Yes | — |

**Core gaps summary:** API and CLI for traffic, anomaly, assets, remediation, health are now covered (smoke). Remaining: TrafficAnalyzer, AnomalyDetector, AssetDiscovery, LLMAnalyzer unit tests (optional; may need network or mock).

---

## NetSec-Cloud

| Feature | Type | Test file(s) | Covered? | Gap |
|--------|------|--------------|----------|-----|
| **API: root** | API | test_api | Yes | — |
| **API: /api/v1/health** | API | test_api | Yes | — |
| **API: /api/v1/cloud/providers** | API | test_api | Yes | — |
| **API: /api/v1/cloud/scan** (POST) | API | test_api | Yes (401 without creds) | — |
| **API: /api/v1/cloud/scan/multi** | API | test_api | Yes | test_multi_cloud_scan_accepts_body |
| **API: /api/v1/cloud/compliance/frameworks** | API | test_api | Yes | — |
| **API: /api/v1/cloud/compliance/frameworks/{fw}/controls** | API | test_api | Yes | — |
| **API: /api/v1/cloud/compliance/check** (POST) | API | test_api | Yes | test_compliance_check_requires_auth, test_compliance_check_bad_framework |
| **CLI: --help, scan --help, providers** | CLI | test_cli | Yes | — |
| **CLI: scan aws/azure/gcp** (full run) | CLI | — | **No** | Would need creds or mock |
| **Core: CloudScanner** | Unit | test_scanner | Yes | — |
| **Core: AWSProvider** (init, scan_* return list) | Unit | test_providers | Yes | — |
| **Core: AzureProvider** | Unit | test_providers | Yes | — |
| **Core: GCPProvider** | Unit | test_providers | Yes | — |
| **Core: compliance mapping** | Unit | test_compliance | Yes | — |
| **Core: checks (storage, iam, networking)** | Unit | — | **No** | Checks not directly tested |

**Cloud gaps summary:** Multi-cloud scan and compliance/check POST are tested (test_multi_cloud_scan_accepts_body, test_compliance_check_requires_auth, test_compliance_check_bad_framework). Remaining: CLI scan full run (would need creds or mock); checks module unit tests.

---

## NetSec-Container

| Feature | Type | Test file(s) | Covered? | Gap |
|--------|------|--------------|----------|-----|
| **API: / (HTML)** | API | test_api | Yes | test_root_returns_html |
| **API: /api/v1/health** | API | test_api | Yes | — |
| **API: /api/v1/scan** (POST) | API | test_api | Partial (200 or 500) | — |
| **API: /api/v1/scan/upload** | API | test_api | Yes | test_scan_upload_accepts_multipart |
| **CLI: --help, scan --help** | CLI | test_cli | Yes | — |
| **CLI: scan (full run)** | CLI | — | **No** | Would need Docker/image |
| **CLI: serve** | CLI | — | **No** | No test |
| **Core: ContainerScanner** (init, methods exist) | Unit | test_scanner | Yes | — |
| **Core: RiskScorer** | Unit | test_scoring | Yes | — |
| **Core: ScanResults, Vulnerability, Secret** | Unit | — | **No** | Only used in test_scoring indirectly |
| **Core: secrets, vulnerability, dockerfile, sbom** | Unit | — | **No** | No unit tests for these modules |
| **Core: LLM analyzer** | Unit | — | **No** | No unit test |

**Container gaps summary:** Root, health, scan POST, scan/upload (test_scan_upload_accepts_multipart), and unit tests for secrets, vuln, dockerfile, scoring, image_extractor are covered. Remaining: CLI scan/serve full run (would need Docker/image); additional unit coverage for ScanResults/Vulnerability/Secret and LLM.

---

## Cross-project gaps (high level)

| Area | Core | Cloud | Container |
|------|------|-------|-----------|
| **LLM-related** | No API/unit test | N/A | No unit test |
| **Traffic / network-heavy** | No TrafficAnalyzer test | N/A | N/A |
| **File upload / multipart** | N/A | N/A | test_scan_upload_accepts_multipart |
| **Integration with real services** | Optional | Optional (moto, etc.) | Optional (Docker) |
| **Compliance POST with body** | N/A | test_compliance_check_* | N/A |

---

## How to run tests and see gaps

```bash
# Run all tests (unit + api + cli; exclude integration for speed)
cd netsec-core   && pytest -v -m "not integration"
cd netsec-cloud  && pytest -v -m "not integration"
cd netsec-container && pytest -v -m "not integration"

# Run only unit tests
pytest -m unit -v

# Run only API tests
pytest -m api -v
```

**Tests added in this pass**

- **Core:** test_remediation_guide.py (unit); test_api_routes extended (anomaly status, remediation list/get).
- **Cloud:** test_api extended (compliance controls, scan 401); test_cli.py (help, scan help, providers).
- **Container:** test_api.py (health, scan POST smoke); test_cli.py (help, scan help); test_scoring.py (RiskScorer unit).

**Remaining gaps** (to close later): Core unit tests for TrafficAnalyzer, AnomalyDetector, AssetDiscovery, LLMAnalyzer (optional); Cloud checks module unit tests; Container CLI scan/serve full run; container core modules (secrets, vuln, dockerfile, sbom) additional unit coverage.
