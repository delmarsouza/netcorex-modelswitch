.PHONY: test lint format

test:
	pytest -q

lint:
	python -m compileall src tests

format:
	@echo "Formatting placeholder"
