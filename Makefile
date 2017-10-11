.PHONY: init style

init:
	pip install pep8

style:
	pep8 --show-source --show-pep8 .

ci: style
