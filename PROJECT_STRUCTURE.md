# Project Structure

```
document-gap-analyzer/
│
├── README.md                 # Main documentation
├── LICENSE                   # License file
├── CONTRIBUTING.md          # Contribution guidelines
├── PROJECT_STRUCTURE.md     # This file
│
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup configuration
├── pytest.ini              # Pytest configuration
├── Makefile                # Common commands
├── quick_start.sh          # Quick setup script
│
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
│
├── gap_analyzer.py         # Main CLI entry point
│
├── src/                    # Source code
│   ├── __init__.py
│   ├── document_parser.py  # Document parsing (PDF, DOCX, TXT)
│   ├── ai_provider.py      # AI provider interfaces (OpenAI, Anthropic)
│   ├── gap_analyzer.py     # Core gap analysis engine
│   ├── report_generator.py # Report generation (MD, HTML, JSON)
│   └── cli.py              # Command-line interface
│
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_document_parser.py
│   ├── test_gap_analyzer.py
│   └── test_report_generator.py
│
└── examples/               # Example documents
    ├── README.md
    ├── user_document.txt
    ├── reference_doc1_financial_requirements.txt
    ├── reference_doc2_operational_requirements.txt
    └── reference_doc3_governance_requirements.txt
```

## Key Files Description

### Core Application Files

- **gap_analyzer.py**: Main entry point for the CLI application
- **src/document_parser.py**: Handles parsing of different document formats
- **src/ai_provider.py**: Abstract interface for AI providers with OpenAI and Anthropic implementations
- **src/gap_analyzer.py**: Core logic for performing gap analysis
- **src/report_generator.py**: Generates reports in multiple formats
- **src/cli.py**: Command-line interface using Click

### Configuration Files

- **requirements.txt**: Python package dependencies
- **setup.py**: Package installation configuration
- **.env.example**: Template for environment variables (API keys)
- **pytest.ini**: Test configuration
- **Makefile**: Common development commands

### Documentation

- **README.md**: Complete user documentation
- **CONTRIBUTING.md**: Guidelines for contributors
- **PROJECT_STRUCTURE.md**: This file
- **examples/README.md**: Documentation for example files

### Tests

- **tests/**: Complete test suite with unit tests
  - Tests for document parser
  - Tests for gap analyzer
  - Tests for report generator

### Examples

- **examples/**: Sample documents for testing
  - User document (to be analyzed)
  - Three reference documents (requirements)

## Module Dependencies

```
cli.py
  ├── gap_analyzer.py
  │   ├── document_parser.py
  │   └── ai_provider.py
  └── report_generator.py
      └── gap_analyzer.py (for data structures)
```

## Data Flow

```
User Input (CLI)
    ↓
Document Parser → Parse all documents
    ↓
Gap Analyzer → Compare user doc vs references
    ↓
AI Provider → Analyze content gaps
    ↓
Gap Analysis Report (data structure)
    ↓
Report Generator → Format as MD/HTML/JSON
    ↓
Output File
```

## Key Design Patterns

1. **Factory Pattern**: `get_ai_provider()` creates appropriate AI provider
2. **Strategy Pattern**: Multiple AI providers implement same interface
3. **Data Classes**: `GapAnalysisItem` and `GapAnalysisReport` for structured data
4. **Single Responsibility**: Each module has one clear purpose

## Extension Points

To extend the application:

1. **Add new document format**: Modify `DocumentParser` class
2. **Add new AI provider**: Implement `AIProvider` interface
3. **Add new report format**: Add method to `ReportGenerator`
4. **Add new CLI command**: Add command to `cli.py`

## Environment Setup

1. Copy `.env.example` to `.env`
2. Add your API keys
3. Run `make install` or `pip install -r requirements.txt`
4. Run `make test` to verify setup

## Quick Commands

```bash
# Setup
make install          # Install dependencies
make check-setup      # Verify configuration

# Development
make test            # Run tests
make test-verbose    # Run tests with details
make lint            # Check code style
make format          # Format code

# Usage
make example         # Run example analysis
make run             # Show CLI help
make clean           # Clean generated files
```
