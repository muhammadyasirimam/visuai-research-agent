.PHONY: install test lint format docs clean docker-build docker-run

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=visuai --cov-report=html

lint:
	flake8 src/visuai
	mypy src/visuai --ignore-missing-imports

format:
	black src/visuai tests/
	isort src/visuai tests/

docs:
	mkdocs serve

docs-build:
	mkdocs build

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .mypy_cache/ htmlcov/
	rm -rf visuai_output/ .visuai_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	docker build -t visuai -f docker/Dockerfile .

docker-run:
	docker run -p 8501:8501 -e VISUAI_LLM_API_KEY=$(OPENAI_API_KEY) visuai

web:
	streamlit run src/visuai/web/app.py --server.port 8501

cli:
	visuai --help

demo:
	python examples/demo.py
