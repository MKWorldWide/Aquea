.PHONY: help install dev test lint format check docs clean

# Default target
help:
	@echo "Aquea - Open Water Reclamation System"
	@echo ""
	@echo "Available targets:"
	@echo "  install    Install development dependencies"
	@echo "  dev       Start development servers"
	@echo "  test      Run tests with coverage"
	@echo "  lint      Run linters (ruff, black, mypy)"
	@echo "  format    Format code (black, isort, ruff)"
	@echo "  check     Run all checks (lint + test)"
	@echo "  docs      Build and serve documentation"
	@echo "  clean     Remove build artifacts"

# Install development dependencies
install:
	python -m pip install --upgrade pip
	pip install -e ".[dev]"
	pre-commit install

# Start development servers
dev:
	docker compose up --build

# Run tests
TEST_ARGS ?= -v
TEST_PATH ?= tests/
test:
	pytest $(TEST_ARGS) $(TEST_PATH)

# Run linters
lint:
	echo "Running ruff..."
	ruff check .
	echo "\nRunning black..."
	black --check .
	echo "\nRunning mypy..."
	mypy .

# Format code
format:
	black .
	isort .
	ruff check --fix .

# Run all checks
check: lint test

# Build and serve documentation
docs:
	mkdocs serve

# Clean build artifacts
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]'`
	rm -f `find . -type f -name '*~'`
	rm -f `find . -type f -name '.*~'`
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	docker compose down -v
	docker system prune -f

docker-clean:
	docker system prune -f
	docker volume prune -f
	docker network prune -f

docker-reset: docker-clean
	docker rmi $(docker images -a -q) -f || true
	docker volume rm $(docker volume ls -q) -f || true

# Show help by default
.DEFAULT_GOAL := help
