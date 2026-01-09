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
