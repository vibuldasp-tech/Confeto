# Working with Word and PDF Documents

## ✅ Supported Formats

The Document Gap Analysis Tool fully supports:

### User Document (Document A - the one you upload)
- ✅ **PDF** (`.pdf`) - Most common format
- ✅ **Word** (`.docx`) - Microsoft Word documents

### Reference Documents (B, C, D - define requirements)
- ✅ **PDF** (`.pdf`)
- ✅ **Word** (`.docx`)
- ✅ **Text** (`.txt`)
- ✅ **Markdown** (`.md`)

**You can mix formats!** For example:
- User document: PDF
- Reference 1: Word
- Reference 2: PDF
- Reference 3: Text

---

## 📄 PDF Document Support

### What Works
✅ Text-based PDFs (created from Word, exported from apps)
✅ Multi-page PDFs (up to 50+ pages)
✅ PDFs with tables and formatting
✅ PDFs with embedded fonts
✅ Scanned PDFs with embedded text layer (OCR already done)

### PDF Parsing Features
- Uses **pdfplumber** (primary) for best text extraction
- Falls back to **PyPDF2** if pdfplumber fails
- Extracts metadata (page count, author, title)
- Handles multi-column layouts
- Preserves document structure

### Example: Analyze a PDF
```bash
# Single user PDF vs reference PDFs
python3 gap_analyzer.py analyze \
  user_annual_report.pdf \
  financial_requirements.pdf \
  operational_requirements.pdf \
  governance_requirements.pdf

# User PDF vs mixed reference formats
python3 gap_analyzer.py analyze \
  my_proposal.pdf \
  client_rfp.pdf \
  technical_specs.docx \
  requirements.txt
```

### Check PDF Before Analysis
```bash
# Inspect your PDF first to verify it parses correctly
python3 gap_analyzer.py info your_document.pdf
```

**Output:**
```
Document Information

File: your_document.pdf
Type: .pdf
Size: 2,456,789 bytes
Pages: 25
Characters: 45,678
Words: 7,891

Preview (first 200 characters):
Company Annual Report 2024
Executive Summary
This document presents...
```

### PDF Troubleshooting

**Problem: "Failed to parse PDF"**

Solution 1: Check if PDF is password-protected
```bash
# Remove password using tools like:
qpdf --decrypt input.pdf output.pdf
```

Solution 2: Check if it's a scanned image
```bash
# If PDF is just scanned images (no text layer), you need OCR first
# Use tools like Adobe Acrobat or online OCR services
```

Solution 3: Try converting to Word
```bash
# Convert PDF to DOCX first, then analyze
# Use Adobe Acrobat, online converters, or:
# https://www.adobe.com/acrobat/online/pdf-to-word.html
```

Solution 4: Export to text
```bash
# Extract text manually and save as .txt
# Then analyze the text file
```

---

## 📝 Word Document Support

### What Works
✅ Modern Word files (.docx)
✅ Documents with complex formatting
✅ Documents with tables
✅ Documents with headers/footers
✅ Documents with multiple sections
✅ Multi-page documents

### Word Parsing Features
- Uses **python-docx** library
- Extracts all paragraphs
- Preserves document structure
- Extracts metadata (author, title)
- Handles tables (extracts text)
- Paragraph count tracking

### Example: Analyze a Word Document
```bash
# User Word doc vs reference documents
python3 gap_analyzer.py analyze \
  my_proposal.docx \
  client_rfp.pdf \
  technical_requirements.docx \
  checklist.txt

# Multiple Word documents
python3 gap_analyzer.py analyze \
  user_report.docx \
  standard_template.docx \
  requirements_doc.docx
```

### Check Word Document Before Analysis
```bash
# Inspect your Word doc first
python3 gap_analyzer.py info your_document.docx
```

**Output:**
```
Document Information

File: your_document.docx
Type: .docx
Size: 156,789 bytes
Paragraphs: 87
Characters: 12,345
Words: 2,134

Preview (first 200 characters):
Annual Report 2024
Executive Summary
Our company has achieved significant milestones...
```

### Word Troubleshooting

**Problem: "Failed to parse DOCX"**

Solution 1: Check file extension
```bash
# Ensure file is .docx (not .doc)
# .doc files are old format - convert to .docx first
```

Solution 2: Open and re-save
```bash
# Open in Word, then Save As → .docx
# This fixes corrupted files
```

Solution 3: Export to PDF
```bash
# If Word file won't parse, export to PDF
# File → Export → Create PDF
```

---

## 🎯 Real-World Examples

### Example 1: Annual Report Analysis (PDF)

**Scenario:** Company uploads annual report PDF to check against compliance requirements

```bash
python3 gap_analyzer.py analyze \
  CompanyAnnualReport2024.pdf \
  SEC_Filing_Requirements.pdf \
  GAAP_Standards.pdf \
  Corporate_Governance_Guidelines.pdf \
  --output annual_report_gap_analysis.html \
  --format html
```

**Result:**
- Coverage: 68%
- Missing: Cash flow statement, audit committee details
- Partial: Risk assessment (incomplete)
- Report saved as styled HTML

### Example 2: Proposal Review (Word)

**Scenario:** Team submits proposal Word doc to verify it addresses all RFP requirements

```bash
python3 gap_analyzer.py analyze \
  Our_Proposal_v3.docx \
  Client_RFP_Requirements.pdf \
  Technical_Specifications.pdf \
  Project_Deliverables_Checklist.docx
```

**Result:**
- Coverage: 85%
- Missing: Project timeline, risk mitigation plan
- Present: All technical specs, team qualifications
- Action: Add missing sections before submission

### Example 3: Mixed Format Analysis

**Scenario:** Documentation audit with various file types

```bash
python3 gap_analyzer.py analyze \
  API_Documentation.pdf \
  Documentation_Standards.txt \
  API_Requirements.docx \
  Style_Guide.md
```

**Result:**
- Works seamlessly with mixed formats
- Coverage: 72%
- Missing: Authentication examples, error codes
- Action: Enhance documentation

---

## 💡 Best Practices for PDF/Word Documents

### For Best Results:

**PDF Documents:**
1. ✅ Use text-based PDFs (not scanned images)
2. ✅ Ensure text is selectable (you can copy-paste)
3. ✅ Remove password protection before analysis
4. ✅ Keep under 50 pages for faster processing
5. ✅ Use standard fonts (not embedded custom fonts)

**Word Documents:**
1. ✅ Save as .docx (not old .doc format)
2. ✅ Use standard formatting
3. ✅ Avoid excessive images (focus on text)
4. ✅ Keep file size reasonable (<10MB)
5. ✅ Test with `info` command first

**General Tips:**
1. ✅ Test documents with `info` command before analysis
2. ✅ Use clear section headings in documents
3. ✅ Ensure content is in English (best AI results)
4. ✅ Keep documents well-formatted
5. ✅ For large docs (50+ pages), consider splitting

---

## 🔍 Testing Your Documents

### Before running full analysis, test parsing:

**Step 1: Test User Document (A)**
```bash
python3 gap_analyzer.py info user_document.pdf
# or
python3 gap_analyzer.py info user_document.docx
```

**Step 2: Test Reference Documents (B, C, D)**
```bash
python3 gap_analyzer.py info reference1.pdf
python3 gap_analyzer.py info reference2.docx
python3 gap_analyzer.py info reference3.txt
```

**Step 3: If all parse correctly, run analysis**
```bash
python3 gap_analyzer.py analyze \
  user_document.pdf \
  reference1.pdf \
  reference2.docx \
  reference3.txt
```

---

## 📊 Format Comparison

| Feature | PDF | Word | Text | Markdown |
|---------|-----|------|------|----------|
| **User Document** | ✅ Best | ✅ Best | ✅ Works | ✅ Works |
| **Reference Docs** | ✅ Best | ✅ Best | ✅ Best | ✅ Works |
| **Formatting** | Preserved | Preserved | Basic | Basic |
| **Tables** | Extracted | Extracted | Manual | Manual |
| **Page Count** | Yes | Yes | No | No |
| **Metadata** | Rich | Rich | Basic | Basic |
| **File Size** | Medium-Large | Medium | Small | Small |
| **Speed** | Fast | Fast | Fastest | Fastest |

**Recommendation:** Use PDF or Word for user documents and reference documents.

---

## 🚀 Quick Start Commands for PDF/Word

### PDF User Document

```bash
# Basic analysis
python3 gap_analyzer.py analyze \
  my_document.pdf \
  requirements.pdf

# With HTML report
python3 gap_analyzer.py analyze \
  my_document.pdf \
  requirements.pdf \
  --output report.html \
  --format html

# Check PDF first
python3 gap_analyzer.py info my_document.pdf
```

### Word User Document

```bash
# Basic analysis
python3 gap_analyzer.py analyze \
  my_document.docx \
  requirements.docx

# With JSON export
python3 gap_analyzer.py analyze \
  my_document.docx \
  requirements.docx \
  --output data.json \
  --format json

# Check Word doc first
python3 gap_analyzer.py info my_document.docx
```

### Mixed Formats

```bash
# PDF user doc + mixed references
python3 gap_analyzer.py analyze \
  user_doc.pdf \
  ref1.pdf \
  ref2.docx \
  ref3.txt

# Word user doc + mixed references
python3 gap_analyzer.py analyze \
  user_doc.docx \
  ref1.pdf \
  ref2.docx \
  ref3.txt
```

---

## 🔧 Advanced PDF/Word Handling

### For Large PDFs (30+ pages)

```bash
# Use verbose mode to see progress
python3 gap_analyzer.py analyze large_doc.pdf refs/*.pdf --verbose

# Or split into sections and analyze separately
python3 gap_analyzer.py analyze section1.pdf refs/*.pdf
python3 gap_analyzer.py analyze section2.pdf refs/*.pdf
```

### For Complex Word Documents

```bash
# Convert complex Word to PDF first if issues
# File → Export → Create PDF in Word

# Then analyze the PDF
python3 gap_analyzer.py analyze converted_doc.pdf refs/*.pdf
```

### Batch Analysis

```bash
# Analyze multiple user documents against same references
for doc in documents/*.pdf; do
  python3 gap_analyzer.py analyze "$doc" requirements/*.pdf \
    --output "reports/$(basename $doc .pdf)_report.md"
done
```

---

## ⚠️ Common Issues and Solutions

### Issue 1: "Cannot extract text from PDF"

**Causes:**
- Scanned PDF (image-only, no text layer)
- Password-protected PDF
- Corrupted PDF file

**Solutions:**
1. Check if you can select/copy text from PDF
2. Remove password protection
3. Use OCR software to add text layer
4. Convert to Word then back to PDF
5. Export as text file

### Issue 2: "DOCX parsing failed"

**Causes:**
- Old .doc format (not .docx)
- Corrupted file
- Macro-enabled file (.docm)

**Solutions:**
1. Open in Word and Save As .docx
2. Remove macros (save as regular .docx)
3. Export to PDF and analyze PDF instead
4. Copy content to new Word document

### Issue 3: "Poor analysis quality"

**Not a parsing issue - AI interpretation issue**

**Solutions:**
1. Ensure documents are well-formatted
2. Use clear section headings
3. Make reference documents more specific
4. Try GPT-4 model (better than GPT-3.5)
5. Check that content is primarily text (not images)

---

## 📋 Document Preparation Checklist

**Before analyzing your PDF/Word document:**

- [ ] Document is .pdf or .docx format
- [ ] File is not password-protected
- [ ] Text is selectable (for PDFs)
- [ ] File size is reasonable (<20MB)
- [ ] Document has clear structure
- [ ] Content is primarily text
- [ ] Test with `info` command first
- [ ] Have 2-4 reference documents ready
- [ ] Reference documents are specific and clear

---

## 🎯 Summary

### ✅ What Works

**PDF Documents:**
- ✓ Text-based PDFs
- ✓ Multi-page documents
- ✓ Documents with tables
- ✓ Standard formatting
- ✓ Multiple megabytes

**Word Documents:**
- ✓ .docx files
- ✓ Complex formatting
- ✓ Documents with tables
- ✓ Multi-page documents
- ✓ Standard templates

**Best Practice:**
```bash
# 1. Test your document first
python3 gap_analyzer.py info your_document.pdf

# 2. If info works, run analysis
python3 gap_analyzer.py analyze \
  your_document.pdf \
  reference1.pdf \
  reference2.docx \
  reference3.pdf
```

---

## 🚀 Ready to Analyze Your PDF/Word Documents?

**Simple workflow:**

```bash
# Step 1: Check your document
python3 gap_analyzer.py info my_document.pdf

# Step 2: Run analysis
python3 gap_analyzer.py analyze \
  my_document.pdf \
  requirements.pdf \
  standards.docx \
  checklist.txt

# Step 3: Review report
cat gap_analysis_report.md
```

**That's it!** The system handles all PDF/Word parsing automatically.

---

For more help, see:
- **START_HERE.md** - Getting started guide
- **GETTING_STARTED.md** - Detailed walkthrough
- **README.md** - Full documentation
