# Document Gap Analysis Workflow

## Visual Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                     USER PREPARES FILES                      │
├─────────────────────────────────────────────────────────────┤
│  • User Document (A) - Document to analyze                  │
│  • Reference Docs (B, C, D) - Define expected content       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   DOCUMENT PARSING                           │
├─────────────────────────────────────────────────────────────┤
│  Parser identifies format and extracts text:                │
│  ✓ PDF  → pdfplumber/PyPDF2                                │
│  ✓ DOCX → python-docx                                       │
│  ✓ TXT  → direct read                                       │
│  ✓ MD   → direct read                                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              AI-POWERED GAP ANALYSIS                         │
├─────────────────────────────────────────────────────────────┤
│  For each reference document (B, C, D):                     │
│                                                              │
│  1. Build comparison prompt                                 │
│  2. Send to AI (OpenAI/Anthropic)                          │
│  3. AI analyzes content                                     │
│  4. Identifies: Present / Partial / Absent                  │
│  5. Assigns confidence scores                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               GAP IDENTIFICATION                             │
├─────────────────────────────────────────────────────────────┤
│  Requirement from Ref Doc B                                 │
│    ├─ Status: Present ✅                                    │
│    ├─ Details: Found in section 2                          │
│    └─ Confidence: 95%                                       │
│                                                              │
│  Requirement from Ref Doc C                                 │
│    ├─ Status: Absent ❌                                     │
│    ├─ Details: Not found anywhere                          │
│    └─ Confidence: 90%                                       │
│                                                              │
│  Requirement from Ref Doc D                                 │
│    ├─ Status: Partial ⚠️                                    │
│    ├─ Details: Mentioned but incomplete                    │
│    └─ Confidence: 80%                                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│            COVERAGE CALCULATION                              │
├─────────────────────────────────────────────────────────────┤
│  Formula:                                                    │
│  Coverage = (Present × 1.0 + Partial × 0.5) / Total × 100  │
│                                                              │
│  Example:                                                    │
│  • 15 Present (15 × 1.0 = 15.0)                            │
│  • 8 Partial  (8 × 0.5 = 4.0)                              │
│  • 7 Absent   (7 × 0.0 = 0.0)                              │
│  • Total: 30 requirements                                   │
│  • Coverage: (15 + 4) / 30 × 100 = 63.3%                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              REPORT GENERATION                               │
├─────────────────────────────────────────────────────────────┤
│  Choose format:                                              │
│  • Markdown (.md) - Human-readable, VCS-friendly           │
│  • HTML (.html)   - Styled, browser-viewable               │
│  • JSON (.json)   - Machine-readable, API-friendly         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 FINAL REPORT                                 │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Coverage Score: 63.3%                                  │ │
│  │                                                         │ │
│  │ ✅ Present (15 items)                                  │ │
│  │   - Financial revenue data                             │ │
│  │   - Customer base metrics                              │ │
│  │   - ...                                                 │ │
│  │                                                         │ │
│  │ ⚠️ Partial (8 items)                                   │ │
│  │   - Customer acquisition metrics                       │ │
│  │   - ...                                                 │ │
│  │                                                         │ │
│  │ ❌ Absent (7 items)                                    │ │
│  │   - Balance sheet information                          │ │
│  │   - Cash flow statements                               │ │
│  │   - ...                                                 │ │
│  │                                                         │ │
│  │ 📋 Recommendations                                      │ │
│  │   1. Add balance sheet data                            │ │
│  │   2. Include cash flow statements                      │ │
│  │   3. ...                                                │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Detailed Process Flow

### Phase 1: Input Processing

```
User Document (A)          Reference Documents (B, C, D)
      │                            │
      └────────────┬───────────────┘
                   │
                   ▼
           Document Parser
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
    Extract    Extract    Extract
     Text     Metadata   Structure
        │          │          │
        └──────────┴──────────┘
                   │
                   ▼
        Parsed Document Objects
```

### Phase 2: AI Analysis

```
User Doc Content + Reference Doc Content
              │
              ▼
     Build AI Prompt
    "Compare these documents..."
              │
              ▼
     Send to AI Provider
    (OpenAI or Anthropic)
              │
              ▼
      AI Processes:
    1. Understand requirements
    2. Search for presence
    3. Assess completeness
    4. Generate findings
              │
              ▼
        JSON Response
    [{requirement, status, 
      details, confidence}]
```

### Phase 3: Report Assembly

```
All Gap Analysis Items
         │
    ┌────┼────┐
    │    │    │
    ▼    ▼    ▼
Present Partial Absent
    │    │    │
    └────┼────┘
         │
         ▼
  Calculate Coverage
         │
         ▼
  Generate Summary
         │
    ┌────┼────┐
    │    │    │
    ▼    ▼    ▼
   MD  HTML  JSON
```

## Example Scenarios

### Scenario 1: Annual Report Review

```
INPUT:
  User Doc:     company_annual_report_2024.pdf
  Reference 1:  sec_filing_requirements.pdf
  Reference 2:  accounting_standards.pdf
  Reference 3:  governance_guidelines.pdf

PROCESS:
  Parse → Analyze → Compare → Report

OUTPUT:
  Coverage: 72%
  Missing: Cash flow statement, audit committee details
  Action: Add missing sections before filing
```

### Scenario 2: Proposal Verification

```
INPUT:
  User Doc:     our_proposal.docx
  Reference 1:  client_rfp.pdf
  Reference 2:  technical_requirements.pdf

PROCESS:
  Parse → Analyze → Compare → Report

OUTPUT:
  Coverage: 85%
  Missing: Timeline details, risk mitigation plan
  Action: Update proposal before submission
```

### Scenario 3: Documentation Audit

```
INPUT:
  User Doc:     api_documentation.md
  Reference 1:  doc_standards.txt
  Reference 2:  api_spec_requirements.md

PROCESS:
  Parse → Analyze → Compare → Report

OUTPUT:
  Coverage: 58%
  Missing: Error codes, rate limits, authentication examples
  Action: Enhance documentation
```

## Status Classification Logic

### ✅ Present (100% coverage)
- Requirement is fully addressed in user document
- All key information is present
- Details are comprehensive
- Example: "Revenue: $50M, Growth: 25%, Breakdown by segment provided"

### ⚠️ Partial (50% coverage)
- Requirement is mentioned but incomplete
- Some information present, but lacking detail
- Needs expansion or clarification
- Example: "Revenue: $50M" (missing breakdown and growth)

### ❌ Absent (0% coverage)
- Requirement not found in user document
- No mention or related content
- Needs to be added
- Example: No balance sheet information anywhere

## AI Prompt Strategy

The system uses a carefully crafted prompt structure:

```
You are performing gap analysis...

REFERENCE DOCUMENT (defines what SHOULD be present):
---
[Reference document content]
---

USER'S DOCUMENT:
---
[User document content]
---

TASK:
Identify:
1. What requirements are PRESENT
2. What requirements are ABSENT  
3. What requirements are PARTIAL

Format as JSON...
```

## Performance Characteristics

| Aspect | Details |
|--------|---------|
| **Speed** | 30-60 seconds per analysis |
| **Accuracy** | ~85-95% (depends on clarity) |
| **Cost** | $0.01-0.03 per analysis |
| **Scalability** | Handles documents up to ~50 pages |

## Integration Points

```
┌─────────────────────────────────────────┐
│     Document Gap Analysis Tool          │
└─────────────────┬───────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
  CMS        CI/CD Pipeline   API
Systems      (Auto-check)    Integration
```

## Typical Usage Pattern

```
Day 1: Initial Analysis
  └─ Run: python3 gap_analyzer.py analyze user.pdf refs/*.pdf
  └─ Review report
  └─ Identify: 35% coverage, 25 missing items

Day 2: Update Document
  └─ Add missing sections
  └─ Enhance partial items
  └─ Re-run: python3 gap_analyzer.py analyze user_v2.pdf refs/*.pdf

Day 3: Final Review
  └─ Coverage improved to 85%
  └─ Only 5 minor items missing
  └─ Document ready for submission
```

## Quality Factors

### High Quality Analysis Results When:
- ✅ Reference documents are clear and specific
- ✅ Requirements are well-structured
- ✅ User document is properly formatted
- ✅ Content is in English
- ✅ Text is extractable (not images)

### Lower Quality Results When:
- ❌ Requirements are vague or ambiguous
- ❌ Documents are poorly formatted
- ❌ Heavy use of domain jargon without context
- ❌ Scanned images without OCR
- ❌ Multiple languages mixed

## Error Handling Flow

```
Start Analysis
     │
     ▼
Parse Documents ──[Fail]──> Error: "Cannot parse PDF"
     │                      → Try different format
     │                      → Check file integrity
    [OK]
     │
     ▼
Check API Key ──[Fail]──> Error: "API key not found"
     │                    → Run: check-setup
     │                    → Configure .env
    [OK]
     │
     ▼
AI Analysis ──[Fail]──> Error: "API error"
     │                  → Check rate limits
     │                  → Verify API key
    [OK]
     │
     ▼
Generate Report ──[Fail]──> Error: "Cannot write file"
     │                      → Check permissions
     │                      → Verify path
    [OK]
     │
     ▼
Success! Report Generated
```

---

## Quick Reference

### Commands Flow

```bash
# 1. Check document (no API key needed)
python3 gap_analyzer.py info document.pdf
    ↓
# 2. Verify setup
python3 gap_analyzer.py check-setup
    ↓
# 3. Run analysis
python3 gap_analyzer.py analyze user.pdf ref1.pdf ref2.pdf
    ↓
# 4. Review report
cat gap_analysis_report.md
```

### Decision Tree

```
Need to analyze documents?
    │
    ├─ No API key yet?
    │   └─> Use 'info' command to inspect documents
    │
    └─ Have API key?
        │
        ├─ First time?
        │   └─> Run example analysis first
        │
        └─ Ready for real analysis?
            │
            ├─ Single reference doc?
            │   └─> Basic analysis
            │
            └─ Multiple reference docs?
                └─> Comprehensive analysis
```

For detailed instructions, see **GETTING_STARTED.md**
