# Targets for working with a FastAPI project

FLAGS=

clean:
	rm -rf `find . -name __pycache__`
	rm -rf .pytest_cache
	find . -type f -name '*.py[co]'  -delete
	find . -type f -name '*~'  -delete
	find . -type f -name '.*~'  -delete
	rm -rf build

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
