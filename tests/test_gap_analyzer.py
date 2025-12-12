"""Tests for gap analyzer module."""

import pytest
from unittest.mock import Mock, MagicMock
from src.gap_analyzer import GapAnalyzer, GapAnalysisItem, GapAnalysisReport


@pytest.fixture
def mock_ai_provider():
    """Create a mock AI provider."""
    provider = Mock()
    provider.analyze = Mock(return_value="""
    [
        {
            "requirement": "Financial revenue data",
            "status": "present",
            "details": "Document includes revenue figures",
            "confidence": 0.95
        },
        {
            "requirement": "Balance sheet information",
            "status": "absent",
            "details": "No balance sheet data found",
            "confidence": 0.90
        }
    ]
    """)
    return provider


@pytest.fixture
def analyzer(mock_ai_provider):
    """Create a gap analyzer instance."""
    return GapAnalyzer(ai_provider=mock_ai_provider)


@pytest.fixture
def sample_files(tmp_path):
    """Create sample files for testing."""
    user_doc = tmp_path / "user.txt"
    user_doc.write_text("Company revenue: $50M. Customer base: 100,000.")
    
    ref_doc1 = tmp_path / "ref1.txt"
    ref_doc1.write_text("Required: Revenue, profit, balance sheet, cash flow.")
    
    ref_doc2 = tmp_path / "ref2.txt"
    ref_doc2.write_text("Required: Customer metrics, market share, product info.")
    
    return {
        'user': str(user_doc),
        'ref1': str(ref_doc1),
        'ref2': str(ref_doc2)
    }


def test_analyzer_initialization(analyzer):
    """Test analyzer initialization."""
    assert analyzer is not None
    assert analyzer.parser is not None
    assert analyzer.ai_provider is not None


def test_calculate_coverage():
    """Test coverage calculation."""
    analyzer = GapAnalyzer.__new__(GapAnalyzer)
    
    gaps = [
        GapAnalysisItem("Ref1", "req1", "present", "details", 1.0),
        GapAnalysisItem("Ref1", "req2", "absent", "details", 1.0),
        GapAnalysisItem("Ref1", "req3", "partial", "details", 1.0),
    ]
    
    coverage = analyzer._calculate_coverage(gaps)
    # (1.0 + 0.0 + 0.5) / 3 * 100 = 50%
    assert coverage == pytest.approx(50.0, rel=0.1)


def test_gap_analysis_item():
    """Test GapAnalysisItem creation."""
    item = GapAnalysisItem(
        requirement_source="Ref Doc 1",
        requirement="Must include revenue",
        status="present",
        details="Revenue found in section 2",
        confidence=0.95
    )
    
    assert item.requirement_source == "Ref Doc 1"
    assert item.status == "present"
    assert item.confidence == 0.95


def test_gap_analysis_report():
    """Test GapAnalysisReport creation and serialization."""
    gaps = [
        GapAnalysisItem("Ref1", "req1", "present", "details", 0.9)
    ]
    
    report = GapAnalysisReport(
        user_document="user.txt",
        reference_documents=["ref1.txt"],
        timestamp="2024-12-12T10:00:00",
        summary="Test summary",
        gaps=gaps,
        coverage_score=90.0
    )
    
    assert report.user_document == "user.txt"
    assert len(report.gaps) == 1
    assert report.coverage_score == 90.0
    
    # Test serialization
    report_dict = report.to_dict()
    assert 'gaps' in report_dict
    assert 'coverage_score' in report_dict
    
    json_str = report.to_json()
    assert 'user.txt' in json_str


def test_analyze_with_mock(analyzer, sample_files):
    """Test analysis with mock AI provider."""
    report = analyzer.analyze(
        sample_files['user'],
        [sample_files['ref1'], sample_files['ref2']]
    )
    
    assert report is not None
    assert isinstance(report, GapAnalysisReport)
    assert report.user_document == "user.txt"
    assert len(report.reference_documents) == 2
    assert len(report.gaps) >= 0
    assert 0 <= report.coverage_score <= 100
