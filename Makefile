.DEFAULT_GOAL := all

full_sources = developing_tools tests
sources = developing_tools
configuration_file = pyproject.toml


.PHONY: install  # Install production dependencies
install:
	@pip install -r requirements.txt


.PHONY: install-dev  # Install development dependencies
install-dev:
	@pip install -r requirements_dev.txt


.PHONY: format  # Automatically format python code
format:
	@ruff check $(full_sources) --fix-only --config $(configuration_file)
	@ruff format $(full_sources) --config $(configuration_file)


.PHONY: lint  # Lint python code
lint:
	@set -e; \
	mypy $(full_sources) --txt-report . --config-file $(configuration_file) || mypy_exit=$$?; \
	bandit $(sources) --recursive --configfile $(configuration_file) || bandit_exit=$$?; \
	ruff check $(full_sources) || ruff_exit=$$?; \
	exit $$(( mypy_exit || bandit_exit || ruff_exit ))


.PHONY: test # Run all tests
test:
	@pytest --config-file $(configuration_file)


.PHONY: coverage # Get coverage report
coverage:
	@set -e; \
	coverage erase; \
	coverage run -m pytest --config-file $(configuration_file) || coverage_exit=$$?; \
	coverage combine; \
	coverage report; \
	exit $$coverage_exit


.PHONY: help # Show this help message
help:
	@echo "Usage: make [COMMAND] [OPTIONS]..."
	@echo
	@echo "Commands:"
	@echo "  make install     	Install production dependencies"
	@echo "  make install-dev 	Install development dependencies"
	@echo "  make format      	Automatically format python code"
	@echo "  make lint        	Lint python code"
	@echo "  make test        	Run all tests"
	@echo "  make coverage    	Get coverage report"
	@echo "  make help        	Show this help message"
