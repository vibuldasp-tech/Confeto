#!/bin/bash
# Quick Docker deployment script

echo "🐳 Document Gap Analysis Tool - Docker Deployment"
echo "=================================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed."
    echo ""
    echo "Install Docker:"
    echo "  curl -fsSL https://get.docker.com -o get-docker.sh"
    echo "  sudo sh get-docker.sh"
    echo ""
    exit 1
fi

echo "✓ Docker found: $(docker --version)"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed."
    echo ""
    echo "Install Docker Compose:"
    echo "  sudo apt-get install docker-compose-plugin"
    echo ""
    exit 1
fi

echo "✓ Docker Compose found"

# Check if .env file exists
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  No .env file found. Creating one..."
    echo ""
    
    # Prompt for API key
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
        cat > .env << EOF
ANTHROPIC_API_KEY=$API_KEY
AI_PROVIDER=anthropic
EOF
    else
        PROVIDER="openai"
        echo "Detected: OpenAI API key"
        cat > .env << EOF
OPENAI_API_KEY=$API_KEY
AI_PROVIDER=openai
EOF
    fi
    
    echo "✓ Created .env file"
else
    echo "✓ .env file found"
fi

echo ""
echo "Building and starting Docker containers..."
echo "This may take a few minutes on first run..."
echo ""

# Build and start
docker-compose up -d --build

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "✅ Deployment successful!"
    echo "=================================================="
    echo ""
    echo "Your application is running at:"
    echo "  http://localhost:8000"
    echo ""
    echo "Useful commands:"
    echo "  View logs:    docker-compose logs -f"
    echo "  Stop:         docker-compose down"
    echo "  Restart:      docker-compose restart"
    echo "  Status:       docker-compose ps"
    echo ""
    echo "Opening in browser..."
    
    # Wait a moment for the service to be ready
    sleep 3
    
    # Try to open in browser
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:8000
    elif command -v open &> /dev/null; then
        open http://localhost:8000
    else
        echo "Please open http://localhost:8000 in your browser"
    fi
else
    echo ""
    echo "❌ Deployment failed"
    echo "Check the error messages above"
    echo ""
    echo "View logs: docker-compose logs"
    exit 1
fi
