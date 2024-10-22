full_sources = developing_tools tests
sources = developing_tools
configuration_file = pyproject.toml 


.PHONY: help
help: # Display this help
	@echo "Usage: make [COMMAND] [OPTIONS]..."
	@awk 'BEGIN {FS = ":.*#"; printf "\nCommands:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?#/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


.PHONY: install
install: # Install dependencies
	@make install-dev


.PHONY: install-dev
install-dev: # Install development dependencies
	@pip install --requirement requirements_dev.txt


.PHONY: install-prod
install-prod: # Install production dependencies
	@pip install --requirement requirements.txt


.PHONY: format
format: # Automatically format python code
	@ruff check $(full_sources) --fix-only --config $(configuration_file)
	@ruff format $(full_sources) --config $(configuration_file)


.PHONY: lint
lint: # Lint python code
	@set -e; \
	mypy $(full_sources) --txt-report . --config-file $(configuration_file) || mypy_exit=$$?; \
	bandit $(sources) --recursive --configfile $(configuration_file) || bandit_exit=$$?; \
	ruff check $(full_sources) || ruff_exit=$$?; \
	exit $$(( mypy_exit || bandit_exit || ruff_exit ))


.PHONY: test
test: # Run all tests
	@pytest --config-file $(configuration_file)


.PHONY: coverage
coverage: # Get coverage report
	@set -e; \
	coverage erase; \
	coverage run --module pytest --config-file $(configuration_file) || coverage_exit=$$?; \
	coverage combine; \
	coverage report; \
	exit $$coverage_exit


.PHONY: clean
clean: # Remove all generated files
	@rm --force --recursive `find . -type f -name '*.py[co]'`
	@rm --force --recursive `find . -name __pycache__`
	@rm --force --recursive `find . -name .ruff_cache`
	@rm --force --recursive `find . -name .mypy_cache`
	@rm --force --recursive `find . -name index.txt`
	@rm --force --recursive `find . -name .pytest_cache`
	@rm --force --recursive .coverage
	@rm --force --recursive .coverage.*
	@rm --force --recursive coverage.xml
	@rm --force --recursive htmlcov
