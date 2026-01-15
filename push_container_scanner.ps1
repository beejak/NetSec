# Push container scanner to existing GitHub repository
# Repository: https://github.com/beejak/NetSec

Write-Host "🚀 Pushing container scanner to existing repository..." -ForegroundColor Cyan
Write-Host "Repository: https://github.com/beejak/NetSec" -ForegroundColor Gray
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "netsec-container")) {
    Write-Host "❌ Error: netsec-container directory not found!" -ForegroundColor Red
    Write-Host "Please run this script from the Netsec-Toolkit root directory" -ForegroundColor Yellow
    exit 1
}

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "📦 Initializing git repository..." -ForegroundColor Yellow
    git init
    git remote add origin https://github.com/beejak/NetSec.git
} else {
    # Check if remote is set correctly
    $remote = git remote get-url origin 2>&1
    if ($LASTEXITCODE -ne 0 -or $remote -notmatch "beejak/NetSec") {
        Write-Host "🔗 Setting up remote repository..." -ForegroundColor Yellow
        git remote remove origin 2>$null
        git remote add origin https://github.com/beejak/NetSec.git
    } else {
        Write-Host "✅ Remote repository configured: $remote" -ForegroundColor Green
    }
}

# Add all changes
Write-Host ""
Write-Host "📝 Adding files..." -ForegroundColor Yellow
git add .

# Check for changes
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "ℹ️  No changes to commit. Repository is up to date." -ForegroundColor Green
} else {
    Write-Host "💾 Creating commit..." -ForegroundColor Yellow
    $commitMessage = @"
Add container security scanner implementation

Features:
- Vulnerability scanning (Trivy integration + basic fallback)
- Secrets detection with image extraction (Docker/Podman)
- SBOM generation (Syft integration)
- Dockerfile security analysis
- Risk scoring system (0-100)
- LLM-powered remediation (OpenAI/Anthropic)
- PDF/CSV/JSON report generation
- REST API with FastAPI
- Web interface with drag-and-drop
- CLI tool with comprehensive options
- CI/CD integration examples

Implementation Status: ~95% complete
"@
    git commit -m $commitMessage
}

# Set branch to main
git branch -M main 2>$null

# Push to GitHub
Write-Host ""
Write-Host "📤 Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "   Repository: https://github.com/beejak/NetSec" -ForegroundColor Gray
Write-Host ""

if (git push -u origin main) {
    Write-Host ""
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 View your repository:" -ForegroundColor Cyan
    Write-Host "   https://github.com/beejak/NetSec" -ForegroundColor White
    Write-Host ""
    Write-Host "📁 Container scanner location:" -ForegroundColor Cyan
    Write-Host "   https://github.com/beejak/NetSec/tree/main/netsec-container" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "❌ Push failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "1. Authentication required - GitHub may prompt for credentials"
    Write-Host "2. Network issues - check your internet connection"
    Write-Host "3. Permission issues - ensure you have write access to the repo"
    Write-Host ""
    Write-Host "To retry manually:" -ForegroundColor Cyan
    Write-Host "  git push -u origin main" -ForegroundColor White
}
