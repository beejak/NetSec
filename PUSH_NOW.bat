@echo off
echo ========================================
echo Pushing Container Scanner to GitHub
echo Repository: https://github.com/beejak/NetSec
echo ========================================
echo.

cd /d "%~dp0"

echo [1/5] Checking git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    pause
    exit /b 1
)

echo [2/5] Initializing git repository (if needed)...
if not exist ".git" (
    git init
    git remote add origin https://github.com/beejak/NetSec.git
) else (
    git remote set-url origin https://github.com/beejak/NetSec.git
)

echo [3/5] Adding all files...
git add .

echo [4/5] Committing changes...
git commit -m "Add container security scanner - complete implementation" 2>nul
if errorlevel 1 (
    echo No changes to commit or commit failed
)

echo [5/5] Pushing to GitHub...
git branch -M main 2>nul
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERROR: Push failed. This usually means:
    echo - Authentication is required (GitHub will prompt)
    echo - Network connection issue
    echo - Repository permissions issue
    echo.
    echo Try running manually: git push -u origin main
) else (
    echo.
    echo ========================================
    echo SUCCESS! Code pushed to GitHub!
    echo ========================================
    echo.
    echo View repository: https://github.com/beejak/NetSec
    echo Container scanner: https://github.com/beejak/NetSec/tree/main/netsec-container
)

echo.
pause
