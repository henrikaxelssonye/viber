# Viber Data Platform

Viber is a data platform project scaffolded for agentic coding workflows. This repository
provides a clean baseline with conventions, documentation, and automation hooks to help
teams iterate quickly and safely.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]
```

Run tests:

```bash
pytest
```

## Fabric Lakehouse access

The Lakehouse connector uses the OneLake ADLS Gen2-compatible endpoint to read Parquet
tables or files. Configure the connector via environment variables:

- `VIBER_FABRIC_WORKSPACE`: Fabric workspace name.
- `VIBER_FABRIC_LAKEHOUSE`: Lakehouse name.
- `VIBER_FABRIC_TABLE`: Default table name (optional).
- `VIBER_FABRIC_PATH`: Default file path under `Files/` (optional).
- `VIBER_FABRIC_ENDPOINT`: OneLake endpoint (default:
  `https://onelake.dfs.fabric.microsoft.com`).
- `VIBER_FABRIC_TENANT_ID`, `VIBER_FABRIC_CLIENT_ID`, `VIBER_FABRIC_CLIENT_SECRET`: Service
  principal auth (optional).
- `VIBER_FABRIC_ACCOUNT_KEY`: Storage account key (optional).

Example usage:

```python
from viber.config import load_fabric_lakehouse_config
from viber.lakehouse import FabricLakehouseReader

config = load_fabric_lakehouse_config()
reader = FabricLakehouseReader(config, output_type="pyarrow")
table = reader.read_table("sales")
```

## Repo layout

- `src/viber/`: Python package root.
- `tests/`: Test suite.
- `docs/`: Architecture, decisions, and playbooks.
- `scripts/`: Helper scripts.

## Next steps

- Define domain models and ingestion pipelines in `src/viber/`.
- Capture architectural decisions in `docs/adr/`.
- Extend automation (CI/CD, linting, type checks).

## Agentic coding

See `docs/agentic-coding.md` for collaboration conventions and automation hooks.
