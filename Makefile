# Phony targets to enable running e.g. test target while also having a folder named test
.PHONY: test

ci:
	@echo "Running CI tests locally..."
	@make ci-lint
	@make ci-test

ci-lint:
	make lint

ci-test:
	make unit-test-no-openkim
	make integration-test-no-openkim

# Run linting on all code and report error count
lint:
	@echo "Running linting on code..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
lint-warn:
	# exit-zero treats all errors as warnings.
	flake8 . --count --exit-zero --max-complexity=10 --statistics

# Run pytest for project
test:
	@echo "Running pytest on code..."
	pytest

test-no-openkim:
	@echo "Running pytest excluding openkim..."
	pytest -k "not openkim"

unit-test-no-openkim:
	@echo "Running pytest with unit tests..."
	pytest -k "not (integration or openkim)"

unit-test:
	@echo "Running pytest with unit tests..."
	pytest -k "not integration"

integration-test-no-openkim:
	@echo "Running pytest with unit tests..."
	pytest -k "integration and not openkim"

integration-test:
	@echo "Running pytest with integration tests..."
	pytest -k "integration"

html-doc:
	@echo "Running sphinx html doc generation..."
	make --directory docs html
