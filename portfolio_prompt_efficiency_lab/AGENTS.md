# Portfolio Prompt Efficiency Lab

## Stable commands

- `uv sync`
- `uv run dbt seed`
- `uv run dbt build`
- `uv run dbt test`
- `uv run python scripts/reset_demo_state.py`

## Working style for this repo

- Treat `models/gold/portfolio_reporting/` as the default relevant slice unless the task says otherwise.
- Avoid `models/gold/compliance/`, `models/gold/archived/`, and `analyses/` unless the task explicitly requires them.
- Reuse `docs/repo_map.md` and `docs/dbt_lineage_notes.md` before re-scanning the repository.
- Plan before editing on implementation tasks and keep changes scoped to the smallest safe file set.

## Conventions

- Silver models clean and type raw seed data.
- Gold portfolio reporting models are the main demo path.
- Business-facing validation lives in dbt tests, not only in prose.
- Keep reusable docs concise; they are context indexes, not exhaustive inventories.
