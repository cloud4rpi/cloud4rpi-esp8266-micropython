.PHONY: init style lint

init:
	pip install pycodestyle pylint

lint:
	python3 -m pylint --rcfile=.pylintrc --reports=n *.py

style:
	pycodestyle --show-source --show-pep8 .

ci: style lint
