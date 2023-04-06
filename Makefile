lint:
	flake8 app/
	isort --check --diff app/
	black --check app/
	mypy --ignore-missing-imports app/

format:
	isort app/
	black app/

mypy:
	mypy --ignore-missing-imports app/
