@echo off
REM Run sanitization for all three projects

echo ==========================================
echo Running Sanitization for All Projects
echo ==========================================
echo.

echo [1/3] NetSec-Core...
cd netsec-core
if exist sanitize_and_test.py (
    python sanitize_and_test.py
) else (
    echo Sanitization script not found
)
cd ..

echo.
echo [2/3] NetSec-Cloud...
cd netsec-cloud
if exist sanitize_and_test.py (
    python sanitize_and_test.py
) else (
    echo Sanitization script not found
)
cd ..

echo.
echo [3/3] NetSec-Container...
cd netsec-container
if exist sanitize_and_test.py (
    python sanitize_and_test.py
) else (
    echo Sanitization script not found
)
cd ..

echo.
echo ==========================================
echo All Sanitization Complete
echo ==========================================
pause
