# PowerShell script to push netsec-container to GitHub

Write-Host "🚀 Preparing to push netsec-container to GitHub..." -ForegroundColor Cyan

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "📦 Initializing git repository..." -ForegroundColor Yellow
    git init
}

# Add all files
Write-Host "📝 Adding files..." -ForegroundColor Yellow
git add .

# Check if there are changes to commit
$staged = git diff --staged --quiet 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "ℹ️  No changes to commit. Repository is up to date." -ForegroundColor Green
} else {
    # Create commit
    Write-Host "💾 Creating commit..." -ForegroundColor Yellow
    $commitMessage = @"
Initial commit: Lightweight container security scanner

Features:
- Vulnerability scanning (Trivy + basic fallback)
- Secrets detection with image extraction
- SBOM generation (Syft)
- Dockerfile analysis
- Risk scoring system
- LLM-powered remediation
- PDF/CSV/JSON reports
- REST API with FastAPI
- Web interface with drag-and-drop
- CLI tool
- CI/CD integration
"@
    git commit -m $commitMessage
}

# Check if remote exists
try {
    $remoteUrl = git remote get-url origin 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Remote 'origin' already configured" -ForegroundColor Green
        Write-Host "   Remote URL: $remoteUrl" -ForegroundColor Gray
    }
} catch {
    Write-Host ""
    Write-Host "⚠️  No remote repository configured!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please create a GitHub repository first:" -ForegroundColor Cyan
    Write-Host "1. Go to https://github.com/new"
    Write-Host "2. Repository name: netsec-container"
    Write-Host "3. Description: Lightweight Container Security Scanner"
    Write-Host "4. DO NOT initialize with README"
    Write-Host "5. Click 'Create repository'"
    Write-Host ""
    
    $githubUser = Read-Host "Enter your GitHub username"
    $useSSH = Read-Host "Use SSH? (y/n)"
    
    if ($useSSH -eq "y" -or $useSSH -eq "Y") {
        $remoteUrl = "git@github.com:${githubUser}/netsec-container.git"
    } else {
        $remoteUrl = "https://github.com/${githubUser}/netsec-container.git"
    }
    
    Write-Host "🔗 Adding remote: $remoteUrl" -ForegroundColor Yellow
    git remote add origin $remoteUrl
}

# Set branch to main
git branch -M main 2>$null

# Push to GitHub
Write-Host ""
Write-Host "📤 Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "   This may prompt for GitHub credentials" -ForegroundColor Gray
Write-Host ""

try {
    git push -u origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
        Write-Host ""
        $repoUrl = $remoteUrl -replace '\.git$', '' -replace 'git@github.com:', 'https://github.com/'
        Write-Host "🌐 Repository URL: $repoUrl" -ForegroundColor Cyan
    }
} catch {
    Write-Host ""
    Write-Host "❌ Push failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "1. Repository doesn't exist on GitHub - create it first"
    Write-Host "2. Authentication failed - check your GitHub credentials"
    Write-Host "3. Network issues - check your internet connection"
    Write-Host ""
    Write-Host "To retry manually:" -ForegroundColor Cyan
    Write-Host "  git push -u origin main"
}
