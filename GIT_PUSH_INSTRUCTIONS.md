# Git Commit and Push Instructions

This document describes how to commit the **testing framework and documentation updates** and push to your remote (e.g. GitHub).

---

## What Was Added/Changed

### New files
- **TESTING_FRAMEWORK_RESEARCH.md** – Research on testing frameworks and libraries; design choices.
- **TESTING.md** – Unified testing framework: pytest, fixtures, markers, coverage, how to run and add tests.
- **netsec-cloud/tests/conftest.py** – Shared fixtures: `client`, `scanner`, `sample_scan_request`.
- **netsec-cloud/tests/test_api.py** – API tests using `client` fixture (root, health, providers, compliance).
- **netsec-container/tests/conftest.py** – Shared fixtures: `client`, `container_scanner`.

### Updated files
- **netsec-cloud/pyproject.toml** – Dev deps: pytest-cov, pytest-mock, httpx; `[tool.pytest.ini_options]` (testpaths, markers, addopts).
- **netsec-cloud/tests/test_scanner.py** – Uses `scanner` fixture and `@pytest.mark.unit` where appropriate.
- **netsec-container/pyproject.toml** – `[tool.pytest.ini_options]` (testpaths, markers, addopts).
- **netsec-core/pyproject.toml** – Pytest markers added for consistency.
- **RUN_ALL_TESTS.md** – Testing framework reference; NetSec-Container commands; Cloud pytest examples.
- **SANITY_AND_TEST_CONFIRMATION.md** – Section 5: Testing framework summary.
- **README.md** – Links to TESTING.md and RUN_ALL_TESTS.md.
- **netsec-cloud/README.md** – Testing section (pytest, fixtures, coverage).
- **netsec-container/README.md** – Testing section (pytest, fixtures, coverage).

---

## Steps to Commit and Push

### 1. Check status

From the **repository root**:

```bash
git status
```

You should see new and modified files listed.

### 2. Stage all changes

```bash
git add -A
```

Or stage selectively (see "What Was Added/Changed" above for the full list). The scripts `commit_and_push.sh` (Linux/macOS) and `commit_and_push.bat` (Windows) run `git add -A` and `git commit` for you; you still need to run `git push` yourself.

### 3. Commit

```bash
git commit -m "Add unified testing framework and update documentation

- Add TESTING_FRAMEWORK_RESEARCH.md (research and design choices)
- Add TESTING.md (pytest, fixtures, markers, coverage, how to run tests)
- Add conftest.py and test_api.py for NetSec-Cloud; conftest.py for NetSec-Container
- Add pytest config and dev deps (pytest-cov, pytest-mock, httpx) to Cloud
- Add pytest markers (unit, integration, api) to Core, Cloud, Container
- Update RUN_ALL_TESTS.md, SANITY_AND_TEST_CONFIRMATION.md, README(s)
- Add GIT_PUSH_INSTRUCTIONS.md for commit and push steps"
```

### 4. Push to remote

If your remote is named `origin` and the branch is `main`:

```bash
git push origin main
```

If your branch is `master`:

```bash
git push origin master
```

If you use a different remote or branch, replace accordingly. If you use GitHub with a personal access token (PAT), you may need to push via HTTPS with the token as password, or configure SSH.

### 5. (Optional) Push with token (HTTPS)

If GitHub requires authentication and you use a PAT:

```bash
# Set remote URL with token (replace YOUR_TOKEN and your GitHub org/repo)
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_ORG/Netsec-Toolkit.git
git push origin main
```

**Security:** Do not commit the token. Prefer environment variables or credential helper; revoke and rotate the token if it was ever exposed.

---

## One-liner script (commit only; you run push)

You can run the script below from the repo root to stage and commit. **You must run `git push` yourself** (the script does not push).

Save as `commit_testing_framework.sh` (Linux/macOS) or run the commands inside it manually on Windows.

```bash
#!/bin/bash
set -e
git add -A
git status
git commit -m "Add unified testing framework and update documentation

- Add TESTING_FRAMEWORK_RESEARCH.md and TESTING.md
- Add conftest.py and test_api.py (Cloud); conftest.py (Container)
- Add pytest config and dev deps; pytest markers (Core, Cloud, Container)
- Update RUN_ALL_TESTS, SANITY_AND_TEST_CONFIRMATION, README(s)
- Add GIT_PUSH_INSTRUCTIONS.md"
echo "Commit done. Run: git push origin main"
```

---

## After pushing

- Run CI (e.g. GitHub Actions) to confirm tests pass.
- Optionally add a branch protection rule so that pushes require passing tests.
