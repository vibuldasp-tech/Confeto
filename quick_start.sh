#!/bin/bash
# Quick start script for Document Gap Analysis Tool

echo "🚀 Document Gap Analysis Tool - Quick Start"
echo "==========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No .env file found"
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "📝 Please edit .env and add your API keys:"
    echo "   - OPENAI_API_KEY or ANTHROPIC_API_KEY"
    echo ""
    read -p "Press Enter to continue..."
fi

# Run setup check
echo ""
echo "Running setup check..."
python gap_analyzer.py check-setup

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the example analysis:"
echo "  make example"
echo ""
echo "Or manually:"
echo "  python gap_analyzer.py analyze examples/user_document.txt examples/reference_doc*.txt"
echo ""
echo "For help:"
echo "  python gap_analyzer.py --help"
echo ""
