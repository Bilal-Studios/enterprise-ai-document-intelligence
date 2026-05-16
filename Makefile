.PHONY: install run test lint eval docker-build docker-run check

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	pytest

lint:
	ruff check .

eval:
	python evals/run_evals.py

docker-build:
	docker build -t enterprise-ai-document-intelligence .

docker-run:
	docker run --rm -p 8000:8000 enterprise-ai-document-intelligence

check:
	ruff check .
	pytest
	python evals/run_evals.py