# Dependency Audit

Run dependency checks to find known vulnerabilities in Python packages.

## pip audit (Python 3.11+)

```bash
# Install pip-audit (if not present)
pip install pip-audit

# Audit current environment (run from each project venv)
cd netsec-core && pip install -e . && pip-audit
cd netsec-cloud && pip install -e . && pip-audit
cd netsec-container && pip install -e . && pip-audit
```

- **Exit 0**: No known vulnerabilities.
- **Exit 1**: One or more packages have known CVEs; upgrade or patch as suggested.

## Alternative: safety

```bash
pip install safety
safety check
```

Run from the project directory after `pip install -e .` so the active environment is audited.

## CI

To fail CI on known vulnerabilities, add a step to the root or per-project workflow:

```yaml
- name: Dependency audit
  run: pip install pip-audit && pip-audit
```

Use this in addition to Dependabot or Renovate if you use them.
