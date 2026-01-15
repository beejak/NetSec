# Run All Tests - Complete Guide

## Quick Start

### NetSec-Core
```bash
cd netsec-core
python sanitize_and_test.py
```

### NetSec-Cloud
```bash
cd netsec-cloud
python sanitize_and_test.py
```

## What Gets Tested

### Sanitization & Test Scripts

Both `sanitize_and_test.py` scripts run:

1. **Import Verification** - All critical modules
2. **Code Linting** - Style and quality checks
3. **Type Checking** - Type hint validation
4. **Verification Scripts** - Basic functionality
5. **Quick Tests** - Fast functional tests
6. **Full Test Suite** - Complete pytest coverage

## Individual Test Commands

### NetSec-Core

```bash
# 1. Sanitization & full test suite
python sanitize_and_test.py

# 2. Just verification
python test_verification.py

# 3. Quick functional test
python test_quick.py

# 4. Comprehensive verification
python run_tests.py

# 5. Full pytest suite
pytest -v

# 6. Pytest with coverage
pytest --cov=netsec_core --cov-report=term-missing

# 7. Specific test file
pytest tests/test_dns_scanner.py -v
```

### NetSec-Cloud

```bash
# 1. Sanitization & full test suite
python sanitize_and_test.py

# 2. Verification
python run_tests.py

# 3. Full pytest suite
pytest -v

# 4. Specific test file
pytest tests/test_providers.py -v
```

## Test Result Location

After running tests, results are automatically logged to:
- `tests/results/test_summary.json` - Summary statistics
- `tests/results/test_<timestamp>.json` - Individual test logs

View results:
```bash
python -c "from netsec_core.utils.test_logger import get_test_logger; print(get_test_logger().generate_report())"
```

## Expected Results

### Sanitization Script Output

```
============================================================
NetSec-Core: Code Sanitization & Test Suite
============================================================

[1/6] Checking imports...
✓ All imports successful

[2/6] Running linter...
✓ Code Linting - PASSED

[3/6] Type checking...
✓ Type Checking - PASSED

[4/6] Running verification script...
✓ Verification Script - PASSED

[5/6] Running quick functional test...
✓ Quick Functional Test - PASSED

[6/6] Running pytest suite...
✓ Pytest Test Suite - PASSED

============================================================
Sanitization & Test Summary
============================================================
✓ PASS: Imports
✓ PASS: Linting
✓ PASS: Type Checking
✓ PASS: Verification
✓ PASS: Quick Test
✓ PASS: Pytest

Total: 6/6 checks passed

🎉 All checks passed! Code is clean and ready.
```

## Troubleshooting

### Import Errors
```bash
# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### Linter Not Found
```bash
# Install linting tools
pip install ruff mypy
```

### Pytest Not Found
```bash
# Install pytest
pip install -r requirements-dev.txt
```

### Test Logger Errors
- Check `tests/results/` directory exists
- Verify write permissions
- Check disk space

## Pre-Push Checklist

Before pushing to GitHub:

- [ ] Run sanitization script
- [ ] All tests pass
- [ ] No linter errors
- [ ] No type errors
- [ ] Test results documented
- [ ] Code reviewed

## Status

✅ **All test infrastructure ready**
✅ **Sanitization scripts created**
✅ **Code cleaned and ready**

**Run `python sanitize_and_test.py` to verify everything!**
