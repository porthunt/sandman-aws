SHELL := /bin/bash

lint:
	flake8 src/
	black --line-length 79 --check src/
	tflint .2 > /dev/null || ./tflint .

unit:
	python -m  pytest --disable-warnings tests/

test: lint unit
