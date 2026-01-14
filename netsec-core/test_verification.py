#!/usr/bin/env python3
"""Quick verification script to test imports and basic functionality."""

import sys
import traceback

def test_imports():
    """Test that all critical modules can be imported."""
    print("=" * 60)
    print("Testing Module Imports")
    print("=" * 60)
    
    results = []
    
    # Test core imports
    try:
        from netsec_core import __version__
        print(f"✓ netsec_core version: {__version__}")
        results.append(True)
    except Exception as e:
        print(f"✗ netsec_core import failed: {e}")
        results.append(False)
    
    # Test API
    try:
        from netsec_core.api.main import app
        print("✓ API app imported")
        results.append(True)
    except Exception as e:
        print(f"✗ API import failed: {e}")
        traceback.print_exc()
        results.append(False)
    
    # Test test logger
    try:
        from netsec_core.utils.test_logger import get_test_logger, TestStatus
        logger = get_test_logger()
        print(f"✓ Test logger imported and initialized")
        print(f"  Log directory: {logger.log_dir}")
        results.append(True)
    except Exception as e:
        print(f"✗ Test logger import failed: {e}")
        traceback.print_exc()
        results.append(False)
    
    # Test LLM analyzer
    try:
        from netsec_core.llm.analyzer import LLMAnalyzer, LLMAnalyzerLocal
        print("✓ LLM analyzer imported")
        results.append(True)
    except Exception as e:
        print(f"✗ LLM analyzer import failed: {e}")
        traceback.print_exc()
        results.append(False)
    
    # Test core scanners
    scanners = [
        ("DNSScanner", "netsec_core.core.dns_scanner", "DNSScanner"),
        ("SSLScanner", "netsec_core.core.ssl_scanner", "SSLScanner"),
        ("NetworkScanner", "netsec_core.core.network_scanner", "NetworkScanner"),
    ]
    
    for name, module_name, class_name in scanners:
        try:
            module = __import__(module_name, fromlist=[class_name])
            scanner_class = getattr(module, class_name)
            scanner = scanner_class()
            print(f"✓ {name} imported and initialized")
            results.append(True)
        except Exception as e:
            print(f"✗ {name} failed: {e}")
            results.append(False)
    
    return all(results)


def test_test_logger():
    """Test test logger functionality."""
    print("\n" + "=" * 60)
    print("Testing Test Logger")
    print("=" * 60)
    
    try:
        from netsec_core.utils.test_logger import get_test_logger, TestStatus
        
        logger = get_test_logger()
        
        # Test logging a test result
        test_record = logger.log_test(
            test_name="test_verification",
            status=TestStatus.PASSED,
            parameters={"test_type": "verification", "module": "test_logger"},
            result={"status": "success"},
            duration=0.1,
        )
        
        print(f"✓ Test logged successfully")
        print(f"  Test name: {test_record['test_name']}")
        print(f"  Status: {test_record['status']}")
        
        # Get summary
        summary = logger.get_summary()
        print(f"✓ Summary retrieved")
        print(f"  Total tests: {summary['total_tests']}")
        print(f"  Passed: {summary['passed']}")
        
        return True
    except Exception as e:
        print(f"✗ Test logger test failed: {e}")
        traceback.print_exc()
        return False


def test_llm_analyzer():
    """Test LLM analyzer initialization."""
    print("\n" + "=" * 60)
    print("Testing LLM Analyzer")
    print("=" * 60)
    
    try:
        from netsec_core.llm.analyzer import LLMAnalyzer, LLMAnalyzerLocal
        
        # Test local analyzer (no API key needed)
        local_analyzer = LLMAnalyzerLocal()
        print("✓ LLMAnalyzerLocal initialized")
        
        # Test cloud analyzer initialization (without API key, should work)
        try:
            cloud_analyzer = LLMAnalyzer(provider="openai", model="gpt-3.5-turbo")
            print("✓ LLMAnalyzer initialized (will use env var or fail gracefully)")
        except Exception as e:
            print(f"⚠ LLMAnalyzer initialization: {e} (expected if no API key)")
        
        # Test local provider
        try:
            ollama_analyzer = LLMAnalyzer(provider="ollama", model="llama2")
            print("✓ Ollama analyzer initialized (will connect on first use)")
        except Exception as e:
            print(f"⚠ Ollama analyzer: {e} (expected if Ollama not running)")
        
        return True
    except Exception as e:
        print(f"✗ LLM analyzer test failed: {e}")
        traceback.print_exc()
        return False


def test_api_structure():
    """Test API structure."""
    print("\n" + "=" * 60)
    print("Testing API Structure")
    print("=" * 60)
    
    try:
        from netsec_core.api.main import app
        
        # Count routes
        routes = [r for r in app.routes if hasattr(r, 'path')]
        print(f"✓ Found {len(routes)} API routes")
        
        # Check for key routes
        route_paths = [r.path for r in routes if hasattr(r, 'path')]
        key_routes = ["/api/v1/health", "/api/v1/dns/scan", "/api/v1/llm/analyze-traffic"]
        
        found = 0
        for route in key_routes:
            if any(route in rp for rp in route_paths):
                print(f"✓ Route exists: {route}")
                found += 1
            else:
                print(f"⚠ Route not found: {route}")
        
        return found > 0
    except Exception as e:
        print(f"✗ API structure test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all verification tests."""
    print("\n" + "=" * 60)
    print("NetSec-Core Verification Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        ("Module Imports", test_imports),
        ("Test Logger", test_test_logger),
        ("LLM Analyzer", test_llm_analyzer),
        ("API Structure", test_api_structure),
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
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All verification tests passed!")
        print("\nNext steps:")
        print("  1. Run pytest: pytest -v")
        print("  2. Check test results: tests/results/test_summary.json")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
