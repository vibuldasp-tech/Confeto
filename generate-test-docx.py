#!/usr/bin/env python3
"""
Generate a sample SAR document for testing the EQUIS SAR MVP application.
"""

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

def create_test_sar():
    doc = Document()
    
    # Title
    title = doc.add_heading('Suspicious Activity Report (SAR)', level=0)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    # Section 1
    heading1 = doc.add_heading('1. REPORTING FINANCIAL INSTITUTION', level=1)
    doc.add_paragraph('Institution Name: Example National Bank')
    doc.add_paragraph('Address: 123 Financial Plaza')
    doc.add_paragraph('City: New York, State: NY, ZIP: 10001')
    doc.add_paragraph('Contact: John Smith, Compliance Officer')
    doc.add_paragraph('Phone: (555) 123-4567')
    doc.add_paragraph('Email: compliance@examplebank.com')
    
    # Section 2
    heading2 = doc.add_heading('2. SUSPECT INFORMATION', level=1)
    doc.add_paragraph('Subject Name: Jane Doe')
    doc.add_paragraph('Date of Birth: 03/15/1975')
    doc.add_paragraph('SSN: XXX-XX-XXXX')
    doc.add_paragraph('Address: 456 Oak Street, Brooklyn, NY 11201')
    doc.add_paragraph('Phone: (555) 987-6543')
    doc.add_paragraph('Account Number: 1234567890')
    doc.add_paragraph('Account Type: Business Checking')
    
    # Section 3
    heading3 = doc.add_heading('3. SUSPICIOUS ACTIVITY DESCRIPTION', level=1)
    para3 = doc.add_paragraph()
    para3.add_run('Summary of Suspicious Activity:\n').bold = True
    doc.add_paragraph(
        'Over a period of two weeks (November 15-30, 2025), the subject made '
        'multiple large cash deposits totaling $250,000 into a business checking '
        'account. The deposits were structured in amounts just below the $10,000 '
        'reporting threshold, ranging from $8,500 to $9,800 per transaction.'
    )
    
    para3_2 = doc.add_paragraph()
    para3_2.add_run('Pattern of Transactions:\n').bold = True
    doc.add_paragraph('• November 15: Cash deposit of $9,500')
    doc.add_paragraph('• November 17: Cash deposit of $9,800')
    doc.add_paragraph('• November 19: Cash deposit of $8,700')
    doc.add_paragraph('• November 22: Cash deposit of $9,200')
    doc.add_paragraph('• November 24: Cash deposit of $9,600')
    doc.add_paragraph('• November 26: Cash deposit of $8,900')
    doc.add_paragraph('• November 28: Cash deposit of $9,300')
    doc.add_paragraph('• November 30: Cash deposit of $9,000')
    
    para3_3 = doc.add_paragraph()
    para3_3.add_run('Red Flags Identified:\n').bold = True
    doc.add_paragraph(
        '1. Structured deposits appearing designed to avoid Currency Transaction Report (CTR) filing\n'
        '2. Inconsistent with stated business purpose (small retail shop)\n'
        '3. Customer unable to provide credible explanation for source of funds\n'
        '4. Deposits made at multiple branch locations\n'
        '5. Unusual timing - all deposits made close to closing time'
    )
    
    # Section 4
    heading4 = doc.add_heading('4. BACKGROUND AND ACCOUNT HISTORY', level=1)
    doc.add_paragraph('Account Opening Date: January 10, 2023')
    doc.add_paragraph('Stated Business Purpose: Small retail clothing store')
    doc.add_paragraph('Expected Monthly Deposits: $5,000 - $15,000')
    doc.add_paragraph('Average Monthly Balance: $8,000')
    
    para4 = doc.add_paragraph()
    para4.add_run('Previous Activity Pattern:\n').bold = True
    doc.add_paragraph(
        'Prior to November 2025, the account showed consistent activity with typical '
        'retail business transactions. Monthly deposits averaged $12,000, primarily '
        'through check and card payments. Cash deposits were infrequent, typically '
        'under $2,000 per transaction. The recent pattern represents a significant '
        'deviation from established baseline behavior.'
    )
    
    # Section 5
    heading5 = doc.add_heading('5. INVESTIGATION AND ACTIONS TAKEN', level=1)
    para5 = doc.add_paragraph()
    para5.add_run('Internal Review:\n').bold = True
    doc.add_paragraph(
        '• Compliance team reviewed transaction history on December 1, 2025\n'
        '• Branch managers interviewed regarding customer interactions\n'
        '• Cross-referenced with other accounts under same customer or related entities\n'
        '• Reviewed identification documents on file\n'
        '• Checked for previous SAR filings (none found)'
    )
    
    para5_2 = doc.add_paragraph()
    para5_2.add_run('Customer Contact:\n').bold = True
    doc.add_paragraph(
        'Compliance officer contacted customer on December 2, 2025, requesting '
        'explanation for recent deposit activity. Customer claimed the funds came '
        'from "increased holiday sales" but could not provide supporting documentation '
        'such as sales records or receipts. Customer became evasive when asked for '
        'additional information.'
    )
    
    # Section 6
    heading6 = doc.add_heading('6. COMPLIANCE OFFICER REVIEW AND DETERMINATION', level=1)
    doc.add_paragraph('Reviewed By: Sarah Johnson, BSA/AML Compliance Officer')
    doc.add_paragraph('Review Date: December 5, 2025')
    doc.add_paragraph('Title: Vice President, Compliance')
    doc.add_paragraph('Employee ID: EMP-4567')
    
    para6 = doc.add_paragraph()
    para6.add_run('Determination:\n').bold = True
    doc.add_paragraph(
        'Based on the structured nature of the deposits, the inconsistency with the '
        'stated business model, the customer\'s inability to provide adequate '
        'documentation, and the overall pattern of suspicious activity, I have '
        'determined that this activity warrants the filing of a Suspicious Activity '
        'Report (SAR) with FinCEN.'
    )
    
    para6_2 = doc.add_paragraph()
    para6_2.add_run('Actions Taken:\n').bold = True
    doc.add_paragraph(
        '• SAR filed with FinCEN on December 6, 2025\n'
        '• Account flagged for enhanced monitoring\n'
        '• Documentation retained in compliance files\n'
        '• Senior management notified\n'
        '• Legal department consulted regarding potential account closure'
    )
    
    # Section 7
    heading7 = doc.add_heading('7. FINANCIAL DETAILS', level=1)
    doc.add_paragraph('Total Amount of Suspicious Activity: $250,000')
    doc.add_paragraph('Number of Transactions: 8')
    doc.add_paragraph('Date Range: November 15-30, 2025')
    doc.add_paragraph('Type of Activity: Structuring / Suspected Money Laundering')
    doc.add_paragraph('Federal Violation(s): 31 USC 5324 (Structuring)')
    
    # Section 8
    heading8 = doc.add_heading('8. ADDITIONAL INFORMATION', level=1)
    doc.add_paragraph(
        'Law enforcement has not been contacted at this time. This matter is being '
        'handled through the standard SAR filing process. The institution will continue '
        'to monitor the account and will file supplemental SARs if additional suspicious '
        'activity is detected. Customer has not been informed of the SAR filing in '
        'accordance with 31 CFR 103.18(e).'
    )
    
    # Footer
    doc.add_paragraph('\n')
    footer = doc.add_paragraph('This document is confidential and for official use only.')
    footer.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    footer_run = footer.runs[0]
    footer_run.font.size = Pt(9)
    footer_run.font.italic = True
    
    # Save the document
    filename = 'Test_SAR_Document.docx'
    doc.save(filename)
    print(f"Test SAR document created: {filename}")
    print(f"The document contains 8 sections with detailed SAR information.")
    print(f"You can now upload this file to test the EQUIS SAR MVP application.")

if __name__ == '__main__':
    create_test_sar()
