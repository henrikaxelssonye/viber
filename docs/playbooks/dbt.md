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

## Lakehouse integration

The dbt model `fabric_lakehouse` reads a local Parquet file generated from Fabric
Lakehouse data. Use the export script to stage data for dbt:

```bash
python scripts/export_lakehouse_parquet.py --table <table-name> \
  --output data/lakehouse/lakehouse.parquet
```

Override the Parquet path using `VIBER_FABRIC_LOCAL_PARQUET` when running dbt.

## Configuration

To override the DuckDB path, set `DBT_DUCKDB_PATH` before running dbt:

```bash
export DBT_DUCKDB_PATH=/path/to/warehouse.duckdb
```
