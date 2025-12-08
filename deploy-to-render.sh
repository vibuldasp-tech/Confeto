#!/bin/bash
# Quick deployment script for Render
# This helps you push to GitHub quickly

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         EQUIS SAR MVP - Deploy to Render (via GitHub)         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

echo ""
echo "📝 Preparing files for deployment..."

# Make sure we're on main branch
git branch -M main 2>/dev/null || git checkout -b main

echo "✅ On main branch"
echo ""

# Add all files
echo "📦 Adding all files..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "ℹ️  No changes to commit"
else
    echo "💾 Committing changes..."
    git commit -m "Deploy EQUIS SAR MVP to Render - $(date +%Y-%m-%d)"
    echo "✅ Changes committed"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "                    NEXT STEPS FOR RENDER                       "
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "1️⃣  CREATE GITHUB REPOSITORY:"
echo "    → Go to: https://github.com/new"
echo "    → Name: equis-sar-mvp"
echo "    → Don't add README or .gitignore"
echo "    → Click 'Create repository'"
echo ""
echo "2️⃣  PUSH TO GITHUB:"
echo "    Run this command (replace YOUR_USERNAME):"
echo ""
echo "    git remote add origin https://github.com/YOUR_USERNAME/equis-sar-mvp.git"
echo "    git push -u origin main"
echo ""
echo "3️⃣  DEPLOY ON RENDER:"
echo "    → Go to: https://render.com"
echo "    → Click 'New +' → 'Web Service'"
echo "    → Connect your GitHub repo"
echo "    → Configure:"
echo "      - Build Command: npm install"
echo "      - Start Command: node server.js"
echo "      - Instance: Free or Starter (\$7/mo)"
echo "    → Click 'Create Web Service'"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📖 Full instructions: See RENDER_DEPLOY.md"
echo "✅ Checklist: See RENDER_CHECKLIST.txt"
echo ""
echo "Good luck! 🚀"
