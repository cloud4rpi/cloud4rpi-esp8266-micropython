.PHONY: init style lint

init:
	pip install pep8 pylint

lint:
	pylint --rcfile=.pylintrc --reports=n *.py

style:
	pep8 --show-source --show-pep8 .

ci: style lint
