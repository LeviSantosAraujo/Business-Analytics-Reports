# Business Analytics Dashboard Makefile
# Provides convenient commands for development and deployment

.PHONY: help install test lint format clean run reports excel setup docs

# Default target
help:
	@echo "Business Analytics Dashboard - Available Commands:"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  install     - Install dependencies and setup environment"
	@echo "  setup       - Complete project setup"
	@echo ""
	@echo "Development:"
	@echo "  test        - Run all tests"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code with black"
	@echo "  clean       - Clean temporary files and cache"
	@echo ""
	@echo "Running Analytics:"
	@echo "  run         - Run comprehensive analytics (console)"
	@echo "  reports     - Generate text reports and charts"
	@echo "  excel       - Generate Excel reports"
	@echo "  all         - Generate all report types"
	@echo ""
	@echo "Documentation:"
	@echo "  docs        - Generate documentation"
	@echo "  check       - Run all quality checks"
	@echo ""
	@echo "Utility:"
	@echo "  validate    - Validate configuration and data"
	@echo "  status      - Show project status"

# Installation and setup
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	@echo "✓ Dependencies installed"

setup: install
	@echo "Setting up project..."
	python -m venv .venv
	@echo "✓ Virtual environment created"
	@echo "✓ Project setup complete"

# Development tools
test:
	@echo "Running tests..."
	python -m pytest tests/ -v --cov=src --cov-report=html
	@echo "✓ Tests completed"

lint:
	@echo "Running linting..."
	flake8 *.py src/ tests/ --max-line-length=100 --ignore=E203,W503
	@echo "✓ Linting completed"

format:
	@echo "Formatting code..."
	black *.py src/ tests/
	@echo "✓ Code formatted"

check: lint test
	@echo "Running all quality checks..."
	@echo "✓ All checks passed"

# Cleaning
clean:
	@echo "Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.log" -delete
	find . -name "*.tmp" -delete
	find . -name "*.temp" -delete
	find . -name "~$*.xlsx" -delete
	@echo "✓ Temporary files cleaned"

# Running analytics
run:
	@echo "Running comprehensive analytics..."
	python comprehensive_analytics.py
	@echo "✓ Analytics completed"

reports:
	@echo "Generating text reports and charts..."
	python generate_reports.py
	@echo "✓ Reports and charts generated"

excel:
	@echo "Generating Excel reports..."
	python generate_excel_reports.py
	@echo "✓ Excel reports generated"

all: reports excel
	@echo "Generating all report types..."
	@echo "✓ All reports generated"

# Documentation
docs:
	@echo "Generating documentation..."
	@echo "Documentation available in README.md and other markdown files"
	@echo "✓ Documentation ready"

# Validation and status
validate:
	@echo "Validating configuration and data..."
	python config.py
	@echo "✓ Configuration validated"

status:
	@echo "Project Status:"
	@echo "==============="
	@echo "Python Version: $$(python --version)"
	@echo "Virtual Environment: $$(python -c 'import sys; print("Active" if sys.prefix != sys.base_prefix else "Inactive")')"
	@echo "Reports Directory: $$(ls -la reports/ 2>/dev/null | wc -l) files"
	@echo "Charts Directory: $$(ls -la reports/charts/ 2>/dev/null | wc -l) files"
	@echo "Data File: $$(test -f DevicesData.xlsx && echo "Exists" || echo "Missing")"
	@echo ""
	@echo "Last Generated Reports:"
	@ls -la reports/*.xlsx 2>/dev/null | tail -5 || echo "No Excel reports found"
	@echo ""
	@echo "Configuration:"
	@python config.py 2>/dev/null || echo "Configuration validation failed"

# Development shortcuts
dev-setup: setup
	@echo "Development environment ready"

dev-test: format lint test
	@echo "Development checks completed"

# Production shortcuts
prod-build: clean test
	@echo "Production build ready"

prod-deploy: prod-build all
	@echo "Production deployment ready"

# Quick start for new users
quickstart:
	@echo "Quick Start Guide:"
	@echo "=================="
	@echo "1. Setup environment: make setup"
	@echo "2. Validate setup: make validate"
	@echo "3. Run analytics: make run"
	@echo "4. Generate reports: make all"
	@echo "5. Check status: make status"
	@echo ""
	@echo "For detailed help, see README.md"

# Backup and restore
backup:
	@echo "Creating backup..."
	timestamp=$$(date +%Y%m%d_%H%M%S); \
	tar -czf backup_$${timestamp}.tar.gz --exclude='.venv' --exclude='reports' --exclude='__pycache__' .; \
	echo "✓ Backup created: backup_$${timestamp}.tar.gz"

restore:
	@echo "Available backups:"
	@ls -la backup_*.tar.gz 2>/dev/null || echo "No backups found"
	@echo "To restore: tar -xzf backup_YYYYMMDD_HHMMSS.tar.gz"

# Performance testing
benchmark:
	@echo "Running performance benchmarks..."
	python -m pytest tests/test_performance.py -v
	@echo "✓ Benchmarks completed"

# Security checks
security:
	@echo "Running security checks..."
	pip install safety bandit
	safety check
	bandit -r . -f json -o security_report.json
	@echo "✓ Security checks completed"

# Docker commands (if using Docker)
docker-build:
	@echo "Building Docker image..."
	docker build -t business-analytics-dashboard .
	@echo "✓ Docker image built"

docker-run:
	@echo "Running Docker container..."
	docker run -v $$(pwd)/data:/app/data -v $$(pwd)/reports:/app/reports business-analytics-dashboard

# CI/CD helpers
ci-test:
	@echo "Running CI tests..."
	python -m pytest tests/ --cov=src --cov-fail-under=80
	black --check *.py src/ tests/
	flake8 *.py src/ tests/
	@echo "✓ CI tests passed"

ci-build: ci-test
	@echo "CI build completed successfully"

# Advanced development
profile:
	@echo "Running performance profiling..."
	python -m cProfile -o profile_output.prof comprehensive_analytics.py
	python -c "import pstats; p = pstats.Stats('profile_output.prof'); p.sort_stats('cumulative').print_stats(20)"
	@echo "✓ Profiling completed"

memory-test:
	@echo "Running memory usage test..."
	python -m memory_profiler comprehensive_analytics.py
	@echo "✓ Memory test completed"

# Documentation generation (if using Sphinx)
docs-build:
	@echo "Building documentation..."
	cd docs && make html
	@echo "✓ Documentation built"

docs-serve:
	@echo "Serving documentation..."
	cd docs/_build/html && python -m http.server 8000

# Release management
version:
	@python -c "import config; print(f'Current version: {getattr(config, \"VERSION\", \"1.0.0\")}')"

bump-patch:
	@echo "Bumping patch version..."
	# Add version bumping logic here

bump-minor:
	@echo "Bumping minor version..."
	# Add version bumping logic here

bump-major:
	@echo "Bumping major version..."
	# Add version bumping logic here

# Environment management
env-dev:
	@echo "Setting development environment..."
	export ENV=development
	@echo "✓ Development environment set"

env-prod:
	@echo "Setting production environment..."
	export ENV=production
	@echo "✓ Production environment set"

# Data management
data-validate:
	@echo "Validating data file..."
	python -c "import pandas as pd; df = pd.read_excel('DevicesData.xlsx'); print(f'Data shape: {df.shape}'); print(f'Missing values: {df.isnull().sum().sum()}')"
	@echo "✓ Data validation completed"

data-backup:
	@echo "Backing up data..."
	cp DevicesData.xlsx backup/DevicesData_$$(date +%Y%m%d_%H%M%S).xlsx
	@echo "✓ Data backed up"

# Report management
reports-clean:
	@echo "Cleaning generated reports..."
	rm -rf reports/*
	mkdir -p reports/charts
	@echo "✓ Reports cleaned"

reports-archive:
	@echo "Archiving reports..."
	timestamp=$$(date +%Y%m%d_%H%M%S); \
	tar -czf reports_archive_$${timestamp}.tar.gz reports/; \
	echo "✓ Reports archived: reports_archive_$${timestamp}.tar.gz"

# Help for specific topics
help-install:
	@echo "Installation Help:"
	@echo "=================="
	@echo "Prerequisites:"
	@echo "- Python 3.9 or higher"
	@echo "- pip package manager"
	@echo "- Sufficient disk space for reports"
	@echo ""
	@echo "Installation steps:"
	@echo "1. make setup"
	@echo "2. make validate"
	@echo "3. make quickstart"

help-analytics:
	@echo "Analytics Help:"
	@echo "==============="
	@echo "Available analytics modules:"
	@echo "- Descriptive Analytics: Basic statistics"
	@echo "- Performance Analytics: Returns and volatility"
	@echo "- Technical Analytics: Indicators and signals"
	@echo "- Risk Analytics: Risk metrics and VaR"
	@echo "- Time Series Analytics: Seasonality and trends"
	@echo "- Volatility Analytics: Volatility patterns"
	@echo "- Predictive Analytics: Trend predictions"
	@echo "- Trading Strategy Analytics: Strategy backtesting"
	@echo ""
	@echo "Usage:"
	@echo "make run          - Console output"
	@echo "make reports      - Text + Charts"
	@echo "make excel         - Excel reports"
	@echo "make all           - All formats"
