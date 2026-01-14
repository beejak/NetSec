@echo off
REM Quick script to push NetSec Toolkit to GitHub (Windows)

echo ==========================================
echo NetSec Toolkit - GitHub Push Script
echo ==========================================
echo.

REM Check if we're in a git repository
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Not a git repository. Initializing...
    git init
    echo [OK] Git repository initialized
)

REM Check current status
echo [INFO] Checking git status...
git status --short

echo.
echo Files to be added:
echo   - NetSec-Core (complete)
echo   - NetSec-Cloud (with Docker files)
echo   - NetSec-Container (with Docker files)
echo   - All documentation
echo   - All configuration files
echo.

REM Confirm
set /p confirm="Continue with add/commit/push? (y/n): "
if /i not "%confirm%"=="y" (
    echo Cancelled.
    exit /b 1
)

REM Add all files
echo.
echo [INFO] Adding all files...
git add .

REM Show what will be committed
echo.
echo [INFO] Files to be committed:
git status --short

echo.
set /p confirm="Commit these changes? (y/n): "
if /i not "%confirm%"=="y" (
    echo Cancelled.
    exit /b 1
)

REM Commit
echo.
echo [INFO] Committing changes...
git commit -m "Complete NetSec Toolkit with Docker files and enhancements

- Add Dockerfile and docker-compose.yml for NetSec-Cloud
- Add Dockerfile and docker-compose.yml for NetSec-Container
- Enhance LLM integration with local model support
- Add comprehensive test result documentation system
- Update all documentation and examples"

REM Check if remote exists
git remote | findstr /C:"origin" >nul
if errorlevel 1 (
    echo.
    echo [WARNING] No remote 'origin' found.
    echo Please add your GitHub repository:
    echo   git remote add origin https://github.com/your-username/netsec-toolkit.git
    exit /b 1
)

REM Show remote
echo.
echo [INFO] Remote repository:
git remote -v

REM Push
echo.
set /p confirm="Push to GitHub? (y/n): "
if /i not "%confirm%"=="y" (
    echo Cancelled. Run 'git push origin main' when ready.
    exit /b 1
)

echo.
echo [INFO] Pushing to GitHub...
for /f "tokens=*" %%i in ('git branch --show-current') do set BRANCH=%%i
git push -u origin %BRANCH%

echo.
echo [OK] Done! Check GitHub to verify all files are uploaded.
echo.
echo Next steps:
echo   1. Verify files on GitHub
echo   2. Set up GitHub Actions (CI/CD)
echo   3. Add repository description
echo   4. Create initial release
