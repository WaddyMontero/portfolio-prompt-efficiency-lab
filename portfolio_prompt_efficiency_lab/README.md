# Portfolio Prompt Efficiency Lab

`portfolio_prompt_efficiency_lab` is a compact `dbt-duckdb` sandbox built for live demos about prompt efficiency with AI coding agents. It gives you one clearly relevant analytics slice, one unrelated slice, and enough decoys to make vague prompting observably noisier than scoped prompting.

## What this repo is for

- Demonstrate why scoped prompting is cheaper and safer than broad prompting.
- Show how reusable artifacts reduce repeated repo discovery work.
- Keep the project small enough for a 12-15 minute live workshop.

## Quickstart

Run these commands from the repository root:

1. Create your local environment file from the example:

```bash
cp .env.example .env
```

2. Then run the setup and validation commands:

```bash
uv sync
uv run dbt seed
uv run dbt build
uv run dbt test
```

`uv run` reads `.env`, so `DBT_PROFILES_DIR=.` is loaded automatically and no extra flags are needed after you create that file.

For a one-command clean bootstrap:

```bash
uv run python scripts/bootstrap_demo.py
```

## How To Run This Live

Use the same sequence for both runs so the comparison stays fair.

1. Bootstrap the clean baseline.

   ```bash
   cp .env.example .env
   uv sync
   uv run python scripts/bootstrap_demo.py
   ```

2. Open the materials you will use during the exercise:
   - [showcase/prompt_pairs.md](showcase/prompt_pairs.md)
   - [showcase/scorecard.md](showcase/scorecard.md)
   - [docs/runbooks/demo_reset.md](docs/runbooks/demo_reset.md)

3. Start a fresh agent session and run the three careless prompts from `showcase/prompt_pairs.md`.
4. Fill in `showcase/scorecard.md` as you go so you capture files inspected, repeated scans, changed files, validation, and risks.
5. When the careless run is done, reset both the repo and your tool state:

   ```bash
   uv run python scripts/reset_demo_state.py
   ```

   Then clear or restart your coding agent so the disciplined run does not inherit the earlier context.

6. Re-bootstrap the repo if you want a fully rebuilt clean state:

   ```bash
   uv run python scripts/bootstrap_demo.py
   ```

7. Start a new fresh agent session and run the disciplined prompts from `showcase/prompt_pairs.md`.
8. Fill in the second side of `showcase/scorecard.md` and compare the two runs.

Task 3 should always start from the clean baseline. Do not reuse partially edited files from the earlier run if you want a fair comparison.

## Demo storyline

The live showcase is built around the same repo and three tasks:

1. Discovery: understand how the reporting slice works.
2. Impact analysis: assess the effect of adding USD-normalized market values to portfolio reporting.
3. Implementation: add `market_value_usd`, `unrealized_gain_usd`, and `concentration_bucket`, then validate.

The disciplined run should externalize reusable context as it goes, while the careless run should only receive the business ask. The baseline project intentionally does **not** include those task 3 columns yet. The sandbox is meant to start from a clean, working state that the agent can improve during the demo.

## Repo shape

```text
models/silver/                   cleaned source-like models
models/gold/portfolio_reporting/ relevant reporting slice for the demo
models/gold/compliance/          unrelated but plausible slice
models/gold/archived/            intentionally irrelevant decoy
analyses/                        scratch SQL that should usually be ignored
docs/                            reusable artifacts created during disciplined runs
showcase/                        prompt pairs, facilitator guide, scorecard, reference notes
scripts/                         bootstrap and reset helpers
```

## What "efficient" means here

This repo is designed so you can compare two sessions using visible proxies:

- how many files the agent inspects
- how often it repeats repository scans
- how many turns it needs
- whether it touches unrelated files
- whether it validates the result before claiming success

See [showcase/scorecard.md](showcase/scorecard.md) and [showcase/prompt_pairs.md](showcase/prompt_pairs.md).

## Resetting between runs

To restore the demo to its starting state after a live run:

```bash
uv run python scripts/reset_demo_state.py
```

That script:

- rewrites `docs/repo_map.md` to the starter template
- rewrites `docs/dbt_lineage_notes.md` to the starter template
- removes dbt build artifacts and the local DuckDB file

If you want a fresh build immediately after reset, run:

```bash
uv run python scripts/bootstrap_demo.py
```

## Validation expectations

The baseline repo should pass `dbt build` and `dbt test` before the workshop starts. During the live implementation task, a good run should also pass after scoped edits to the reporting slice.
