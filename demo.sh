#!/bin/bash
# Demo script for Document Gap Analysis Tool

echo "=================================================="
echo "  Document Gap Analysis Tool - Interactive Demo"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to pause
pause() {
    echo ""
    read -p "Press Enter to continue..."
    echo ""
}

# 1. Show tool info
echo -e "${BLUE}Step 1: Check Available Commands${NC}"
echo "Let's see what commands are available:"
echo ""
python3 gap_analyzer.py --help
pause

# 2. Check a document
echo -e "${BLUE}Step 2: Inspect a Document (No API Key Needed)${NC}"
echo "Let's look at the example user document:"
echo ""
python3 gap_analyzer.py info examples/user_document.txt
pause

# 3. Check another document
echo -e "${BLUE}Step 3: Inspect a Reference Document${NC}"
echo "Now let's check one of the reference documents:"
echo ""
python3 gap_analyzer.py info examples/reference_doc1_financial_requirements.txt
pause

# 4. Check setup
echo -e "${BLUE}Step 4: Check Your Setup${NC}"
echo "Let's verify if API keys are configured:"
echo ""
python3 gap_analyzer.py check-setup
echo ""

# Check if API keys are present
if [ -f ".env" ]; then
    if grep -q "OPENAI_API_KEY=sk-" .env || grep -q "ANTHROPIC_API_KEY=sk-ant" .env; then
        echo -e "${GREEN}✓ API keys found! You're ready to run analysis.${NC}"
        pause
        
        # 5. Run analysis
        echo -e "${BLUE}Step 5: Run Gap Analysis${NC}"
        echo "Now let's analyze the documents:"
        echo ""
        echo "Running: python3 gap_analyzer.py analyze \\"
        echo "  examples/user_document.txt \\"
        echo "  examples/reference_doc1_financial_requirements.txt \\"
        echo "  examples/reference_doc2_operational_requirements.txt \\"
        echo "  examples/reference_doc3_governance_requirements.txt"
        echo ""
        
        python3 gap_analyzer.py analyze \
          examples/user_document.txt \
          examples/reference_doc1_financial_requirements.txt \
          examples/reference_doc2_operational_requirements.txt \
          examples/reference_doc3_governance_requirements.txt
        
        pause
        
        # 6. Show report
        echo -e "${BLUE}Step 6: View the Generated Report${NC}"
        echo "Opening the report (first 50 lines):"
        echo ""
        head -50 gap_analysis_report.md
        echo ""
        echo -e "${GREEN}Full report saved to: gap_analysis_report.md${NC}"
        
    else
        echo -e "${YELLOW}⚠ No API keys configured yet.${NC}"
        echo ""
        echo "To run the full analysis, you need to:"
        echo "1. Copy the example config: cp .env.example .env"
        echo "2. Edit .env and add your API key"
        echo "3. Run this demo again"
        echo ""
        echo "Get API keys from:"
        echo "  - OpenAI: https://platform.openai.com/api-keys"
        echo "  - Anthropic: https://console.anthropic.com/"
    fi
else
    echo -e "${YELLOW}⚠ No .env file found.${NC}"
    echo ""
    echo "To run the full analysis, you need to:"
    echo "1. Copy the example config: cp .env.example .env"
    echo "2. Edit .env and add your API key"
    echo "3. Run this demo again"
fi

echo ""
echo "=================================================="
echo "Demo complete!"
echo ""
echo "Next steps:"
echo "  1. Review GETTING_STARTED.md for detailed guide"
echo "  2. Set up your API key if not done"
echo "  3. Try analyzing your own documents"
echo ""
echo "Commands to try:"
echo "  python3 gap_analyzer.py info your_document.pdf"
echo "  python3 gap_analyzer.py analyze your_doc.pdf ref1.pdf ref2.pdf"
echo "=================================================="
