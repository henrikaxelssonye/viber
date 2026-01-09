.PHONY: install lint format test dbt-debug dbt-run

export DBT_PROJECT_DIR := $(abspath data/dbt)
export DBT_PROFILES_DIR := $(abspath data/dbt)

install:
	pip install -e .[dev]

lint:
	ruff check .

format:
	ruff format .

test:
	pytest

dbt-debug:
	dbt debug --project-dir $(DBT_PROJECT_DIR) --profiles-dir $(DBT_PROFILES_DIR)

dbt-run:
	dbt run --project-dir $(DBT_PROJECT_DIR) --profiles-dir $(DBT_PROFILES_DIR)
