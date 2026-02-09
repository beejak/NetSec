# CI and Branch Protection

## Root CI (`.github/workflows/ci.yml`)

The repository root workflow runs **three jobs in parallel** (no `needs:` between them):

| Job | Working directory | Steps |
|-----|-------------------|--------|
| **test-core** | netsec-core | checkout, Python 3.11, `pip install -e ".[dev]"`, pytest (exclude integration), ruff (optional) |
| **test-cloud** | netsec-cloud | Same |
| **test-container** | netsec-container | Same |

- **Triggers:** push and pull_request to `main`, `master`, `develop`.
- **Pytest:** `pytest -v -m "not integration" --tb=short` so integration tests are skipped for speed.
- **Lint:** `ruff check src/ tests/ || true` so lint runs but does not fail the job (remove `|| true` to fail on lint errors).

## Enabling branch protection (GitHub)

1. Repo **Settings** → **Branches** → **Add rule** (or edit rule for `main`/`master`).
2. **Branch name pattern:** `main` (or `master`).
3. Enable **Require status checks to pass before merging**.
4. Select status checks: **NetSec-Core**, **NetSec-Cloud**, **NetSec-Container** (these match the job names in the root workflow).
5. Optionally enable **Require branches to be up to date before merging**.
6. Save.

After this, merges to the protected branch will require all three test jobs to pass.

## Per-project CI

Each project also has its own workflow under `netsec-core/.github/workflows/ci.yml`, etc. They can run in addition to the root workflow (e.g. matrix Python versions, coverage upload). The root workflow is the single entry point for “all three projects” in parallel.
