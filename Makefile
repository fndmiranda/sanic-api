requirements-dev:
	@pip install --upgrade pip
	@pip install -r requirements/development.txt

runserver-dev:
	@python main.py

flake8:
	@flake8 --show-source
