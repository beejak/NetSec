"""Test result logging and documentation system."""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from enum import Enum

# Set up logger for test logger warnings
_logger = logging.getLogger(__name__)


class TestStatus(Enum):
    """Test status enumeration."""
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    ERROR = "ERROR"


class TestResultLogger:
    """Logger for test results with parameter documentation."""
    
    def __init__(self, log_dir: Optional[str] = None):
        """
        Initialize test result logger.
        
        Args:
            log_dir: Directory to store test logs (default: tests/results/)
        """
        if log_dir:
            self.log_dir = Path(log_dir)
        else:
            # Default to tests/results/ directory
            base_dir = Path(__file__).parent.parent.parent.parent
            self.log_dir = base_dir / "tests" / "results"
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create summary file
        self.summary_file = self.log_dir / "test_summary.json"
        self._load_summary()
    
    def _load_summary(self):
        """Load existing test summary."""
        if self.summary_file.exists():
            try:
                with open(self.summary_file, 'r') as f:
                    self.summary = json.load(f)
            except Exception:
                self.summary = {
                    "total_tests": 0,
                    "passed": 0,
                    "failed": 0,
                    "skipped": 0,
                    "errors": 0,
                    "test_runs": [],
                }
        else:
            self.summary = {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "errors": 0,
                "test_runs": [],
            }
    
    def _save_summary(self):
        """Save test summary."""
        try:
            with open(self.summary_file, 'w') as f:
                json.dump(self.summary, f, indent=2)
        except Exception as e:
            _logger.warning(f"Could not save test summary: {e}")
    
    def log_test(
        self,
        test_name: str,
        status: TestStatus,
        parameters: Optional[Dict[str, Any]] = None,
        result: Optional[Any] = None,
        error: Optional[str] = None,
        duration: Optional[float] = None,
        test_file: Optional[str] = None,
    ):
        """
        Log a test result with parameters.
        
        Args:
            test_name: Name of the test
            status: Test status (PASSED, FAILED, SKIPPED, ERROR)
            parameters: Test parameters (inputs, configuration, etc.)
            result: Test result/output
            error: Error message if test failed
            duration: Test duration in seconds
            test_file: Source test file path
        """
        timestamp = datetime.utcnow().isoformat()
        
        test_record = {
            "test_name": test_name,
            "status": status.value,
            "timestamp": timestamp,
            "parameters": parameters or {},
            "duration_seconds": duration,
            "test_file": test_file,
        }
        
        if result is not None:
            # Try to serialize result, fallback to string
            try:
                if isinstance(result, (dict, list, str, int, float, bool, type(None))):
                    test_record["result"] = result
                else:
                    test_record["result"] = str(result)
            except Exception:
                test_record["result"] = str(result)
        
        if error:
            test_record["error"] = error
        
        # Save individual test log
        test_log_file = self.log_dir / f"test_{timestamp.replace(':', '-').replace('.', '-')}.json"
        try:
            with open(test_log_file, 'w') as f:
                json.dump(test_record, f, indent=2)
        except Exception as e:
            _logger.warning(f"Could not save test log: {e}")
        
        # Update summary
        self.summary["total_tests"] += 1
        if status == TestStatus.PASSED:
            self.summary["passed"] += 1
        elif status == TestStatus.FAILED:
            self.summary["failed"] += 1
        elif status == TestStatus.SKIPPED:
            self.summary["skipped"] += 1
        elif status == TestStatus.ERROR:
            self.summary["errors"] += 1
        
        # Add to test runs (keep last 1000)
        self.summary["test_runs"].append(test_record)
        if len(self.summary["test_runs"]) > 1000:
            self.summary["test_runs"] = self.summary["test_runs"][-1000:]
        
        self._save_summary()
        
        return test_record
    
    def get_summary(self) -> Dict[str, Any]:
        """Get test summary statistics."""
        return {
            "total_tests": self.summary["total_tests"],
            "passed": self.summary["passed"],
            "failed": self.summary["failed"],
            "skipped": self.summary["skipped"],
            "errors": self.summary["errors"],
            "pass_rate": (
                self.summary["passed"] / self.summary["total_tests"] * 100
                if self.summary["total_tests"] > 0
                else 0
            ),
            "latest_tests": self.summary["test_runs"][-10:] if self.summary["test_runs"] else [],
        }
    
    def get_tests_by_status(self, status: TestStatus) -> List[Dict[str, Any]]:
        """Get all tests with a specific status."""
        return [
            test for test in self.summary["test_runs"]
            if test.get("status") == status.value
        ]
    
    def get_tests_by_name(self, test_name: str) -> List[Dict[str, Any]]:
        """Get all test runs for a specific test name."""
        return [
            test for test in self.summary["test_runs"]
            if test.get("test_name") == test_name
        ]
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """
        Generate a human-readable test report.
        
        Args:
            output_file: Optional file path to save report
        
        Returns:
            Report as string
        """
        summary = self.get_summary()
        
        report = []
        report.append("=" * 80)
        report.append("NetSec-Core Test Results Report")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.utcnow().isoformat()}")
        report.append("")
        report.append("Summary:")
        report.append(f"  Total Tests: {summary['total_tests']}")
        report.append(f"  Passed: {summary['passed']} ({summary['pass_rate']:.1f}%)")
        report.append(f"  Failed: {summary['failed']}")
        report.append(f"  Skipped: {summary['skipped']}")
        report.append(f"  Errors: {summary['errors']}")
        report.append("")
        
        # Recent tests
        if summary['latest_tests']:
            report.append("Recent Test Results:")
            report.append("-" * 80)
            for test in summary['latest_tests']:
                status_symbol = "✓" if test['status'] == "PASSED" else "✗"
                report.append(
                    f"{status_symbol} {test['test_name']} - {test['status']} "
                    f"({test.get('duration_seconds', 0):.2f}s)"
                )
                if test.get('parameters'):
                    report.append(f"    Parameters: {json.dumps(test['parameters'], indent=6)}")
                if test.get('error'):
                    report.append(f"    Error: {test['error']}")
                report.append("")
        
        # Failed tests
        failed_tests = self.get_tests_by_status(TestStatus.FAILED)
        if failed_tests:
            report.append("Failed Tests:")
            report.append("-" * 80)
            for test in failed_tests[-10:]:  # Last 10 failed
                report.append(f"✗ {test['test_name']}")
                report.append(f"  Timestamp: {test['timestamp']}")
                if test.get('parameters'):
                    report.append(f"  Parameters: {json.dumps(test['parameters'], indent=4)}")
                if test.get('error'):
                    report.append(f"  Error: {test['error']}")
                report.append("")
        
        report_text = "\n".join(report)
        
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    f.write(report_text)
            except Exception as e:
                _logger.warning(f"Could not save report: {e}")
        
        return report_text


# Global instance
_test_logger = None


def get_test_logger() -> TestResultLogger:
    """Get global test logger instance."""
    global _test_logger
    if _test_logger is None:
        _test_logger = TestResultLogger()
    return _test_logger
