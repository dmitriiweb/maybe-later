.PHONY: test
test:
	pytest --cov=maybe_later -vv tests/
	flake8 maybe_later tests/
	mypy maybe_later --implicit-reexport
	black maybe_later tests/
	isort maybe_later tests/

.PHONY: linters
linters:
	mypy maybe_later --implicit-reexport
	black maybe_later tests/
	isort maybe_later tests/

.PHONY: publish
publish:
	poetry build
	poetry publish