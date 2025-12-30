#!/bin/bash

# Job Finder Platform - Quick Deploy Script
# This script helps you push your code to GitHub for Render deployment

echo "=============================================="
echo "   Job Finder Platform - Deploy to Render"
echo "=============================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Git not initialized. Initializing now..."
    git init
    echo "✅ Git initialized"
fi

# Check if remote exists
if ! git remote | grep -q origin; then
    echo ""
    echo "⚠️  No GitHub remote found."
    echo "Please enter your GitHub repository URL:"
    echo "Example: https://github.com/dayyalabhanuprakash/job-search-platforms.git"
    read -p "Repository URL: " repo_url
    git remote add origin "$repo_url"
    echo "✅ Remote added: $repo_url"
fi

echo ""
echo "📦 Preparing files for deployment..."

# Add all files
git add .

# Commit
echo ""
read -p "Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Job Finder Platform - Ready for deployment"
fi

git commit -m "$commit_msg"
echo "✅ Changes committed"

# Push to GitHub
echo ""
echo "🚀 Pushing to GitHub..."
git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null

if [ $? -eq 0 ]; then
    echo ""
    echo "=============================================="
    echo "✅ SUCCESS! Code pushed to GitHub"
    echo "=============================================="
    echo ""
    echo "🌐 Next Steps:"
    echo ""
    echo "1. Go to: https://render.com"
    echo "2. Sign in with your GitHub account"
    echo "3. Click 'New +' → 'Web Service'"
    echo "4. Select your repository"
    echo "5. Render will auto-detect settings from render.yaml"
    echo "6. Click 'Create Web Service'"
    echo ""
    echo "⏱️  Deployment takes 2-3 minutes"
    echo "🎉 Your live URL will be: https://[your-service-name].onrender.com"
    echo ""
    echo "📖 Full instructions: See DEPLOYMENT_INSTRUCTIONS.md"
    echo "=============================================="
else
    echo ""
    echo "⚠️  Push failed. Please check:"
    echo "1. GitHub repository exists"
    echo "2. You have permission to push"
    echo "3. Remote URL is correct"
    echo ""
    echo "Run: git remote -v"
    echo "To see your current remote settings"
fi
