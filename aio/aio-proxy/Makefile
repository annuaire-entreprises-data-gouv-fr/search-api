FLAGS=


flake:
	flake8 aio_proxy setup.py

clean:
	rm -rf `find . -name __pycache__`
	find . -type f -name '*.py[co]'  -delete
	find . -type f -name '*~'  -delete
	find . -type f -name '.*~'  -delete
	rm -rf build

run:
	python -m aio_proxy

.PHONY: flake clean
