#!/bin/bash
# Run Core, Cloud, and Container test suites in parallel from repo root.
# Usage: ./run_all_tests_parallel.sh
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "Running NetSec-Core, NetSec-Cloud, NetSec-Container tests in parallel..."
( cd netsec-core && pip install -e ".[dev]" -q && pytest -v -m "not integration" --tb=short ) & p1=$!
( cd netsec-cloud && pip install -e ".[dev]" -q && pytest -v -m "not integration" --tb=short ) & p2=$!
( cd netsec-container && pip install -e ".[dev]" -q && pytest -v -m "not integration" --tb=short ) & p3=$!
wait $p1; r1=$?
wait $p2; r2=$?
wait $p3; r3=$?
[ $r1 -eq 0 ] && [ $r2 -eq 0 ] && [ $r3 -eq 0 ] || exit 1

echo "Done. Check output above for [core], [cloud], [container] results."
