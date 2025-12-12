# Quick Start Guide

Get up and running with the Document Gap Analysis Tool in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- An API key for OpenAI or Anthropic

## Installation

### Option 1: Automated Setup (Linux/Mac)

```bash
# Clone the repository
git clone https://github.com/yourusername/document-gap-analyzer.git
cd document-gap-analyzer

# Run quick start script
./quick_start.sh
```

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/document-gap-analyzer.git
cd document-gap-analyzer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

## Configuration

Edit `.env` and add your API key:

```bash
# For OpenAI
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here

# OR for Anthropic
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

## Verify Setup

```bash
python gap_analyzer.py check-setup
```

You should see:
```
✓ .env file found
✓ OpenAI API key configured
✓ Default AI provider: openai
✓ Setup looks good!
```

## Run Your First Analysis

### Using Example Documents

```bash
python gap_analyzer.py analyze \
  examples/user_document.txt \
  examples/reference_doc1_financial_requirements.txt \
  examples/reference_doc2_operational_requirements.txt \
  examples/reference_doc3_governance_requirements.txt
```

Or simply:

```bash
make example
```

### Output

The tool will:
1. Parse all documents
2. Perform AI-powered gap analysis
3. Generate a report: `gap_analysis_report.md`

Expected output:
```
Document Gap Analysis Tool

User Document: user_document.txt
Reference Documents:
  1. reference_doc1_financial_requirements.txt
  2. reference_doc2_operational_requirements.txt
  3. reference_doc3_governance_requirements.txt

✓ Using AI provider: OpenAIProvider

Analyzing documents... ✓ Analysis complete

Analysis Complete!

┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Metric             ┃ Value ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ Total Requirements │    45 │
│ Present            │    12 │
│ Partial            │     8 │
│ Absent             │    25 │
│ Coverage Score     │ 35.6% │
└────────────────────┴───────┘

✓ Report saved to: gap_analysis_report.md

⚠️  Warning: 25 requirements are missing from the user document
```

## Analyze Your Own Documents

```bash
python gap_analyzer.py analyze \
  path/to/your/document.pdf \
  path/to/reference1.pdf \
  path/to/reference2.docx
```

### Generate HTML Report

```bash
python gap_analyzer.py analyze your_doc.pdf ref1.pdf ref2.pdf \
  --output report.html \
  --format html
```

### Generate JSON Report

```bash
python gap_analyzer.py analyze your_doc.pdf ref1.pdf ref2.pdf \
  --output report.json \
  --format json
```

## Understanding the Report

The generated report includes:

### 1. Coverage Score (0-100%)
Overall completeness of your document

### 2. Present Items ✅
Requirements that are fully addressed in your document

Example:
```
**Financial Revenue Data**
- Source: Reference Document 1
- Details: Document includes comprehensive revenue breakdown
- Confidence: 95%
```

### 3. Partial Items ⚠️
Requirements that are partially addressed

Example:
```
**Customer Metrics**
- Source: Reference Document 2
- Details: Customer count provided but missing CAC and CLV
- Confidence: 80%
```

### 4. Absent Items ❌
Requirements that are missing

Example:
```
**Balance Sheet Information**
- Source: Reference Document 1
- Details: No balance sheet or asset/liability information found
- Confidence: 90%
```

### 5. Recommendations
Actionable next steps to improve your document

## Common Use Cases

### 1. Compliance Check
```bash
python gap_analyzer.py analyze \
  my_annual_report.pdf \
  sec_requirements.pdf \
  industry_standards.pdf
```

### 2. Proposal Verification
```bash
python gap_analyzer.py analyze \
  our_proposal.docx \
  rfp_requirements.pdf
```

### 3. Documentation Review
```bash
python gap_analyzer.py analyze \
  api_docs.md \
  doc_standards.txt \
  api_requirements.md
```

## CLI Commands

### Main Commands

```bash
# Analyze documents
gap-analyzer analyze <user_doc> <ref_doc1> [ref_doc2...]

# Check setup
gap-analyzer check-setup

# Get document info
gap-analyzer info <document_path>

# Show help
gap-analyzer --help
```

### Options

```
-o, --output PATH       Output file path
-f, --format FORMAT     Report format (markdown/html/json)
-p, --provider PROVIDER AI provider (openai/anthropic)
-v, --verbose          Enable verbose logging
```

## Supported Document Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Most PDFs supported (not scanned images) |
| Word | `.docx` | Microsoft Word documents |
| Text | `.txt` | Plain text files |
| Markdown | `.md` | Markdown files |

## Troubleshooting

### "API key not found"
- Check that `.env` file exists
- Verify your API key is correct
- Make sure you've set `AI_PROVIDER` to match your key

### "Failed to parse PDF"
- Ensure PDF is not password-protected
- Try converting to text first
- Some scanned PDFs need OCR (not supported yet)

### "Rate limit exceeded"
- Wait a moment and try again
- Consider using a different AI provider
- Split large documents into smaller sections

## Next Steps

1. ✅ Run the example analysis
2. 📄 Prepare your own documents
3. 🔍 Analyze your documents
4. 📊 Review the generated report
5. ✏️ Update your document based on findings
6. 🔄 Re-analyze to verify improvements

## Tips for Best Results

### For Reference Documents
- Be specific about requirements
- Use clear section headings
- List concrete items to check
- Avoid ambiguous language

### For User Documents
- Use clear formatting
- Include relevant section headers
- Ensure text is extractable (not images)
- Use standard document formats

## Getting Help

```bash
# Show all available commands
python gap_analyzer.py --help

# Show help for specific command
python gap_analyzer.py analyze --help

# Check document info
python gap_analyzer.py info your_document.pdf
```

## Additional Resources

- **Full Documentation**: See `README.md`
- **Examples**: Check `examples/` directory
- **Contributing**: See `CONTRIBUTING.md`
- **Project Structure**: See `PROJECT_STRUCTURE.md`

## Questions?

- Check the [README.md](README.md) for detailed documentation
- Review example documents in `examples/`
- Open an issue on GitHub

---

**Ready to analyze?** Run `make example` to see it in action!
