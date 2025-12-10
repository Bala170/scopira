# Scopira Makefile

# Variables
PYTHON := python3
PIP := pip3

# Help target
help:
	@echo "Scopira Development Commands"
	@echo "============================"
	@echo "setup     - Install all dependencies"
	@echo "run       - Start development servers"
	@echo "test      - Run all tests"
	@echo "clean     - Clean up temporary files"
	@echo "docs      - Generate documentation"
	@echo "docker    - Start services with Docker Compose"

# Setup development environment
setup:
	$(PYTHON) setup.py

# Run development servers
run:
	$(PYTHON) run_dev.py

# Run tests
test:
	$(PYTHON) run_tests.py

# Clean temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf uploads/
	mkdir uploads/

# Generate documentation
docs:
	@echo "Documentation is available in DOCUMENTATION.md"

# Run with Docker
docker:
	docker-compose up

# Stop Docker services
docker-stop:
	docker-compose down

# Build Docker images
docker-build:
	docker-compose build

# Install backend dependencies
install-backend:
	cd backend && $(PIP) install -r requirements.txt

# Install ML dependencies
install-ml:
	cd ml && $(PIP) install -r requirements.txt

# Install database dependencies
install-db:
	cd database && $(PIP) install -r requirements.txt

.PHONY: help setup run test clean docs docker docker-stop docker-build install-backend install-ml install-db