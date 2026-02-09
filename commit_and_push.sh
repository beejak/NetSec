#!/bin/bash
# Stage and commit testing framework changes. You run "git push" manually.
set -e
cd "$(dirname "$0")"
git add -A
git status
git commit -m "Add unified testing framework and update documentation

- Add TESTING_FRAMEWORK_RESEARCH.md and TESTING.md
- Add conftest.py and test_api.py (Cloud); conftest.py (Container)
- Add pytest config and dev deps; pytest markers (Core, Cloud, Container)
- Update RUN_ALL_TESTS, SANITY_AND_TEST_CONFIRMATION, README(s)
- Add GIT_PUSH_INSTRUCTIONS.md"
echo "Commit done. Run: git push origin main"
