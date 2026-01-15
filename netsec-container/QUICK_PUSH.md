# Quick Push to GitHub

## Option 1: Use the Script (Recommended)

### On Linux/Mac:
```bash
cd netsec-container
chmod +x push_to_github.sh
./push_to_github.sh
```

### On Windows (PowerShell):
```powershell
cd netsec-container
.\push_to_github.ps1
```

## Option 2: Manual Steps

### 1. Create GitHub Repository First
- Go to: https://github.com/new
- Name: `netsec-container`
- Description: `Lightweight Container Security Scanner with LLM-Powered Remediation`
- **DO NOT** check "Initialize with README"
- Click "Create repository"

### 2. Initialize and Push
```bash
cd netsec-container

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Container security scanner with LLM remediation"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/netsec-container.git

# Push
git branch -M main
git push -u origin main
```

## What Gets Pushed

✅ All source code  
✅ Documentation  
✅ Configuration files  
✅ CI/CD workflows  
❌ Excluded: cache files, reports, venv (via .gitignore)

## After Pushing

1. Visit your repository on GitHub
2. Add topics: `container-security`, `vulnerability-scanner`, `devsecops`
3. Add a LICENSE file (MIT recommended)
4. Enable GitHub Actions (if using CI/CD)
