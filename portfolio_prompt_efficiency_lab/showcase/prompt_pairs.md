# Prompt Pairs

These prompts are written to be tool-agnostic, but they map well to Codex and Claude Code.

## Task 1: Discovery

### Careless prompt

```text
Can you review this repo and tell me how the portfolio reporting works? Create any docs you think would help.
```

### Disciplined prompt

```text
Context:
This is a small dbt + DuckDB sandbox for a live workshop about prompt efficiency.

Scope:
- models/silver/
- models/gold/portfolio_reporting/
- README.md
- AGENTS.md

Ignore:
- models/gold/compliance/
- models/gold/archived/
- analyses/
- showcase/

Goal:
Create a short reusable repository map for the portfolio reporting slice.

Constraints:
- Do not inspect ignored paths unless you can justify why.
- Do not modify any files except docs/repo_map.md.
- Keep the output under 200 lines.

Output:
Write docs/repo_map.md with:
1. high-level architecture
2. important folders
3. build and test commands
4. data flow
5. risky areas
```

## Task 2: Impact Analysis

### Careless prompt

```text
We need USD-normalized market values in portfolio reporting. Figure out what this impacts and summarize it.
```

### Disciplined prompt

```text
Context:
We want to add USD-normalized market values to the portfolio reporting slice in this dbt sandbox.

Scope:
- docs/repo_map.md
- docs/dbt_lineage_notes.md
- models/gold/portfolio_reporting/
- models/silver/silver_holdings.sql
- models/silver/silver_fx_rates.sql

Ignore:
- models/gold/compliance/
- models/gold/archived/
- analyses/

Goal:
Assess the impact of adding USD-normalized market values to portfolio reporting.

Constraints:
- First reuse docs/repo_map.md if it exists.
- Do not modify models yet.
- Expand lineage one dependency layer at a time.
- Only update docs/dbt_lineage_notes.md.

Output:
Return:
1. current behavior
2. direct upstream dependencies
3. direct downstream consumers
4. smallest safe implementation plan
5. tests to run

Also save the reusable summary to docs/dbt_lineage_notes.md.
```

## Task 3: Implementation

### Careless prompt

```text
Please add market_value_usd, unrealized_gain_usd, and concentration_bucket to the portfolio reporting outputs and make sure everything still works.
```

### Disciplined prompt

```text
Context:
This repo is a dbt + DuckDB sandbox. We already mapped the repo and captured lineage notes.

Scope:
- docs/dbt_lineage_notes.md
- models/gold/portfolio_reporting/
- models/silver/silver_concentration_thresholds.sql

Ignore:
- models/gold/compliance/
- models/gold/archived/
- analyses/
- showcase/

Goal:
Add market_value_usd, unrealized_gain_usd, and concentration_bucket to the portfolio reporting slice.

Constraints:
- First inspect the current implementation and return a smallest-safe-change plan.
- Do not edit files outside the allowed scope unless you explain why and ask first.
- Reuse the existing FX rate field instead of redesigning upstream logic.
- Validate the result with dbt before finishing.

Output:
1. current behavior
2. files you will edit
3. risks
4. implementation
5. tests run
6. remaining risks
```
