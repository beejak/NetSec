#!/bin/bash
# Script to push netsec-container to GitHub

set -e

echo "🚀 Preparing to push netsec-container to GitHub..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
fi

# Add all files
echo "📝 Adding files..."
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit. Repository is up to date."
else
    # Create commit
    echo "💾 Creating commit..."
    git commit -m "Initial commit: Lightweight container security scanner

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
- CI/CD integration"
fi

# Check if remote exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "✅ Remote 'origin' already configured"
    REMOTE_URL=$(git remote get-url origin)
    echo "   Remote URL: $REMOTE_URL"
else
    echo ""
    echo "⚠️  No remote repository configured!"
    echo ""
    echo "Please create a GitHub repository first:"
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: netsec-container"
    echo "3. Description: Lightweight Container Security Scanner"
    echo "4. DO NOT initialize with README"
    echo "5. Click 'Create repository'"
    echo ""
    read -p "Enter your GitHub username: " GITHUB_USER
    read -p "Use SSH? (y/n): " USE_SSH
    
    if [ "$USE_SSH" = "y" ] || [ "$USE_SSH" = "Y" ]; then
        REMOTE_URL="git@github.com:${GITHUB_USER}/netsec-container.git"
    else
        REMOTE_URL="https://github.com/${GITHUB_USER}/netsec-container.git"
    fi
    
    echo "🔗 Adding remote: $REMOTE_URL"
    git remote add origin "$REMOTE_URL"
fi

# Set branch to main
git branch -M main 2>/dev/null || true

# Push to GitHub
echo ""
echo "📤 Pushing to GitHub..."
echo "   This may prompt for GitHub credentials"
echo ""

if git push -u origin main; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    REMOTE_URL=$(git remote get-url origin)
    if [[ $REMOTE_URL == *"github.com"* ]]; then
        REPO_URL=$(echo "$REMOTE_URL" | sed 's/\.git$//' | sed 's/git@github.com:/https:\/\/github.com\//')
        echo "🌐 Repository URL: $REPO_URL"
    fi
else
    echo ""
    echo "❌ Push failed!"
    echo ""
    echo "Common issues:"
    echo "1. Repository doesn't exist on GitHub - create it first"
    echo "2. Authentication failed - check your GitHub credentials"
    echo "3. Network issues - check your internet connection"
    echo ""
    echo "To retry manually:"
    echo "  git push -u origin main"
fi
