"""Tests for report generator module."""

import pytest
from pathlib import Path
from src.report_generator import ReportGenerator
from src.gap_analyzer import GapAnalysisReport, GapAnalysisItem


@pytest.fixture
def generator():
    """Create a report generator instance."""
    return ReportGenerator()


@pytest.fixture
def sample_report():
    """Create a sample gap analysis report."""
    gaps = [
        GapAnalysisItem("Ref1", "Revenue data", "present", "Found in section 2", 0.95),
        GapAnalysisItem("Ref1", "Balance sheet", "absent", "Not found", 0.90),
        GapAnalysisItem("Ref2", "Customer metrics", "partial", "Incomplete", 0.80),
    ]
    
    return GapAnalysisReport(
        user_document="user_doc.txt",
        reference_documents=["ref1.txt", "ref2.txt"],
        timestamp="2024-12-12T10:00:00",
        summary="Test summary",
        gaps=gaps,
        coverage_score=65.0
    )


def test_generator_initialization(generator):
    """Test generator initialization."""
    assert generator is not None


def test_generate_markdown(generator, sample_report):
    """Test markdown report generation."""
    markdown = generator.generate_markdown(sample_report)
    
    assert markdown is not None
    assert "# Document Gap Analysis Report" in markdown
    assert "user_doc.txt" in markdown
    assert "Coverage Score" in markdown
    assert "Revenue data" in markdown
    assert "Balance sheet" in markdown


def test_generate_html(generator, sample_report):
    """Test HTML report generation."""
    html = generator.generate_html(sample_report)
    
    assert html is not None
    assert "<!DOCTYPE html>" in html
    assert "user_doc.txt" in html
    assert "Coverage Score" in html
    assert "Revenue data" in html


def test_save_report_markdown(generator, sample_report, tmp_path):
    """Test saving markdown report to file."""
    output_path = tmp_path / "report.md"
    generator.save_report(sample_report, str(output_path), format='markdown')
    
    assert output_path.exists()
    content = output_path.read_text()
    assert "# Document Gap Analysis Report" in content


def test_save_report_html(generator, sample_report, tmp_path):
    """Test saving HTML report to file."""
    output_path = tmp_path / "report.html"
    generator.save_report(sample_report, str(output_path), format='html')
    
    assert output_path.exists()
    content = output_path.read_text()
    assert "<!DOCTYPE html>" in content


def test_save_report_json(generator, sample_report, tmp_path):
    """Test saving JSON report to file."""
    output_path = tmp_path / "report.json"
    generator.save_report(sample_report, str(output_path), format='json')
    
    assert output_path.exists()
    content = output_path.read_text()
    assert "user_document" in content
    assert "gaps" in content


def test_save_report_invalid_format(generator, sample_report, tmp_path):
    """Test saving with invalid format."""
    output_path = tmp_path / "report.xyz"
    
    with pytest.raises(ValueError, match="Unknown format"):
        generator.save_report(sample_report, str(output_path), format='xyz')


def test_report_creates_directories(generator, sample_report, tmp_path):
    """Test that saving report creates necessary directories."""
    output_path = tmp_path / "subdir" / "nested" / "report.md"
    generator.save_report(sample_report, str(output_path), format='markdown')
    
    assert output_path.exists()
    assert output_path.parent.exists()
