#!/bin/bash
# Push container scanner to existing GitHub repository
# Repository: https://github.com/beejak/NetSec

set -e

echo "🚀 Pushing container scanner to existing repository..."
echo "Repository: https://github.com/beejak/NetSec"
echo ""

# Check if we're in the right directory
if [ ! -d "netsec-container" ]; then
    echo "❌ Error: netsec-container directory not found!"
    echo "Please run this script from the Netsec-Toolkit root directory"
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git remote add origin https://github.com/beejak/NetSec.git
else
    # Check if remote is set correctly
    REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
    if [[ ! "$REMOTE" == *"beejak/NetSec"* ]]; then
        echo "🔗 Setting up remote repository..."
        git remote remove origin 2>/dev/null || true
        git remote add origin https://github.com/beejak/NetSec.git
    else
        echo "✅ Remote repository configured: $REMOTE"
    fi
fi

# Add all changes
echo ""
echo "📝 Adding files..."
git add .

# Check for changes
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit. Repository is up to date."
else
    echo "💾 Creating commit..."
    git commit -m "Add container security scanner implementation

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

Implementation Status: ~95% complete"
fi

# Set branch to main
git branch -M main 2>/dev/null || true

# Push to GitHub
echo ""
echo "📤 Pushing to GitHub..."
echo "   Repository: https://github.com/beejak/NetSec"
echo ""

if git push -u origin main; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🌐 View your repository:"
    echo "   https://github.com/beejak/NetSec"
    echo ""
    echo "📁 Container scanner location:"
    echo "   https://github.com/beejak/NetSec/tree/main/netsec-container"
else
    echo ""
    echo "❌ Push failed!"
    echo ""
    echo "Common issues:"
    echo "1. Authentication required - GitHub may prompt for credentials"
    echo "2. Network issues - check your internet connection"
    echo "3. Permission issues - ensure you have write access to the repo"
    echo ""
    echo "To retry manually:"
    echo "  git push -u origin main"
fi
