SERVICE=kami
PYTHONBASE=python3.11

.PHONY:
help:
	@echo ""
	@echo "Help"
	@echo ""
	@echo "Run linters:"
	@echo "    make linters"
	@echo ""

.PHONY:
linters:
	mypy --config-file .mypy.ini --ignore-missing-imports --show-column-numbers airlines/
	flake8 --ignore=E501 airlines/


