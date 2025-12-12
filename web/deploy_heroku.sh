#!/bin/bash
# Quick deployment script for Heroku

echo "🚀 Deploying Document Gap Analysis Web App to Heroku"
echo "=================================================="
echo ""

# Check if heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed."
    echo "Install it from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

echo "✓ Heroku CLI found"

# Check if logged in
if ! heroku auth:whoami &> /dev/null; then
    echo ""
    echo "Logging in to Heroku..."
    heroku login
fi

echo "✓ Logged in to Heroku"

# Get app name
echo ""
read -p "Enter your app name (e.g., my-gap-analyzer): " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "❌ App name is required"
    exit 1
fi

# Create Heroku app
echo ""
echo "Creating Heroku app: $APP_NAME"
heroku create $APP_NAME

if [ $? -ne 0 ]; then
    echo "⚠️  App might already exist, continuing..."
fi

# Get API key
echo ""
echo "You need an API key from either:"
echo "  - OpenAI: https://platform.openai.com/api-keys"
echo "  - Anthropic: https://console.anthropic.com/"
echo ""
read -p "Enter your API key: " API_KEY

if [ -z "$API_KEY" ]; then
    echo "❌ API key is required"
    exit 1
fi

# Detect provider
if [[ $API_KEY == sk-ant* ]]; then
    PROVIDER="anthropic"
    echo "Detected: Anthropic API key"
else
    PROVIDER="openai"
    echo "Detected: OpenAI API key"
fi

# Set environment variables
echo ""
echo "Setting environment variables..."
if [ "$PROVIDER" == "openai" ]; then
    heroku config:set OPENAI_API_KEY=$API_KEY --app $APP_NAME
    heroku config:set AI_PROVIDER=openai --app $APP_NAME
else
    heroku config:set ANTHROPIC_API_KEY=$API_KEY --app $APP_NAME
    heroku config:set AI_PROVIDER=anthropic --app $APP_NAME
fi

echo "✓ Environment variables set"

# Check if git is initialized
if [ ! -d .git ]; then
    echo ""
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit"
fi

# Add Heroku remote if not exists
if ! git remote | grep -q heroku; then
    echo "Adding Heroku remote..."
    heroku git:remote --app $APP_NAME
fi

# Deploy
echo ""
echo "Deploying to Heroku..."
echo "This may take a few minutes..."
echo ""

git push heroku main

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "✅ Deployment successful!"
    echo "=================================================="
    echo ""
    echo "Your app is live at:"
    echo "https://$APP_NAME.herokuapp.com"
    echo ""
    echo "Opening in browser..."
    heroku open --app $APP_NAME
    echo ""
    echo "To view logs: heroku logs --tail --app $APP_NAME"
    echo "To restart: heroku restart --app $APP_NAME"
    echo ""
else
    echo ""
    echo "❌ Deployment failed"
    echo "Check the error messages above"
    echo ""
    echo "View logs: heroku logs --tail --app $APP_NAME"
    exit 1
fi
