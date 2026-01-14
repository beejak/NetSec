"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from netsec_core.api.main import app
from netsec_core.utils.test_logger import TestResultLogger, TestStatus, get_test_logger


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    return TestClient(app)


@pytest.fixture
def api_base_url():
    """Base URL for API testing."""
    return "http://localhost:8000"


@pytest.fixture(autouse=True)
def log_test_result(request):
    """Automatically log test results."""
    test_logger = get_test_logger()
    
    # Get test parameters
    test_params = {}
    if hasattr(request, "param"):
        test_params["param"] = str(request.param)
    if hasattr(request, "fixturenames"):
        test_params["fixtures"] = request.fixturenames
    
    # Log test start
    test_name = request.node.name
    test_file = str(request.node.fspath) if hasattr(request.node, 'fspath') else None
    
    yield
    
    # Log test result after execution
    # This will be called after the test completes
    pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results."""
    outcome = yield
    rep = outcome.get_result()
    
    test_logger = get_test_logger()
    test_name = item.name
    test_file = str(item.fspath) if hasattr(item, 'fspath') else None
    
    # Extract parameters from test
    test_params = {}
    if hasattr(item, "callspec"):
        if item.callspec and hasattr(item.callspec, "params"):
            test_params["parametrized"] = item.callspec.params
    
    # Determine status
    if rep.when == "call":
        if rep.outcome == "passed":
            status = TestStatus.PASSED
        elif rep.outcome == "failed":
            status = TestStatus.FAILED
        elif rep.outcome == "skipped":
            status = TestStatus.SKIPPED
        else:
            status = TestStatus.ERROR
        
        # Log the test result
        test_logger.log_test(
            test_name=test_name,
            status=status,
            parameters=test_params,
            result=None,  # Could capture actual result if needed
            error=rep.longrepr if rep.failed else None,
            duration=rep.duration,
            test_file=test_file,
        )
