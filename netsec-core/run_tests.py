#!/usr/bin/env python3
"""Comprehensive test runner and verification script for NetSec-Core."""

import sys
import importlib
import traceback
from pathlib import Path


def test_imports():
    """Test that all critical modules can be imported."""
    print("=" * 60)
    print("Testing Module Imports")
    print("=" * 60)
    
    modules_to_test = [
        ("netsec_core", "__version__"),
        ("netsec_core.api.main", "app"),
        ("netsec_core.api.models", "ScanRequest"),
        ("netsec_core.core.dns_scanner", "DNSScanner"),
        ("netsec_core.core.ssl_scanner", "SSLScanner"),
        ("netsec_core.core.network_scanner", "NetworkScanner"),
        ("netsec_core.core.traffic_analyzer", "TrafficAnalyzer"),
        ("netsec_core.core.anomaly_detector", "AnomalyDetector"),
        ("netsec_core.core.asset_discovery", "AssetDiscovery"),
        ("netsec_core.cli.main", "cli"),
        ("netsec_core.llm.analyzer", "LLMAnalyzer"),
        ("netsec_core.remediation.guide", "RemediationGuide"),
        ("netsec_core.config", "get_config"),
        ("netsec_core.utils.logger", "setup_logger"),
    ]
    
    results = []
    for module_name, attr_name in modules_to_test:
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, attr_name):
                print(f"✓ {module_name}.{attr_name}")
                results.append(True)
            else:
                print(f"✗ {module_name}.{attr_name} - Attribute not found")
                results.append(False)
        except Exception as e:
            print(f"✗ {module_name} - {e}")
            results.append(False)
    
    return all(results)


def test_api_structure():
    """Test API structure and routes."""
    print("\n" + "=" * 60)
    print("Testing API Structure")
    print("=" * 60)
    
    try:
        from netsec_core.api.main import app
        
        # Get all routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                routes.append((route.path, route.methods))
        
        print(f"✓ Found {len(routes)} API routes")
        
        # Check for key routes
        route_paths = [r[0] for r in routes]
        key_routes = [
            "/api/v1/health",
            "/api/v1/dns/scan",
            "/api/v1/ssl/check-certificate",
            "/api/v1/scan/ports",
        ]
        
        for route in key_routes:
            if any(route in rp for rp in route_paths):
                print(f"✓ Route exists: {route}")
            else:
                print(f"⚠ Route not found: {route}")
        
        return True
    except Exception as e:
        print(f"✗ API structure test failed: {e}")
        traceback.print_exc()
        return False


def test_cli_structure():
    """Test CLI structure."""
    print("\n" + "=" * 60)
    print("Testing CLI Structure")
    print("=" * 60)
    
    try:
        from netsec_core.cli.main import cli
        
        # Check if cli is a Click group
        if hasattr(cli, 'commands'):
            print(f"✓ CLI has {len(cli.commands)} command groups")
            for cmd_name in cli.commands.keys():
                print(f"  - {cmd_name}")
        else:
            print("⚠ CLI structure unexpected")
        
        return True
    except Exception as e:
        print(f"✗ CLI structure test failed: {e}")
        traceback.print_exc()
        return False


def test_scanner_initialization():
    """Test scanner initialization."""
    print("\n" + "=" * 60)
    print("Testing Scanner Initialization")
    print("=" * 60)
    
    scanners = [
        ("DNSScanner", "netsec_core.core.dns_scanner", "DNSScanner"),
        ("SSLScanner", "netsec_core.core.ssl_scanner", "SSLScanner"),
        ("NetworkScanner", "netsec_core.core.network_scanner", "NetworkScanner"),
        ("TrafficAnalyzer", "netsec_core.core.traffic_analyzer", "TrafficAnalyzer"),
        ("AnomalyDetector", "netsec_core.core.anomaly_detector", "AnomalyDetector"),
        ("AssetDiscovery", "netsec_core.core.asset_discovery", "AssetDiscovery"),
    ]
    
    results = []
    for name, module_name, class_name in scanners:
        try:
            module = importlib.import_module(module_name)
            scanner_class = getattr(module, class_name)
            scanner = scanner_class()
            print(f"✓ {name} initialized")
            results.append(True)
        except Exception as e:
            print(f"✗ {name} initialization failed: {e}")
            results.append(False)
    
    return all(results)


def test_config_and_logging():
    """Test configuration and logging."""
    print("\n" + "=" * 60)
    print("Testing Configuration & Logging")
    print("=" * 60)
    
    try:
        from netsec_core.config import get_config
        config = get_config()
        print(f"✓ Configuration loaded")
        print(f"  - API Host: {config.get('api', {}).get('host', 'N/A')}")
        print(f"  - API Port: {config.get('api', {}).get('port', 'N/A')}")
        
        from netsec_core.utils.logger import setup_logger
        logger = setup_logger("test")
        logger.info("Test log message")
        print("✓ Logger initialized and working")
        
        return True
    except Exception as e:
        print(f"✗ Config/Logging test failed: {e}")
        traceback.print_exc()
        return False


def test_file_structure():
    """Test that all expected files exist."""
    print("\n" + "=" * 60)
    print("Testing File Structure")
    print("=" * 60)
    
    base_path = Path(__file__).parent
    required_files = [
        "README.md",
        "requirements.txt",
        "setup.py",
        "pyproject.toml",
        "Dockerfile",
        "docker-compose.yml",
        ".github/workflows/ci.yml",
    ]
    
    results = []
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
            results.append(True)
        else:
            print(f"✗ {file_path} - Missing")
            results.append(False)
    
    return all(results)


def main():
    """Run all verification tests."""
    print("\n" + "=" * 60)
    print("NetSec-Core Comprehensive Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        ("File Structure", test_file_structure),
        ("Module Imports", test_imports),
        ("API Structure", test_api_structure),
        ("CLI Structure", test_cli_structure),
        ("Scanner Initialization", test_scanner_initialization),
        ("Configuration & Logging", test_config_and_logging),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test crashed: {e}")
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} test suites passed")
    
    if passed == total:
        print("\n🎉 All verification tests passed!")
        print("\nNext steps:")
        print("  1. Run pytest: pytest -v")
        print("  2. Run quick test: python test_quick.py")
        print("  3. Start API: python run_api.py")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test suite(s) failed")
        print("Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
