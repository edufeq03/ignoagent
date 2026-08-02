.PHONY: install run test clean

install:
	pip install -e .

run:
	python -m ignoagent

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
