# Git Push Instructions

How to commit and push to your remote (e.g. GitHub).

---

## Steps

### 1. Stage and commit

From the **repository root**:

```bash
git add -A
git status
git commit -m "Your short description of changes"
```

Or use the scripts: `commit_and_push.sh` (Linux/macOS) or `commit_and_push.bat` (Windows). You still need to run `git push` yourself.

### 2. Push

```bash
git push origin main
```

Use `master` if that is your default branch. If you use a token or SSH, configure remote as needed (e.g. `git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_ORG/Netsec-Toolkit.git`).

### 3. Verify

Check your repository on GitHub. If CI is enabled (see [CI_AND_BRANCH_PROTECTION.md](CI_AND_BRANCH_PROTECTION.md)), confirm the workflow runs and tests pass.

---

## Replace placeholders

In [SUPPORT_AND_SLA.md](SUPPORT_AND_SLA.md) and [MASTER_INDEX.md](MASTER_INDEX.md), replace `your-org` with your GitHub org or repo path when cloning or linking.
