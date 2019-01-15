.PHONY: init style lint lint3

init:
	pip install pycodestyle pylint

lint:
	pylint --rcfile=.pylintrc --reports=n *.py

lint3:
	python3 -m pylint --rcfile=.pylintrc --reports=n *.py

style:
	pycodestyle --show-source --show-pep8 .

ci: style lint
