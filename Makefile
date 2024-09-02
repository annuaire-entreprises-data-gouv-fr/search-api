# Targets for working with a FastAPI project

FLAGS=

flake:
	flake8 app setup.py

clean:
	rm -rf `find . -name __pycache__`
	find . -type f -name '*.py[co]'  -delete
	find . -type f -name '*~'  -delete
	find . -type f -name '.*~'  -delete
	rm -rf build

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


.PHONY: flake clean run
