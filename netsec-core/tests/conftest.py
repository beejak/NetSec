"""Pytest configuration and fixtures."""

import datetime

import pytest
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from fastapi.testclient import TestClient

from netsec_core.api.main import app
from netsec_core.utils.test_logger import TestStatus, get_test_logger


@pytest.fixture(scope="session")
def synthetic_cert_der():
    """Generate a self-signed DER certificate for offline SSL tests."""
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COMMON_NAME, "example.com"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Test Org"),
        ]
    )
    now = datetime.datetime.utcnow()
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + datetime.timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName("example.com")]),
            critical=False,
        )
        .sign(key, hashes.SHA256(), default_backend())
    )
    return cert.public_bytes(serialization.Encoding.DER)


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    return TestClient(app)


@pytest.fixture
def api_base_url():
    """Base URL for API testing."""
    return "http://localhost:8000"


@pytest.fixture
def cli_runner():
    """Click CliRunner for CLI tests."""
    from click.testing import CliRunner

    return CliRunner()


@pytest.fixture(autouse=True)
def log_test_result(request):
    """Automatically log test results."""
    # Get test parameters
    test_params = {}
    if hasattr(request, "param"):
        test_params["param"] = str(request.param)
    if hasattr(request, "fixturenames"):
        test_params["fixtures"] = request.fixturenames

    # Log test start
    _test_name = request.node.name
    _test_file = str(request.node.fspath) if hasattr(request.node, "fspath") else None

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
    test_file = str(item.fspath) if hasattr(item, "fspath") else None

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
