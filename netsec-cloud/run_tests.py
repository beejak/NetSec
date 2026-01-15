#!/usr/bin/env python3
"""Comprehensive test runner and verification script for NetSec-Cloud."""

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
        ("netsec_cloud", "__version__"),
        ("netsec_cloud.scanner", "CloudScanner"),
        ("netsec_cloud.providers.base", "CloudProvider"),
        ("netsec_cloud.providers.aws", "AWSProvider"),
        ("netsec_cloud.providers.azure", "AzureProvider"),
        ("netsec_cloud.providers.gcp", "GCPProvider"),
        ("netsec_cloud.api.main", "app"),
        ("netsec_cloud.api.models", "ScanRequest"),
        ("netsec_cloud.checks.base", "SecurityCheck"),
        ("netsec_cloud.checks.storage", "StorageSecurityCheck"),
        ("netsec_cloud.checks.iam", "IAMSecurityCheck"),
        ("netsec_cloud.checks.networking", "NetworkingSecurityCheck"),
        ("netsec_cloud.cli.main", "cli"),
    ]
    
    results = []
    for module_name, attr_name in modules_to_test:
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, attr_name):
                print(f"[OK] {module_name}.{attr_name}")
                results.append(True)
            else:
                print(f"[FAIL] {module_name}.{attr_name} - Attribute not found")
                results.append(False)
        except Exception as e:
            print(f"[FAIL] {module_name} - {e}")
            results.append(False)
    
    return all(results)


def test_api_structure():
    """Test API structure and routes."""
    print("\n" + "=" * 60)
    print("Testing API Structure")
    print("=" * 60)
    
    try:
        from netsec_cloud.api.main import app
        
        # Get all routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                routes.append((route.path, route.methods))
        
        print(f"[OK] Found {len(routes)} API routes")
        
        # Check for key routes
        route_paths = [r[0] for r in routes]
        key_routes = [
            "/api/v1/health",
            "/api/v1/cloud/scan",
            "/api/v1/cloud/providers",
        ]
        
        for route in key_routes:
            if any(route in rp for rp in route_paths):
                print(f"[OK] Route exists: {route}")
            else:
                print(f"[WARN] Route not found: {route}")
        
        return True
    except Exception as e:
        print(f"[FAIL] API structure test failed: {e}")
        traceback.print_exc()
        return False


def test_provider_structure():
    """Test provider structure."""
    print("\n" + "=" * 60)
    print("Testing Provider Structure")
    print("=" * 60)
    
    providers = [
        ("AWSProvider", "netsec_cloud.providers.aws", "AWSProvider"),
        ("AzureProvider", "netsec_cloud.providers.azure", "AzureProvider"),
        ("GCPProvider", "netsec_cloud.providers.gcp", "GCPProvider"),
    ]
    
    results = []
    for name, module_name, class_name in providers:
        try:
            module = importlib.import_module(module_name)
            provider_class = getattr(module, class_name)
            # Just check it exists, don't initialize (requires credentials)
            print(f"[OK] {name} class found")
            results.append(True)
        except Exception as e:
            print(f"[FAIL] {name} not found: {e}")
            results.append(False)
    
    return all(results)


def test_scanner_structure():
    """Test scanner structure."""
    print("\n" + "=" * 60)
    print("Testing Scanner Structure")
    print("=" * 60)
    
    try:
        from netsec_cloud.scanner import CloudScanner
        scanner = CloudScanner()
        print("[OK] CloudScanner initialized")
        print(f"  - Providers: {len(scanner.providers)}")
        return True
    except Exception as e:
        print(f"[FAIL] Scanner test failed: {e}")
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
        ".github/workflows/ci.yml",
    ]
    
    results = []
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"[OK] {file_path}")
            results.append(True)
        else:
            print(f"[FAIL] {file_path} - Missing")
            results.append(False)
    
    return all(results)


def main():
    """Run all verification tests."""
    print("\n" + "=" * 60)
    print("NetSec-Cloud Comprehensive Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        ("File Structure", test_file_structure),
        ("Module Imports", test_imports),
        ("API Structure", test_api_structure),
        ("Provider Structure", test_provider_structure),
        ("Scanner Structure", test_scanner_structure),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n[FAIL] {name} test crashed: {e}")
            traceback.print_exc()
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
    
    print(f"\nTotal: {passed}/{total} test suites passed")
    
    if passed == total:
        print("\n[SUCCESS] All verification tests passed!")
        print("\nNext steps:")
        print("  1. Run pytest: pytest -v")
        print("  2. Start API: uvicorn netsec_cloud.api.main:app --reload")
        return 0
    else:
        print(f"\n[WARN]️  {total - passed} test suite(s) failed")
        print("Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
