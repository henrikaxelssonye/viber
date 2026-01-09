# Agentic coding guidelines

These conventions make it easier for humans and agents to collaborate safely.

## Repository hygiene

- Prefer small, focused commits with clear messages.
- Keep architecture decisions in `docs/adr/`.
- Document operational workflows in `docs/playbooks/`.

## Coding workflows

- Start by clarifying intent and scope in issues/notes.
- Use tests or checks for every new behavior.
- Prefer explicit configuration over implicit defaults.

## Automation hooks

- Use `pre-commit` for formatting and linting.
- Run `make test` before releasing changes.
