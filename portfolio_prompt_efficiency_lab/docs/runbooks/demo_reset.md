# Demo Reset Runbook

Use this after a live run so the next session starts from the same baseline.

## Reset

```bash
uv run python scripts/reset_demo_state.py
```

## Rebuild

```bash
uv run python scripts/bootstrap_demo.py
```

## What should be true after rebuild

- `docs/repo_map.md` contains the starter template
- `docs/dbt_lineage_notes.md` contains the starter template
- `portfolio_prompt_efficiency_lab.duckdb` has been recreated
- `uv run dbt build` succeeds from a clean state
