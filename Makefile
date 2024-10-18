# Makefile for Flask application

.PHONY: install lint test format

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Lint the code
lint:
	@echo "Running linter..."
	flake8 api/ scraper/ tests/ --max-line-length=79 

# Run tests
test:
	@echo "Running tests..."
	pytest tests/

# Format the code
format:
	@echo "Formatting code..."
	black api/ scraper/ 

# Clean up .pyc files
clean:
	@echo "Cleaning up..."
	find . -name "*.pyc" -exec rm -f {} \;
