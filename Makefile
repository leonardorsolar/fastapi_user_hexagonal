# Makefile

.PHONY: test

test:
	PYTHONPATH=./src pytest tests/
