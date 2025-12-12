"""Gap analysis engine for document comparison."""

import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from src.document_parser import DocumentParser
from src.ai_provider import AIProvider, get_ai_provider

logger = logging.getLogger(__name__)


@dataclass
class GapAnalysisItem:
    """Represents a single gap analysis finding."""
    requirement_source: str  # Which reference document this came from
    requirement: str  # What is required
    status: str  # 'present', 'absent', 'partial'
    details: str  # Additional context
    confidence: float  # Confidence score (0-1)


@dataclass
class GapAnalysisReport:
    """Complete gap analysis report."""
    user_document: str
    reference_documents: List[str]
    timestamp: str
    summary: str
    gaps: List[GapAnalysisItem]
    coverage_score: float  # Overall coverage percentage
    
    def to_dict(self) -> Dict:
        """Convert report to dictionary."""
        return {
            'user_document': self.user_document,
            'reference_documents': self.reference_documents,
            'timestamp': self.timestamp,
            'summary': self.summary,
            'gaps': [asdict(gap) for gap in self.gaps],
            'coverage_score': self.coverage_score
        }
    
    def to_json(self) -> str:
        """Convert report to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class GapAnalyzer:
    """Performs gap analysis on documents using AI."""
    
    def __init__(self, ai_provider: Optional[AIProvider] = None):
        """
        Initialize the gap analyzer.
        
        Args:
            ai_provider: AI provider instance (defaults to configured provider)
        """
        self.parser = DocumentParser()
        self.ai_provider = ai_provider or get_ai_provider()
    
    def analyze(
        self,
        user_document_path: str,
        reference_document_paths: List[str]
    ) -> GapAnalysisReport:
        """
        Perform gap analysis on user document against reference documents.
        
        Args:
            user_document_path: Path to user's document
            reference_document_paths: List of paths to reference documents
            
        Returns:
            GapAnalysisReport with detailed findings
        """
        logger.info(f"Starting gap analysis for {user_document_path}")
        
        # Parse all documents
        user_doc = self.parser.parse(user_document_path)
        reference_docs = []
        
        for ref_path in reference_document_paths:
            try:
                ref_doc = self.parser.parse(ref_path)
                reference_docs.append(ref_doc)
            except Exception as e:
                logger.error(f"Failed to parse reference document {ref_path}: {e}")
                raise
        
        # Perform gap analysis
        gaps = []
        
        for i, ref_doc in enumerate(reference_docs, 1):
            logger.info(f"Analyzing against reference document {i}/{len(reference_docs)}")
            doc_gaps = self._analyze_against_reference(
                user_doc,
                ref_doc,
                f"Reference Document {i}"
            )
            gaps.extend(doc_gaps)
        
        # Generate summary
        summary = self._generate_summary(user_doc, reference_docs, gaps)
        
        # Calculate coverage score
        coverage_score = self._calculate_coverage(gaps)
        
        return GapAnalysisReport(
            user_document=user_doc['file_name'],
            reference_documents=[doc['file_name'] for doc in reference_docs],
            timestamp=datetime.now().isoformat(),
            summary=summary,
            gaps=gaps,
            coverage_score=coverage_score
        )
    
    def _analyze_against_reference(
        self,
        user_doc: Dict,
        reference_doc: Dict,
        source_name: str
    ) -> List[GapAnalysisItem]:
        """
        Analyze user document against a single reference document.
        
        Args:
            user_doc: Parsed user document
            reference_doc: Parsed reference document
            source_name: Name/identifier of the reference document
            
        Returns:
            List of gap analysis items
        """
        prompt = self._build_analysis_prompt(
            user_doc['content'],
            reference_doc['content'],
            source_name
        )
        
        try:
            response = self.ai_provider.analyze(prompt, max_tokens=4000)
            gaps = self._parse_ai_response(response, source_name)
            return gaps
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            raise
    
    def _build_analysis_prompt(
        self,
        user_content: str,
        reference_content: str,
        source_name: str
    ) -> str:
        """Build the prompt for AI analysis."""
        return f"""You are performing a gap analysis to identify what content is present and absent in a user's document compared to a reference document.

REFERENCE DOCUMENT ({source_name}):
This document defines what SHOULD be present in the user's document.
---
{reference_content}
---

USER'S DOCUMENT:
---
{user_content}
---

TASK:
Analyze the user's document and identify:
1. What requirements from the reference document are PRESENT in the user's document
2. What requirements are ABSENT (missing) from the user's document
3. What requirements are PARTIALLY addressed

For each requirement, provide:
- The specific requirement or content item expected
- Status: "present", "absent", or "partial"
- Details explaining your assessment
- Confidence score (0.0 to 1.0)

Format your response as a JSON array of objects with this structure:
[
  {{
    "requirement": "Description of the requirement",
    "status": "present|absent|partial",
    "details": "Explanation of your finding",
    "confidence": 0.95
  }}
]

Be thorough and specific. Focus on substantive content rather than formatting.
Return ONLY the JSON array, no other text."""
    
    def _parse_ai_response(
        self,
        response: str,
        source_name: str
    ) -> List[GapAnalysisItem]:
        """Parse AI response into gap analysis items."""
        try:
            # Extract JSON from response (in case AI added extra text)
            response = response.strip()
            if not response.startswith('['):
                # Try to find JSON array in response
                start = response.find('[')
                end = response.rfind(']') + 1
                if start >= 0 and end > start:
                    response = response[start:end]
            
            items = json.loads(response)
            
            gaps = []
            for item in items:
                gap = GapAnalysisItem(
                    requirement_source=source_name,
                    requirement=item.get('requirement', ''),
                    status=item.get('status', 'unknown'),
                    details=item.get('details', ''),
                    confidence=float(item.get('confidence', 0.5))
                )
                gaps.append(gap)
            
            return gaps
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            logger.debug(f"Response was: {response}")
            # Return empty list rather than failing completely
            return []
    
    def _generate_summary(
        self,
        user_doc: Dict,
        reference_docs: List[Dict],
        gaps: List[GapAnalysisItem]
    ) -> str:
        """Generate an executive summary of the gap analysis."""
        total_items = len(gaps)
        present = len([g for g in gaps if g.status == 'present'])
        absent = len([g for g in gaps if g.status == 'absent'])
        partial = len([g for g in gaps if g.status == 'partial'])
        
        summary = f"""Gap Analysis Summary:

User Document: {user_doc['file_name']}
Reference Documents: {', '.join([doc['file_name'] for doc in reference_docs])}

Total Requirements Analyzed: {total_items}
✓ Present: {present} ({present/total_items*100:.1f}%)
✗ Absent: {absent} ({absent/total_items*100:.1f}%)
◐ Partial: {partial} ({partial/total_items*100:.1f}%)

The user's document covers {present + partial*0.5:.0f} out of {total_items} requirements.
"""
        
        if absent > 0:
            summary += f"\n⚠️  {absent} requirements are missing and need to be addressed."
        
        return summary
    
    def _calculate_coverage(self, gaps: List[GapAnalysisItem]) -> float:
        """
        Calculate overall coverage score.
        
        Present = 1.0, Partial = 0.5, Absent = 0.0
        Weighted by confidence.
        """
        if not gaps:
            return 0.0
        
        total_score = 0.0
        total_weight = 0.0
        
        for gap in gaps:
            if gap.status == 'present':
                score = 1.0
            elif gap.status == 'partial':
                score = 0.5
            else:  # absent
                score = 0.0
            
            total_score += score * gap.confidence
            total_weight += gap.confidence
        
        return (total_score / total_weight * 100) if total_weight > 0 else 0.0
