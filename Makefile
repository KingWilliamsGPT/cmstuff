.PHONY: help install dev clean build test check upload upload-test

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install the package locally
	pip install .

dev: ## Install in editable/development mode
	pip install -e .

clean: ## Remove build artifacts
	rm -rf build/ dist/ src/*.egg-info .eggs/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true

build: clean ## Build source and wheel distributions
	pip install --upgrade setuptools wheel
	python setup.py sdist bdist_wheel

test: ## Run tests
	python -m pytest tests/ -v

check: build ## Check the built package before uploading
	pip install --upgrade twine
	twine check dist/*

upload-test: check ## Upload to TestPyPI
	twine upload --repository testpypi dist/*

upload: check ## Upload to PyPI (production)
	twine upload dist/*
