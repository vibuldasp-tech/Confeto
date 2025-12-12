# Contributing to Document Gap Analysis Tool

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/document-gap-analyzer.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Install dev dependencies: `pip install -e ".[dev]"`

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write clean, readable code
- Follow Python PEP 8 style guidelines
- Add docstrings to functions and classes
- Keep functions focused and single-purpose

### 3. Add Tests

All new features should include tests:

```bash
# Create test file in tests/ directory
# tests/test_your_feature.py

def test_your_feature():
    # Your test code
    assert True
```

### 4. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_your_feature.py -v
```

### 5. Update Documentation

- Update README.md if adding new features
- Add docstrings to new functions/classes
- Update CHANGELOG.md (if exists)

### 6. Commit Your Changes

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: description of what you added"
```

### 7. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Code Style

### Python Style

- Follow PEP 8
- Use meaningful variable names
- Maximum line length: 100 characters
- Use type hints where appropriate

Example:

```python
def parse_document(file_path: str) -> Dict[str, any]:
    """
    Parse a document and extract content.
    
    Args:
        file_path: Path to the document
        
    Returns:
        Dictionary with document content and metadata
    """
    # Implementation
    pass
```

### Documentation

- Use docstrings for all public functions/classes
- Follow Google-style docstring format
- Include type hints in function signatures

## Testing Guidelines

### Test Structure

```python
def test_feature_name():
    # Arrange: Set up test data
    test_data = create_test_data()
    
    # Act: Execute the functionality
    result = function_under_test(test_data)
    
    # Assert: Verify the results
    assert result == expected_result
```

### Test Coverage

- Aim for >80% code coverage
- Test happy paths and edge cases
- Test error handling

## Adding New AI Providers

To add support for a new AI provider:

1. Create a new class in `src/ai_provider.py` that inherits from `AIProvider`
2. Implement the `analyze()` method
3. Add configuration options to `.env.example`
4. Update the `get_ai_provider()` factory function
5. Add tests in `tests/test_ai_provider.py`
6. Update documentation

Example:

```python
class NewAIProvider(AIProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('NEW_AI_API_KEY')
        # Initialize client
    
    def analyze(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        # Implementation
        pass
```

## Adding Document Format Support

To add support for a new document format:

1. Add the extension to `SUPPORTED_FORMATS` in `DocumentParser`
2. Implement a parser method (e.g., `_parse_rtf()`)
3. Add it to the `parsers` dictionary
4. Add required dependencies to `requirements.txt`
5. Add tests
6. Update documentation

## Reporting Issues

When reporting issues, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)
- Sample documents (if applicable)

## Feature Requests

Feature requests are welcome! Please:

- Check if it's already been requested
- Explain the use case
- Describe the expected behavior
- Consider contributing the feature yourself

## Code Review Process

Pull requests will be reviewed for:

- Code quality and style
- Test coverage
- Documentation
- Backward compatibility
- Performance implications

## Questions?

Feel free to:
- Open an issue for discussion
- Ask questions in pull requests
- Reach out to maintainers

Thank you for contributing!
