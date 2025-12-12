"""Report generation for gap analysis results."""

from typing import Optional
from pathlib import Path
import json

from src.gap_analyzer import GapAnalysisReport


class ReportGenerator:
    """Generate various report formats from gap analysis results."""
    
    def generate_markdown(self, report: GapAnalysisReport) -> str:
        """Generate a markdown report."""
        md = f"""# Document Gap Analysis Report

**Generated:** {report.timestamp}

## Overview

- **User Document:** {report.user_document}
- **Reference Documents:** {', '.join(report.reference_documents)}
- **Coverage Score:** {report.coverage_score:.1f}%

## Summary

{report.summary}

---

## Detailed Findings

"""
        
        # Group by status
        present = [g for g in report.gaps if g.status == 'present']
        partial = [g for g in report.gaps if g.status == 'partial']
        absent = [g for g in report.gaps if g.status == 'absent']
        
        if present:
            md += f"\n### ✅ Present ({len(present)})\n\n"
            for gap in present:
                md += f"**{gap.requirement}**\n"
                md += f"- Source: {gap.requirement_source}\n"
                md += f"- Details: {gap.details}\n"
                md += f"- Confidence: {gap.confidence:.0%}\n\n"
        
        if partial:
            md += f"\n### ⚠️ Partially Addressed ({len(partial)})\n\n"
            for gap in partial:
                md += f"**{gap.requirement}**\n"
                md += f"- Source: {gap.requirement_source}\n"
                md += f"- Details: {gap.details}\n"
                md += f"- Confidence: {gap.confidence:.0%}\n\n"
        
        if absent:
            md += f"\n### ❌ Missing ({len(absent)})\n\n"
            for gap in absent:
                md += f"**{gap.requirement}**\n"
                md += f"- Source: {gap.requirement_source}\n"
                md += f"- Details: {gap.details}\n"
                md += f"- Confidence: {gap.confidence:.0%}\n\n"
        
        md += "\n---\n\n"
        md += "## Recommendations\n\n"
        
        if absent:
            md += "The following items should be added to the document:\n\n"
            for i, gap in enumerate(absent, 1):
                md += f"{i}. {gap.requirement}\n"
            md += "\n"
        
        if partial:
            md += "The following items need more detail or clarification:\n\n"
            for i, gap in enumerate(partial, 1):
                md += f"{i}. {gap.requirement}\n"
        
        return md
    
    def generate_html(self, report: GapAnalysisReport) -> str:
        """Generate an HTML report."""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gap Analysis Report - {report.user_document}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .meta {{
            background: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .score {{
            font-size: 2em;
            color: #4CAF50;
            font-weight: bold;
        }}
        .section {{
            margin: 30px 0;
        }}
        .item {{
            background: #fafafa;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #ddd;
            border-radius: 4px;
        }}
        .present {{ border-left-color: #4CAF50; }}
        .partial {{ border-left-color: #FF9800; }}
        .absent {{ border-left-color: #f44336; }}
        .requirement {{
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
        }}
        .details {{
            color: #666;
            font-size: 0.95em;
        }}
        .confidence {{
            display: inline-block;
            padding: 2px 8px;
            background: #e0e0e0;
            border-radius: 3px;
            font-size: 0.85em;
            margin-top: 5px;
        }}
        .badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: bold;
            margin: 5px;
        }}
        .badge-present {{ background: #4CAF50; color: white; }}
        .badge-partial {{ background: #FF9800; color: white; }}
        .badge-absent {{ background: #f44336; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Document Gap Analysis Report</h1>
        
        <div class="meta">
            <p><strong>User Document:</strong> {report.user_document}</p>
            <p><strong>Reference Documents:</strong> {', '.join(report.reference_documents)}</p>
            <p><strong>Generated:</strong> {report.timestamp}</p>
            <p><strong>Coverage Score:</strong> <span class="score">{report.coverage_score:.1f}%</span></p>
        </div>
        
        <div class="section">
            <h2>Summary</h2>
            <pre style="white-space: pre-wrap; background: #f9f9f9; padding: 15px; border-radius: 5px;">{report.summary}</pre>
        </div>
"""
        
        # Group by status
        present = [g for g in report.gaps if g.status == 'present']
        partial = [g for g in report.gaps if g.status == 'partial']
        absent = [g for g in report.gaps if g.status == 'absent']
        
        # Stats badges
        html += f"""
        <div class="section">
            <h2>Statistics</h2>
            <span class="badge badge-present">✓ Present: {len(present)}</span>
            <span class="badge badge-partial">◐ Partial: {len(partial)}</span>
            <span class="badge badge-absent">✗ Absent: {len(absent)}</span>
        </div>
"""
        
        if present:
            html += f"""
        <div class="section">
            <h2>✅ Present ({len(present)})</h2>
"""
            for gap in present:
                html += f"""
            <div class="item present">
                <div class="requirement">{gap.requirement}</div>
                <div class="details"><strong>Source:</strong> {gap.requirement_source}</div>
                <div class="details">{gap.details}</div>
                <span class="confidence">Confidence: {gap.confidence:.0%}</span>
            </div>
"""
            html += "        </div>\n"
        
        if partial:
            html += f"""
        <div class="section">
            <h2>⚠️ Partially Addressed ({len(partial)})</h2>
"""
            for gap in partial:
                html += f"""
            <div class="item partial">
                <div class="requirement">{gap.requirement}</div>
                <div class="details"><strong>Source:</strong> {gap.requirement_source}</div>
                <div class="details">{gap.details}</div>
                <span class="confidence">Confidence: {gap.confidence:.0%}</span>
            </div>
"""
            html += "        </div>\n"
        
        if absent:
            html += f"""
        <div class="section">
            <h2>❌ Missing ({len(absent)})</h2>
"""
            for gap in absent:
                html += f"""
            <div class="item absent">
                <div class="requirement">{gap.requirement}</div>
                <div class="details"><strong>Source:</strong> {gap.requirement_source}</div>
                <div class="details">{gap.details}</div>
                <span class="confidence">Confidence: {gap.confidence:.0%}</span>
            </div>
"""
            html += "        </div>\n"
        
        html += """
    </div>
</body>
</html>
"""
        return html
    
    def save_report(
        self,
        report: GapAnalysisReport,
        output_path: str,
        format: str = 'markdown'
    ):
        """
        Save report to file.
        
        Args:
            report: Gap analysis report
            output_path: Path to save the report
            format: Report format ('markdown', 'html', or 'json')
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'markdown':
            content = self.generate_markdown(report)
        elif format == 'html':
            content = self.generate_html(report)
        elif format == 'json':
            content = report.to_json()
        else:
            raise ValueError(f"Unknown format: {format}")
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
