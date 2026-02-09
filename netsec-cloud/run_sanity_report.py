#!/usr/bin/env python3
"""Run sanity and tests, write report to sanity_report.txt."""
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
REPORT = ROOT / "sanity_report.txt"

def run(cmd, cwd=None):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd or ROOT, timeout=90)
    return r.returncode, r.stdout or "", r.stderr or ""

def main():
    lines = []
    def log(s=""):
        lines.append(s)

    log("=== NetSec-Cloud Sanity & Tests ===")
    log()

    # Imports
    log("1. Imports")
    sys.path.insert(0, str(ROOT / "src"))
    for m in ["netsec_cloud", "netsec_cloud.scanner", "netsec_cloud.providers.aws",
              "netsec_cloud.providers.azure", "netsec_cloud.providers.gcp",
              "netsec_cloud.compliance.mapping", "netsec_cloud.api.main"]:
        try:
            __import__(m)
            log(f"  OK {m}")
        except Exception as e:
            log(f"  FAIL {m}: {e}")
    log()

    # Pytest
    log("2. Pytest")
    code, out, err = run("python -m pytest tests/ -v --tb=short -q", ROOT)
    log(out or "(no stdout)")
    if err:
        log("stderr:", err)
    log(f"  Exit code: {code}")
    log()

    # Run_tests.py
    log("3. run_tests.py")
    code2, out2, err2 = run("python run_tests.py", ROOT)
    log(out2[:2000] if out2 else "(no stdout)")
    log(f"  Exit code: {code2}")
    log()

    summary = "PASS" if (code == 0 and code2 == 0) else "FAIL"
    log(f"=== Summary: {summary} ===")

    REPORT.write_text("\n".join(lines))
    print("Report written to", REPORT)
    return 0 if code == 0 and code2 == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
