@echo off
REM Run Core, Cloud, and Container test suites in parallel from repo root.
REM Usage: run_all_tests_parallel.bat
cd /d "%~dp0"

start "netsec-core" cmd /c "cd netsec-core && pip install -e .[dev] -q && pytest -v -m "not integration" --tb=short"
start "netsec-cloud" cmd /c "cd netsec-cloud && pip install -e .[dev] -q && pytest -v -m "not integration" --tb=short"
start "netsec-container" cmd /c "cd netsec-container && pip install -e .[dev] -q && pytest -v -m "not integration" --tb=short"

echo Started three test runs in separate windows. Check each window for results.
pause
