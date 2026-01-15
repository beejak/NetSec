# Force push to GitHub - handles everything
# Run this from Netsec-Toolkit root directory

$ErrorActionPreference = "Stop"

Write-Host "🚀 Pushing to GitHub: https://github.com/beejak/NetSec" -ForegroundColor Cyan
Write-Host ""

# Step 1: Initialize git if needed
if (-not (Test-Path ".git")) {
    Write-Host "📦 Initializing git..." -ForegroundColor Yellow
    git init
}

# Step 2: Set remote
Write-Host "🔗 Configuring remote..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin https://github.com/beejak/NetSec.git

# Step 3: Add all files
Write-Host "📝 Staging files..." -ForegroundColor Yellow
git add .

# Step 4: Commit
Write-Host "💾 Committing..." -ForegroundColor Yellow
$hasChanges = git diff --staged --quiet 2>&1
if ($LASTEXITCODE -ne 0) {
    git commit -m "Add container security scanner - complete implementation

- Vulnerability scanning (Trivy + fallback)
- Secrets detection with image extraction
- SBOM generation
- Dockerfile analysis
- Risk scoring
- LLM remediation
- PDF/CSV/JSON reports
- REST API
- Web interface
- CLI tool"
} else {
    Write-Host "ℹ️  No changes to commit" -ForegroundColor Gray
}

# Step 5: Push
Write-Host "📤 Pushing to GitHub..." -ForegroundColor Yellow
git branch -M main 2>$null
git push -u origin main --force

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ SUCCESS! Pushed to GitHub!" -ForegroundColor Green
    Write-Host "🌐 https://github.com/beejak/NetSec" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "⚠️  Push may require authentication" -ForegroundColor Yellow
    Write-Host "Run manually: git push -u origin main" -ForegroundColor Gray
}
