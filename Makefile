# Makefile for managing the pharmaceutical data pipeline project

# Variables
VENV_NAME = .venv
PYTHON_FILES = $(shell python -c "import toml; print(' '.join(toml.load('pyproject.toml')['tool']['setuptools']['packages']['find']['include']))")

# Detect the operating system
ifeq ($(OS),Windows_NT)
    OS_NAME := Windows
else
    OS_NAME := $(shell uname -s)
endif

# install uv
install_uv:
ifeq ($(OS_NAME),Linux)
	@echo "Detected Linux OS"
	curl -LsSf https://astral.sh/uv/install.sh | sh
else ifeq ($(OS_NAME),Darwin)
	@echo "Detected macOS"
	curl -LsSf https://astral.sh/uv/install.sh | sh
else ifeq ($(OS_NAME),Windows)
	@echo "Detected Windows OS"
	powershell -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
	# "If you are on Windows and this doesn't work, check your permissions or run the command manually."
endif

# Create a virtual environment
venv:
	uv venv $(VENV_NAME)
	@echo "Virtual $(VENV_NAME) environment created."

# Activate the virtual environment
activate:
ifeq ($(OS_NAME),Windows)
	@$(VENV_NAME)\Scripts\activate
else
	@source $(VENV_NAME)/bin/activate
endif
	@echo "Virtual $(VENV_NAME) environment activated."

# Install dependencies using uv
install:
	uv pip install -r requirements.txt
	@echo "Dependencies installed."


# Pre-commit hooks
pre_commit:
	pre-commit install
	@echo "Pre-commit hooks installed."

# Clean up
clean:
ifeq ($(OS_NAME),Windows)
	del /s /q venv
	rmdir /s /q venv
else
	rm -rf venv
endif
	@echo "Cleaned up the environment."


# Tests
test:
	@echo "add tests here"
	@echo "Tests executed."

# Build the Docker image
build:
	docker build -t tools .
	@echo "Docker image built."

# Run the Docker container : docker run -it --rm mle_test ls -la venv
run:
	docker run -it --rm --entrypoint /bin/bash tools
	@echo "Docker container running with interactive shell."

# Linting and formatting
.PHONY: format
format:
	black $(PYTHON_FILES)
	isort $(PYTHON_FILES)
	@echo "Formatting completed."

.PHONY: check-format
check-format:
	black --check $(PYTHON_FILES)
	isort --check --diff $(PYTHON_FILES)
	@echo "Format check completed."

.PHONY: lint
lint: format
	pre-commit run flake8
	pre-commit run bandit
	pre-commit run mypy
	@echo "Linting completed."

# Help
help:
	@echo "Makefile for managing the pharmaceutical data pipeline project"
	@echo "Usage:"
	@echo "  make venv         - Create a virtual environment"
	@echo "  make activate     - Activate the virtual environment"
	@echo "  make install      - Install dependencies using uv"
	@echo "  make pre_commit   - Install pre-commit hooks"
	@echo "  make lint         - Check code style with flake8, isort, black, and mypy"
	@echo "  make format       - Format code with isort and black"
	@echo "  make clean        - Clean up the environment"
	@echo "  make build        - Build the Docker image"
	@echo "  make run          - Run the Docker container"
	@echo "  make help         - Display this help message"
