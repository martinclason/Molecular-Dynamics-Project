# Phony targets to enable running e.g. test target while also having a folder named test
.PHONY: test

ci:
	@echo "Running CI tests locally..."
	make lint
	make test

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

html-doc:
	@echo "Running sphinx html doc generation..."
	make --directory docs html