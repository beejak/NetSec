# Test Instructions

## Quick Verification

Run the verification script to test all imports and basic functionality:

```bash
cd netsec-core
python test_verification.py
```

This will test:
- ✅ Module imports
- ✅ Test logger functionality
- ✅ LLM analyzer initialization
- ✅ API structure

## Full Test Suite

Run the complete pytest suite:

```bash
# Install dependencies first
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run all tests
pytest -v

# Run with coverage
pytest --cov=netsec_core --cov-report=term-missing

# Run specific test file
pytest tests/test_dns_scanner.py -v
```

## Test Results

After running tests, results are automatically logged to:
- `tests/results/test_summary.json` - Summary statistics
- `tests/results/test_<timestamp>.json` - Individual test logs

View test results:

```bash
python -c "from netsec_core.utils.test_logger import get_test_logger; print(get_test_logger().generate_report())"
```

## Quick Functional Test

Run the quick functional test:

```bash
python test_quick.py
```

## Test Individual Components

### Test DNS Scanner
```bash
python -c "from netsec_core.core.dns_scanner import DNSScanner; s = DNSScanner(); print(s.scan_domain('example.com'))"
```

### Test SSL Scanner
```bash
python -c "from netsec_core.core.ssl_scanner import SSLScanner; s = SSLScanner(); print(s.check_certificate('example.com', 443))"
```

### Test Network Scanner
```bash
python -c "from netsec_core.core.network_scanner import NetworkScanner; s = NetworkScanner(); print(s.scan_ports('127.0.0.1', [22, 80, 443]))"
```

### Test Test Logger
```bash
python -c "from netsec_core.utils.test_logger import get_test_logger, TestStatus; logger = get_test_logger(); logger.log_test('test_manual', TestStatus.PASSED, {'param': 'value'}); print('Test logged!')"
```

### Test LLM Analyzer (Local)
```bash
python -c "from netsec_core.llm.analyzer import LLMAnalyzerLocal; a = LLMAnalyzerLocal(); print(a.explain_finding({'type': 'test', 'severity': 'low', 'description': 'Test finding'}))"
```

## API Testing

Start the API server:

```bash
python run_api.py
# or
uvicorn netsec_core.api.main:app --reload
```

Then test endpoints:

```bash
# Health check
curl http://localhost:8000/api/v1/health

# DNS scan
curl -X POST "http://localhost:8000/api/v1/dns/scan" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

## Expected Results

All tests should:
- ✅ Import successfully
- ✅ Initialize without errors
- ✅ Execute basic functionality
- ✅ Log results automatically (for pytest tests)

## Troubleshooting

### Import Errors
- Make sure you're in the `netsec-core` directory
- Install dependencies: `pip install -r requirements.txt`
- Install package: `pip install -e .`

### Test Logger Errors
- Check that `tests/results/` directory exists or can be created
- Verify write permissions

### LLM Errors
- Local models (Ollama, etc.) require the service to be running
- Cloud models require API keys (set environment variables)
- Falls back to rule-based if LLM unavailable

## Next Steps

After running tests:
1. Review test results in `tests/results/`
2. Check test summary for pass/fail rates
3. Review any failed tests
4. Run specific tests for debugging
