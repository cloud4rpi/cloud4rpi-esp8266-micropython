.PHONY: style lint

style:
	pep8 --show-source --show-pep8 .

ci: style
