# Test Results Documentation

## Overview

All test results are automatically logged with parameters and outcomes. This documentation system tracks:

- Test name and status
- Test parameters (inputs, configuration)
- Test results/outputs
- Errors (if any)
- Duration
- Timestamp

## Test Result Location

Test results are stored in: `tests/results/`

- Individual test logs: `test_<timestamp>.json`
- Summary: `test_summary.json`
- Reports: `test_report.txt` (generated on demand)

## Viewing Test Results

### Using Python

```python
from netsec_core.utils.test_logger import get_test_logger

logger = get_test_logger()

# Get summary
summary = logger.get_summary()
print(f"Total: {summary['total_tests']}, Passed: {summary['passed']}")

# Get failed tests
from netsec_core.utils.test_logger import TestStatus
failed = logger.get_tests_by_status(TestStatus.FAILED)

# Get tests by name
dns_tests = logger.get_tests_by_name("test_dns_scanner")

# Generate report
report = logger.generate_report("tests/results/test_report.txt")
print(report)
```

### Using CLI

```bash
# After running tests
cd netsec-core
python -c "from netsec_core.utils.test_logger import get_test_logger; print(get_test_logger().generate_report())"
```

## Test Result Format

Each test result includes:

```json
{
  "test_name": "test_dns_scanner",
  "status": "PASSED",
  "timestamp": "2024-12-XX...",
  "parameters": {
    "parametrized": {"domain": "example.com"}
  },
  "duration_seconds": 0.123,
  "test_file": "tests/test_dns_scanner.py",
  "result": {...}
}
```

## Integration with pytest

The test logger is automatically integrated with pytest via `conftest.py`. All tests are automatically logged when run with pytest.

## Manual Test Logging

You can also manually log test results:

```python
from netsec_core.utils.test_logger import get_test_logger, TestStatus

logger = get_test_logger()

logger.log_test(
    test_name="my_custom_test",
    status=TestStatus.PASSED,
    parameters={"input": "test_value", "config": {"timeout": 5}},
    result={"output": "success"},
    duration=0.5,
)
```
