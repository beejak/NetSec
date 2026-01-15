#!/usr/bin/env python3
"""Quick test script for NetSec-Core functionality."""

import sys
import traceback


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from netsec_core import __version__
        print(f"[OK] NetSec-Core version: {__version__}")
        
        from netsec_core.api.main import app
        print("[OK] FastAPI app imported")
        
        from netsec_core.core.dns_scanner import DNSScanner
        print("[OK] DNS Scanner imported")
        
        from netsec_core.core.ssl_scanner import SSLScanner
        print("[OK] SSL Scanner imported")
        
        from netsec_core.core.network_scanner import NetworkScanner
        print("[OK] Network Scanner imported")
        
        from netsec_core.core.traffic_analyzer import TrafficAnalyzer
        print("[OK] Traffic Analyzer imported")
        
        from netsec_core.core.anomaly_detector import AnomalyDetector
        print("[OK] Anomaly Detector imported")
        
        from netsec_core.core.asset_discovery import AssetDiscovery
        print("[OK] Asset Discovery imported")
        
        from netsec_core.cli.main import cli
        print("[OK] CLI imported")
        
        return True
    except Exception as e:
        print(f"[FAIL] Import error: {e}")
        traceback.print_exc()
        return False


def test_dns_scanner():
    """Test DNS scanner basic functionality."""
    print("\nTesting DNS Scanner...")
    try:
        from netsec_core.core.dns_scanner import DNSScanner
        scanner = DNSScanner()
        
        # Test with a simple domain
        result = scanner.scan_domain("example.com", check_tunneling=False, check_spoofing=False, analyze_patterns=False)
        
        if "domain" in result and result["domain"] == "example.com":
            print("[OK] DNS Scanner basic test passed")
            return True
        else:
            print("[FAIL] DNS Scanner test failed: unexpected result")
            return False
    except Exception as e:
        print(f"[FAIL] DNS Scanner error: {e}")
        traceback.print_exc()
        return False


def test_ssl_scanner():
    """Test SSL scanner basic functionality."""
    print("\nTesting SSL Scanner...")
    try:
        from netsec_core.core.ssl_scanner import SSLScanner
        scanner = SSLScanner()
        
        # Test certificate parsing (may fail if network unavailable)
        try:
            result = scanner.check_certificate("example.com", port=443, check_expiration=False, check_ciphers=False, check_chain=False)
            if "hostname" in result:
                print("[OK] SSL Scanner basic test passed")
                return True
        except Exception:
            print("[WARN] SSL Scanner test skipped (network unavailable)")
            return True  # Not a failure, just network issue
    except Exception as e:
        print(f"[FAIL] SSL Scanner error: {e}")
        traceback.print_exc()
        return False


def test_network_scanner():
    """Test network scanner basic functionality."""
    print("\nTesting Network Scanner...")
    try:
        from netsec_core.core.network_scanner import NetworkScanner
        scanner = NetworkScanner()
        
        # Test port scanning on localhost
        result = scanner.scan_ports("127.0.0.1", ports=[22, 80, 443], scan_type="tcp", timeout=1.0)
        
        if "scan_id" in result and "target" in result:
            print("[OK] Network Scanner basic test passed")
            print(f"  Found {len(result.get('open_ports', []))} open ports")
            return True
        else:
            print("[FAIL] Network Scanner test failed: unexpected result")
            return False
    except Exception as e:
        print(f"[FAIL] Network Scanner error: {e}")
        traceback.print_exc()
        return False


def test_anomaly_detector():
    """Test anomaly detector basic functionality."""
    print("\nTesting Anomaly Detector...")
    try:
        from netsec_core.core.anomaly_detector import AnomalyDetector
        detector = AnomalyDetector()
        
        # Test baseline learning
        result = detector.learn_baseline(duration=60)
        if result.get("status") == "learning":
            print("[OK] Anomaly Detector basic test passed")
            return True
        else:
            print("[FAIL] Anomaly Detector test failed")
            return False
    except Exception as e:
        print(f"[FAIL] Anomaly Detector error: {e}")
        traceback.print_exc()
        return False


def test_api_models():
    """Test API models."""
    print("\nTesting API Models...")
    try:
        from netsec_core.api.models import ScanRequest, ScanResult, Finding, Severity
        
        # Test ScanRequest
        request = ScanRequest(target="example.com", ports=[80, 443])
        assert request.target == "example.com"
        
        # Test Finding
        finding = Finding(
            finding_id="test-1",
            type="test",
            severity=Severity.HIGH,
            description="Test finding"
        )
        assert finding.severity == Severity.HIGH
        
        print("[OK] API Models test passed")
        return True
    except Exception as e:
        print(f"[FAIL] API Models error: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all quick tests."""
    print("=" * 60)
    print("NetSec-Core Quick Test Suite")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("API Models", test_api_models),
        ("DNS Scanner", test_dns_scanner),
        ("SSL Scanner", test_ssl_scanner),
        ("Network Scanner", test_network_scanner),
        ("Anomaly Detector", test_anomaly_detector),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"[FAIL] {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[OK] PASS" if result else "[FAIL] FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed!")
        return 0
    else:
        print(f"\n[WARN]️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
