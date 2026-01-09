# dbt usage

## Location conventions

- Data tooling lives under `data/` in this repo.
- The dbt project is at `data/dbt/`.
- DuckDB state is stored at `data/warehouse.duckdb` by default.

## Prerequisites

- Install dbt with the DuckDB adapter (for example, `pip install dbt-duckdb`).
- Run commands from the repo root.

## Common commands

```bash
make dbt-debug
make dbt-run
```

## Configuration

To override the DuckDB path, set `DBT_DUCKDB_PATH` before running dbt:

```bash
export DBT_DUCKDB_PATH=/path/to/warehouse.duckdb
```
