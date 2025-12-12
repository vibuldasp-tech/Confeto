# Document Gap Analysis Tool

An AI-powered system that performs comprehensive gap analysis by comparing a user's document against multiple reference documents to identify what content is present, absent, or partially addressed.

## Overview

This tool helps you ensure that documents contain all required information by comparing them against reference documents that define expected content. It's particularly useful for:

- **Compliance checking**: Verify documents meet regulatory or organizational requirements
- **Quality assurance**: Ensure reports contain all mandatory sections
- **Content validation**: Check if proposals, reports, or submissions are complete
- **Documentation review**: Identify missing information before submission

## How It Works

1. **User uploads a document** (the document to be analyzed)
2. **Reference documents are provided** (documents that define what should be present)
3. **AI performs gap analysis** by:
   - Extracting and understanding content from all documents
   - Comparing user document against each reference document
   - Identifying present, absent, and partially addressed requirements
4. **Comprehensive report is generated** with:
   - Coverage score
   - Detailed findings for each requirement
   - Actionable recommendations

## Features

- ✅ **Multiple document formats**: PDF, DOCX, TXT, Markdown
- 🤖 **AI-powered analysis**: Uses OpenAI GPT-4 or Anthropic Claude
- 📊 **Comprehensive reporting**: Markdown, HTML, and JSON output formats
- 🎯 **Detailed gap identification**: Present, absent, and partial coverage
- 📈 **Coverage scoring**: Quantitative assessment of completeness
- 🔍 **Source tracking**: Know which reference document each requirement comes from
- 💻 **CLI interface**: Easy to use command-line tool

## Installation

### Prerequisites

- Python 3.8 or higher
- API key for OpenAI or Anthropic (or both)

### Step 1: Clone the repository

```bash
git clone https://github.com/yourusername/document-gap-analyzer.git
cd document-gap-analyzer
```

### Step 2: Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

### Step 4: Configure API keys

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API key(s):

```bash
# Choose your AI provider
AI_PROVIDER=openai  # or 'anthropic'

# OpenAI configuration
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# Anthropic configuration (alternative)
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

### Step 5: Verify setup

```bash
python gap_analyzer.py check-setup
```

## Usage

### Basic Usage

```bash
python gap_analyzer.py analyze <user_document> <reference_doc1> <reference_doc2> [reference_doc3...]
```

### Example with Sample Documents

The repository includes example documents to test the tool:

```bash
python gap_analyzer.py analyze \
  examples/user_document.txt \
  examples/reference_doc1_financial_requirements.txt \
  examples/reference_doc2_operational_requirements.txt \
  examples/reference_doc3_governance_requirements.txt
```

This will generate a gap analysis report showing what's present and missing in the user document.

### Command Options

```bash
Options:
  -o, --output PATH        Output file path (default: gap_analysis_report.md)
  -f, --format [markdown|html|json]  Report format (default: markdown)
  -p, --provider [openai|anthropic]  AI provider to use
  -v, --verbose           Enable verbose logging
  --help                  Show help message
```

### Examples

**Generate HTML report:**

```bash
python gap_analyzer.py analyze user_doc.pdf ref1.pdf ref2.docx \
  --output report.html \
  --format html
```

**Use specific AI provider:**

```bash
python gap_analyzer.py analyze user_doc.pdf ref1.pdf ref2.pdf \
  --provider anthropic
```

**Get document information:**

```bash
python gap_analyzer.py info examples/user_document.txt
```

## Report Format

### Coverage Score

The tool calculates an overall coverage score (0-100%) based on:
- **Present requirements**: 1.0 weight
- **Partial requirements**: 0.5 weight
- **Absent requirements**: 0.0 weight

Each finding is also assigned a confidence score by the AI.

### Report Sections

1. **Overview**: Document names, timestamp, coverage score
2. **Summary**: Quick statistics of present/absent/partial requirements
3. **Detailed Findings**: 
   - ✅ Present: Requirements that are fully addressed
   - ⚠️ Partial: Requirements that are partially addressed
   - ❌ Absent: Missing requirements
4. **Recommendations**: Actionable next steps

### Sample Report Output

```markdown
# Document Gap Analysis Report

**Coverage Score:** 68.5%

## Summary

Total Requirements Analyzed: 25
✓ Present: 15 (60.0%)
✗ Absent: 7 (28.0%)
◐ Partial: 3 (12.0%)

## Detailed Findings

### ✅ Present (15)

**Financial Revenue Data**
- Source: Reference Document 1
- Details: Document includes comprehensive revenue breakdown by segment
- Confidence: 95%

### ❌ Missing (7)

**Balance Sheet Information**
- Source: Reference Document 1
- Details: No balance sheet or asset/liability information found
- Confidence: 90%
```

## Use Cases

### 1. Annual Report Compliance

Ensure your annual report contains all required sections:

```bash
python gap_analyzer.py analyze \
  my_annual_report.pdf \
  financial_requirements.pdf \
  operational_requirements.pdf \
  governance_requirements.pdf
```

### 2. Proposal Verification

Check if your proposal addresses all RFP requirements:

```bash
python gap_analyzer.py analyze \
  our_proposal.docx \
  rfp_requirements.pdf \
  technical_specs.pdf
```

### 3. Documentation Review

Verify technical documentation completeness:

```bash
python gap_analyzer.py analyze \
  api_documentation.md \
  documentation_standards.txt \
  api_requirements.txt
```

### 4. Quality Assurance

Check project deliverables against requirements:

```bash
python gap_analyzer.py analyze \
  project_deliverable.pdf \
  project_requirements.docx \
  quality_checklist.txt
```

## Architecture

### Components

```
┌─────────────────────────────────────────┐
│         CLI Interface (cli.py)          │
│  - Command parsing                      │
│  - User interaction                     │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│    Gap Analyzer (gap_analyzer.py)       │
│  - Orchestrates analysis                │
│  - Calculates coverage                  │
└───┬──────────────────────────────┬──────┘
    │                              │
┌───▼──────────────────┐  ┌────────▼────────────┐
│  Document Parser     │  │   AI Provider       │
│  (document_parser.py)│  │  (ai_provider.py)   │
│  - PDF, DOCX, TXT    │  │  - OpenAI           │
│  - Content extract   │  │  - Anthropic        │
└──────────────────────┘  └─────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│  Report Generator (report_generator.py) │
│  - Markdown, HTML, JSON                 │
└─────────────────────────────────────────┘
```

### Key Modules

1. **document_parser.py**: Handles parsing of multiple document formats
2. **ai_provider.py**: Interfaces with AI services (OpenAI, Anthropic)
3. **gap_analyzer.py**: Core analysis logic and coverage calculation
4. **report_generator.py**: Generates reports in various formats
5. **cli.py**: Command-line interface

## Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_gap_analyzer.py

# Run with verbose output
pytest -v
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AI_PROVIDER` | AI service to use ('openai' or 'anthropic') | `openai` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `OPENAI_MODEL` | OpenAI model name | `gpt-4-turbo-preview` |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `ANTHROPIC_MODEL` | Anthropic model name | `claude-3-sonnet-20240229` |

### Supported Document Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Uses pdfplumber and PyPDF2 |
| Word | `.docx` | Microsoft Word documents |
| Text | `.txt` | Plain text files |
| Markdown | `.md` | Markdown files |

## Best Practices

### For Reference Documents

1. **Be specific**: Clearly state what information is required
2. **Use sections**: Organize requirements into logical sections
3. **Provide examples**: Show what good coverage looks like
4. **Avoid ambiguity**: Use clear, unambiguous language

### For Better Results

1. **Use high-quality documents**: Clear, well-formatted documents yield better results
2. **Multiple references**: Use 2-3 reference documents for comprehensive coverage
3. **Review AI findings**: Always review the AI's assessment for accuracy
4. **Iterative process**: Use the tool multiple times as you improve the document

## Limitations

- **AI interpretation**: Results depend on AI model's understanding
- **Context matters**: Very technical or domain-specific jargon may be challenging
- **No OCR**: Scanned PDFs with images of text are not supported
- **Language**: Best results with English documents
- **Cost**: API calls to OpenAI/Anthropic incur costs

## Troubleshooting

### "API key not found"

Make sure your `.env` file exists and contains valid API keys.

### "Failed to parse PDF"

Try a different PDF reader or convert the PDF to text first. Scanned PDFs need OCR preprocessing.

### "Out of tokens" or rate limit errors

- Reduce document size or split into smaller sections
- Wait a moment and retry
- Check your API usage limits

### Poor analysis quality

- Ensure reference documents are clear and well-structured
- Try a more capable model (e.g., GPT-4 instead of GPT-3.5)
- Verify documents are in supported formats and readable

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

See LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the documentation

## Roadmap

Future enhancements:

- [ ] Support for more document formats (RTF, ODT)
- [ ] OCR support for scanned documents
- [ ] Multi-language support
- [ ] Custom AI model fine-tuning
- [ ] Web interface
- [ ] Batch processing
- [ ] Template library for common document types
- [ ] Integration with document management systems

## Acknowledgments

Built with:
- [OpenAI GPT-4](https://openai.com/)
- [Anthropic Claude](https://www.anthropic.com/)
- [PyPDF2](https://pypdf2.readthedocs.io/)
- [python-docx](https://python-docx.readthedocs.io/)
- [Click](https://click.palletsprojects.com/)
- [Rich](https://rich.readthedocs.io/)

---

**Note**: This tool uses AI for analysis. Always review results and use human judgment for critical decisions.
