#!/usr/bin/env python3
"""Run Core, Cloud, and Container test suites in parallel from repo root."""
import concurrent.futures
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECTS = [
    ("netsec-core", "core"),
    ("netsec-cloud", "cloud"),
    ("netsec-container", "container"),
]


def run_pytest(project_dir: str, label: str) -> tuple[str, int]:
    """Run pytest in project_dir; return (label, returncode)."""
    work_dir = ROOT / project_dir
    if not work_dir.is_dir():
        return label, -1
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", ".[dev]", "-q"],
            cwd=work_dir,
            capture_output=True,
            timeout=120,
            check=False,
        )
        r = subprocess.run(
            [sys.executable, "-m", "pytest", "-v", "-m", "not integration", "--tb=short"],
            cwd=work_dir,
            capture_output=True,
            timeout=300,
        )
        return label, r.returncode
    except (subprocess.TimeoutExpired, Exception):
        return label, -1


def main() -> int:
    print("Running NetSec-Core, NetSec-Cloud, NetSec-Container tests in parallel...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(run_pytest, d, l): l for d, l in PROJECTS
        }
        results = {}
        for fut in concurrent.futures.as_completed(futures):
            label = futures[fut]
            label, code = fut.result()
            results[label] = code
            status = "PASS" if code == 0 else "FAIL"
            print(f"[{label}] {status} (exit {code})")
    failed = sum(1 for c in results.values() if c != 0)
    print("Done." if failed == 0 else f"{failed} project(s) failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
