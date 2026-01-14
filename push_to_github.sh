#!/bin/bash
# Quick script to push NetSec Toolkit to GitHub

set -e

echo "=========================================="
echo "NetSec Toolkit - GitHub Push Script"
echo "=========================================="
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not a git repository. Initializing..."
    git init
    echo "✓ Git repository initialized"
fi

# Check current status
echo "📊 Checking git status..."
git status --short

echo ""
echo "Files to be added:"
echo "  - NetSec-Core (complete)"
echo "  - NetSec-Cloud (with Docker files)"
echo "  - NetSec-Container (with Docker files)"
echo "  - All documentation"
echo "  - All configuration files"
echo ""

# Confirm
read -p "Continue with add/commit/push? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

# Add all files
echo ""
echo "📦 Adding all files..."
git add .

# Show what will be committed
echo ""
echo "📝 Files to be committed:"
git status --short

echo ""
read -p "Commit these changes? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

# Commit
echo ""
echo "💾 Committing changes..."
git commit -m "Complete NetSec Toolkit with Docker files and enhancements

- Add Dockerfile and docker-compose.yml for NetSec-Cloud
- Add Dockerfile and docker-compose.yml for NetSec-Container  
- Enhance LLM integration with local model support (Ollama, LM Studio, vLLM, HuggingFace)
- Add comprehensive test result documentation system
- Update all documentation and examples
- Add .gitignore files for all projects
- Complete project structure for all three projects"

# Check if remote exists
if ! git remote | grep -q origin; then
    echo ""
    echo "⚠️  No remote 'origin' found."
    echo "Please add your GitHub repository:"
    echo "  git remote add origin https://github.com/your-username/netsec-toolkit.git"
    echo "Or:"
    echo "  git remote add origin git@github.com:your-username/netsec-toolkit.git"
    exit 1
fi

# Show remote
echo ""
echo "🔗 Remote repository:"
git remote -v

# Push
echo ""
read -p "Push to GitHub? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled. Run 'git push origin main' when ready."
    exit 1
fi

echo ""
echo "🚀 Pushing to GitHub..."
BRANCH=$(git branch --show-current)
git push -u origin "$BRANCH"

echo ""
echo "✅ Done! Check GitHub to verify all files are uploaded."
echo ""
echo "Next steps:"
echo "  1. Verify files on GitHub"
echo "  2. Set up GitHub Actions (CI/CD)"
echo "  3. Add repository description"
echo "  4. Create initial release"
