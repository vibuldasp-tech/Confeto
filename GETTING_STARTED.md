# Getting Started Guide

This guide will walk you through your first document gap analysis in just a few steps.

## ✅ Step 1: Installation Complete!

The core dependencies are already installed. You can verify by running:

```bash
python3 gap_analyzer.py --help
```

You should see the help menu with available commands.

## 📄 Step 2: Explore Your Documents (No API Key Needed)

Before running analysis, you can inspect any document using the `info` command:

```bash
# Check the sample user document
python3 gap_analyzer.py info examples/user_document.txt

# Check a reference document
python3 gap_analyzer.py info examples/reference_doc1_financial_requirements.txt

# Check your own documents
python3 gap_analyzer.py info path/to/your/document.pdf
```

This command shows:
- File type and size
- Page count (for PDFs)
- Word count
- Content preview

**Example output:**
```
Document Information

File: user_document.txt
Type: .txt
Size: 1,313 bytes
Characters: 1,313
Words: 193

Preview (first 200 characters):
Company Annual Report 2024...
```

## 🔑 Step 3: Set Up Your API Key

To perform AI-powered gap analysis, you need an API key from either OpenAI or Anthropic.

### Option A: Using OpenAI (GPT-4)

1. **Get an API key:**
   - Go to https://platform.openai.com/api-keys
   - Sign up or log in
   - Create a new API key
   - Copy the key (starts with `sk-...`)

2. **Configure the tool:**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env file and add:
   AI_PROVIDER=openai
   OPENAI_API_KEY=sk-your-actual-key-here
   OPENAI_MODEL=gpt-4-turbo-preview
   ```

### Option B: Using Anthropic (Claude)

1. **Get an API key:**
   - Go to https://console.anthropic.com/
   - Sign up or log in
   - Create a new API key
   - Copy the key (starts with `sk-ant-...`)

2. **Configure the tool:**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env file and add:
   AI_PROVIDER=anthropic
   ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
   ANTHROPIC_MODEL=claude-3-sonnet-20240229
   ```

### Verify Your Setup

```bash
python3 gap_analyzer.py check-setup
```

You should see:
```
✓ .env file found
✓ OpenAI API key configured
✓ Default AI provider: openai
✓ Setup looks good!
```

## 🚀 Step 4: Run Your First Analysis

Now you're ready to perform gap analysis! Let's start with the example documents:

```bash
python3 gap_analyzer.py analyze \
  examples/user_document.txt \
  examples/reference_doc1_financial_requirements.txt \
  examples/reference_doc2_operational_requirements.txt \
  examples/reference_doc3_governance_requirements.txt
```

### What Happens:

1. **Document Parsing**: All documents are parsed and text is extracted
2. **AI Analysis**: The AI compares the user document against each reference
3. **Gap Identification**: Identifies what's present, partial, or absent
4. **Report Generation**: Creates `gap_analysis_report.md`

### Expected Output:

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
│ Total Requirements │    48 │
│ Present            │    12 │
│ Partial            │     8 │
│ Absent             │    28 │
│ Coverage Score     │ 33.3% │
└────────────────────┴───────┘

✓ Report saved to: gap_analysis_report.md

⚠️  Warning: 28 requirements are missing from the user document
```

## 📊 Step 5: Review Your Report

Open the generated report:

```bash
# View in terminal
cat gap_analysis_report.md

# Or open in your editor
code gap_analysis_report.md
# or
nano gap_analysis_report.md
```

The report includes:

### 1. Overview Section
- User document name
- Reference documents used
- Overall coverage score
- Quick statistics

### 2. Present Requirements ✅
Items that ARE in your document:
```markdown
**Financial Revenue Data**
- Source: Reference Document 1
- Details: Document includes revenue of $50M and 25% growth
- Confidence: 95%
```

### 3. Partial Requirements ⚠️
Items that are PARTIALLY addressed:
```markdown
**Customer Metrics**
- Source: Reference Document 2
- Details: Customer count provided (100,000) but missing CAC, CLV, and retention rates
- Confidence: 80%
```

### 4. Absent Requirements ❌
Items that are MISSING:
```markdown
**Balance Sheet Information**
- Source: Reference Document 1
- Details: No asset, liability, or equity information found
- Confidence: 90%
```

### 5. Recommendations
Actionable list of what to add or improve.

## 🎨 Step 6: Generate Different Report Formats

### HTML Report (Styled, Beautiful)

```bash
python3 gap_analyzer.py analyze \
  examples/user_document.txt \
  examples/reference_doc*.txt \
  --output report.html \
  --format html
```

Then open `report.html` in your browser for a styled, professional report.

### JSON Export (For Automation)

```bash
python3 gap_analyzer.py analyze \
  examples/user_document.txt \
  examples/reference_doc*.txt \
  --output report.json \
  --format json
```

Use this for programmatic access or integration with other tools.

## 📝 Step 7: Analyze Your Own Documents

Now let's analyze YOUR documents!

### Prepare Your Files

1. **User Document**: The document you want to check (A)
2. **Reference Documents**: Documents defining what should be present (B, C, D)

Supported formats:
- PDF (`.pdf`)
- Word (`.docx`)
- Text (`.txt`)
- Markdown (`.md`)

### Run Analysis

```bash
python3 gap_analyzer.py analyze \
  path/to/your/document.pdf \
  path/to/reference1.pdf \
  path/to/reference2.docx \
  path/to/reference3.txt \
  --output my_report.md
```

### Example Use Cases

#### 1. Annual Report Compliance
```bash
python3 gap_analyzer.py analyze \
  my_annual_report_2024.pdf \
  sec_filing_requirements.pdf \
  company_reporting_standards.docx \
  industry_best_practices.pdf
```

#### 2. Proposal Review
```bash
python3 gap_analyzer.py analyze \
  our_proposal.docx \
  client_rfp_requirements.pdf \
  technical_specifications.pdf
```

#### 3. Documentation Audit
```bash
python3 gap_analyzer.py analyze \
  api_documentation.md \
  documentation_standards.txt \
  api_requirements_checklist.md
```

## 💡 Pro Tips

### 1. Check Documents First
Always run `info` on your documents first to verify they parse correctly:
```bash
python3 gap_analyzer.py info your_document.pdf
```

### 2. Use Clear Reference Documents
For best results, reference documents should:
- ✅ Clearly list requirements or expected content
- ✅ Use section headings
- ✅ Be specific about what's needed
- ❌ Avoid vague language

### 3. Multiple Reference Documents
Use 2-4 reference documents for comprehensive coverage:
```bash
python3 gap_analyzer.py analyze user.pdf ref1.pdf ref2.pdf ref3.pdf ref4.pdf
```

### 4. Verbose Mode for Debugging
```bash
python3 gap_analyzer.py analyze user.pdf ref.pdf --verbose
```

### 5. Iterate and Improve
1. Run initial analysis
2. Review gaps
3. Update your document
4. Re-run analysis to verify improvements

## 🔧 Advanced Usage

### Custom Output Path

```bash
python3 gap_analyzer.py analyze user.pdf ref.pdf \
  --output reports/analysis_2024_12_12.md
```

### Switch AI Providers

```bash
# Use Anthropic instead of OpenAI
python3 gap_analyzer.py analyze user.pdf ref.pdf \
  --provider anthropic
```

### Combine Multiple Options

```bash
python3 gap_analyzer.py analyze \
  my_document.pdf \
  requirement1.pdf \
  requirement2.docx \
  requirement3.txt \
  --output detailed_analysis.html \
  --format html \
  --provider openai \
  --verbose
```

## 📋 Quick Reference Commands

```bash
# View help
python3 gap_analyzer.py --help
python3 gap_analyzer.py analyze --help

# Check setup
python3 gap_analyzer.py check-setup

# Document info (no API key needed)
python3 gap_analyzer.py info document.pdf

# Basic analysis
python3 gap_analyzer.py analyze user.pdf ref1.pdf ref2.pdf

# HTML report
python3 gap_analyzer.py analyze user.pdf ref.pdf -o report.html -f html

# JSON export
python3 gap_analyzer.py analyze user.pdf ref.pdf -o data.json -f json

# With specific provider
python3 gap_analyzer.py analyze user.pdf ref.pdf -p anthropic

# Verbose mode
python3 gap_analyzer.py analyze user.pdf ref.pdf -v
```

## ⚠️ Troubleshooting

### "ModuleNotFoundError: No module named 'XXX'"

Install missing dependencies:
```bash
pip3 install -r requirements.txt
```

### "API key not found"

1. Check `.env` file exists
2. Verify API key is correct
3. Make sure no extra spaces in `.env`
4. Run `python3 gap_analyzer.py check-setup`

### "Failed to parse PDF"

- Ensure PDF is not password-protected
- Try with a different PDF
- Check if PDF is text-based (not a scanned image)

### "Rate limit exceeded"

- Wait 1 minute and try again
- Check your API usage limits
- Consider splitting large documents

### Poor Analysis Quality

- Make sure reference documents are clear
- Use more specific requirements
- Try GPT-4 model (better than GPT-3.5)
- Ensure documents are in English (best results)

## 💰 Cost Considerations

### OpenAI Pricing (Approximate)
- GPT-4 Turbo: ~$0.01-0.03 per analysis
- Depends on document length
- Check: https://openai.com/pricing

### Anthropic Pricing (Approximate)
- Claude 3 Sonnet: ~$0.01-0.03 per analysis
- Depends on document length
- Check: https://www.anthropic.com/pricing

**Tip**: Start with shorter documents to test, then scale up.

## 🎯 Next Steps

1. ✅ Run the example analysis (Step 4)
2. 📊 Review the generated report (Step 5)
3. 📝 Prepare your own documents
4. 🚀 Analyze your documents (Step 7)
5. 🔄 Iterate based on findings

## 📚 Additional Resources

- **Full Documentation**: `README.md`
- **Quick Start**: `QUICKSTART.md`
- **Project Structure**: `PROJECT_STRUCTURE.md`
- **Contributing**: `CONTRIBUTING.md`
- **Examples**: `examples/README.md`

## 🆘 Need Help?

- Check the troubleshooting section above
- Review example documents in `examples/`
- Run commands with `--help` flag
- Check `.env.example` for configuration reference

---

## ✨ You're All Set!

The tool is ready to use. Start with the example:

```bash
python3 gap_analyzer.py analyze \
  examples/user_document.txt \
  examples/reference_doc*.txt
```

Then move on to analyzing your own documents!

**Happy analyzing! 🎉**
