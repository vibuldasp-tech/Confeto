.PHONY: help install test clean run example

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests with coverage"
	@echo "  make clean      - Clean up generated files"
	@echo "  make run        - Run the CLI tool"
	@echo "  make example    - Run example analysis"
	@echo "  make lint       - Run code linting"
	@echo "  make format     - Format code with black"

install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest --cov=src --cov-report=html --cov-report=term-missing

test-verbose:
	pytest -v --cov=src --cov-report=html --cov-report=term-missing

clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	rm -rf src/__pycache__ tests/__pycache__
	rm -rf build dist *.egg-info
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

run:
	python gap_analyzer.py --help

example:
	python gap_analyzer.py analyze \
		examples/user_document.txt \
		examples/reference_doc1_financial_requirements.txt \
		examples/reference_doc2_operational_requirements.txt \
		examples/reference_doc3_governance_requirements.txt

check-setup:
	python gap_analyzer.py check-setup

lint:
	@echo "Note: Install flake8 first with: pip install flake8"
	flake8 src/ --max-line-length=100 --ignore=E501,W503

format:
	@echo "Note: Install black first with: pip install black"
	black src/ tests/ --line-length=100

.DEFAULT_GOAL := help
