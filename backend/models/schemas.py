"""
Pydantic models for API request/response schemas
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class SessionResponse(BaseModel):
    session_id: str
    status: str
    message: str


class ParseResponse(BaseModel):
    status: str
    sections_count: int
    file_type: str


class Suggestion(BaseModel):
    id: str
    type: str  # "insertion", "deletion", "replacement"
    position: int
    original_text: Optional[str] = None
    suggested_text: str
    rationale: str
    equis_clause: Optional[str] = None
    equis_clause_number: Optional[str] = None
    confidence: float
    accepted: Optional[bool] = None


class EvidenceLink(BaseModel):
    file_id: str
    filename: str
    page: Optional[int] = None
    paragraph: Optional[str] = None
    excerpt: str
    confidence: float


class Section(BaseModel):
    id: str
    number: str
    title: str
    level: int
    content: str
    suggestions: List[Suggestion]
    evidence_links: List[EvidenceLink]
    coverage_score: float
    equis_criteria: List[str]


class MappingResponse(BaseModel):
    section_id: str
    equis_criteria: List[str]
    coverage_score: float
    evidence_matches: List[Dict[str, Any]]


class DraftResponse(BaseModel):
    session_id: str
    sections: List[Section]
    overall_coverage: float


class CoverageStandard(BaseModel):
    standard_number: str
    standard_title: str
    coverage_score: float
    criteria_count: int
    covered_criteria: int
    missing_criteria: List[str]


class CoverageDashboard(BaseModel):
    overall_coverage: float
    standards: List[CoverageStandard]
    missing_evidence_count: int
    priority_tasks: List[str]


class SectionUpdate(BaseModel):
    content: str
    accepted_suggestions: Optional[List[str]] = None
    rejected_suggestions: Optional[List[str]] = None
