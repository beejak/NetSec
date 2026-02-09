@echo off
REM Stage and commit testing framework changes. You run "git push" manually.
cd /d "%~dp0"
git add -A
git status
git commit -m "Add unified testing framework and update documentation" -m "- Add TESTING_FRAMEWORK_RESEARCH.md and TESTING.md" -m "- Add conftest.py and test_api.py (Cloud); conftest.py (Container)" -m "- Add pytest config and dev deps; pytest markers" -m "- Update RUN_ALL_TESTS, SANITY_AND_TEST_CONFIRMATION, README(s)"
if %ERRORLEVEL% equ 0 (
    echo Commit done. Run: git push origin main
) else (
    echo Commit failed or nothing to commit.
)
pause
