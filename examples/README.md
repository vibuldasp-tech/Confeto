# Example Documents

This directory contains sample documents to demonstrate the gap analysis tool.

## Files

### User Document

**`user_document.txt`** - A sample company annual report that will be analyzed.

This document contains:
- Executive summary
- Financial performance (partial information)
- Market expansion details
- Product development information
- Customer base metrics
- Operations overview
- Team information

### Reference Documents

These documents define what SHOULD be present in an annual report:

**`reference_doc1_financial_requirements.txt`** - Financial reporting requirements
- Revenue breakdown
- Profitability metrics
- Balance sheet
- Cash flow
- Financial ratios
- Cost analysis
- Future outlook

**`reference_doc2_operational_requirements.txt`** - Operational reporting requirements
- Production metrics
- Customer metrics
- Market presence
- Product portfolio
- Technology infrastructure
- Logistics and distribution
- Partnerships

**`reference_doc3_governance_requirements.txt`** - Governance and compliance requirements
- Corporate governance structure
- Executive leadership
- Risk management
- Compliance and legal
- Corporate social responsibility
- Human resources
- Stakeholder communications
- Ethics and audit

## Running the Example

From the project root directory, run:

```bash
python gap_analyzer.py analyze \
  examples/user_document.txt \
  examples/reference_doc1_financial_requirements.txt \
  examples/reference_doc2_operational_requirements.txt \
  examples/reference_doc3_governance_requirements.txt
```

This will:
1. Parse all four documents
2. Compare the user document against each of the three reference documents
3. Identify what's present, absent, and partially addressed
4. Generate a detailed gap analysis report

## Expected Results

The analysis should identify:

**Present:**
- Revenue information
- Customer base data
- Market expansion details
- Product development information
- Operations overview
- Team size

**Partially Present:**
- Financial metrics (only basic info)
- Customer metrics (incomplete)

**Absent:**
- Balance sheet information
- Cash flow data
- Financial ratios
- Corporate governance details
- Risk management framework
- Compliance information
- CSR initiatives
- And many more...

The coverage score should be relatively low (30-40%) as the user document is intentionally incomplete to demonstrate the gap analysis functionality.

## Creating Your Own Examples

You can create your own test cases by:

1. Creating a user document with the content you want to analyze
2. Creating one or more reference documents that define requirements
3. Running the analysis tool on your documents

Supported formats: `.txt`, `.md`, `.pdf`, `.docx`
