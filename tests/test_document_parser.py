"""Tests for document parser module."""

import pytest
from pathlib import Path
from src.document_parser import DocumentParser


@pytest.fixture
def parser():
    """Create a document parser instance."""
    return DocumentParser()


@pytest.fixture
def sample_txt_file(tmp_path):
    """Create a sample text file for testing."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("This is a test document.\nIt has multiple lines.")
    return str(file_path)


def test_parser_initialization(parser):
    """Test parser initialization."""
    assert parser is not None
    assert len(parser.parsers) > 0
    assert '.txt' in parser.SUPPORTED_FORMATS


def test_parse_txt_file(parser, sample_txt_file):
    """Test parsing a text file."""
    result = parser.parse(sample_txt_file)
    
    assert result is not None
    assert 'content' in result
    assert 'file_name' in result
    assert 'file_type' in result
    assert result['file_type'] == '.txt'
    assert 'This is a test document' in result['content']


def test_parse_nonexistent_file(parser):
    """Test parsing a non-existent file."""
    with pytest.raises(FileNotFoundError):
        parser.parse('/nonexistent/file.txt')


def test_parse_unsupported_format(parser, tmp_path):
    """Test parsing an unsupported file format."""
    file_path = tmp_path / "test.xyz"
    file_path.write_text("test content")
    
    with pytest.raises(ValueError, match="Unsupported file format"):
        parser.parse(str(file_path))


def test_metadata_extraction(parser, sample_txt_file):
    """Test metadata extraction."""
    result = parser.parse(sample_txt_file)
    
    assert 'metadata' in result
    assert 'file_size' in result['metadata']
    assert result['metadata']['file_size'] > 0
