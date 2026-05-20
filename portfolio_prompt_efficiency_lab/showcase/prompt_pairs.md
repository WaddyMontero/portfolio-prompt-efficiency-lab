# Prompt Pairs

These prompts are written to be tool-agnostic, but they map well to Codex and Claude Code.

Use them as a two-session exercise:

- Session 1 compares discovery and impact analysis.
- Session 2 compares a follow-up implementation task that starts from a fresh agent session.
- The disciplined path should carry forward reusable artifacts from session 1. The careless path should mostly rely on rediscovery.

## Task 1: Discovery

### Careless prompt

```text
Can you review this repo and tell me how the portfolio reporting works?
```

### Disciplined prompt

```text
Context:
This is a small dbt + DuckDB sandbox for a live workshop about prompt efficiency.

Scope:
- models/silver/
- models/gold/portfolio_reporting/
- README.md

Ignore:
- models/gold/compliance/
- models/gold/archived/
- analyses/
- showcase/

Goal:
Understand the portfolio reporting slice and leave behind reusable working context for later tasks.

Constraints:
- Do not inspect ignored paths unless you can justify why.
- Do not modify any files except docs/repo_map.md and AGENTS.md.
- Keep each artifact concise and scannable.

Output:
Write:
1. docs/repo_map.md with high-level architecture, important folders, build/test commands, data flow, and risky areas
2. AGENTS.md with short repo-specific working notes for future agent sessions
```

## Task 2: Impact Analysis

### Careless prompt

```text
We need USD-normalized market values in portfolio reporting. What would this affect?
```

### Disciplined prompt

```text
Context:
We want to add USD-normalized market values to the portfolio reporting slice in this dbt sandbox. Task 1 should already have produced docs/repo_map.md and AGENTS.md.

Scope:
- AGENTS.md
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
- First reuse AGENTS.md and docs/repo_map.md if they exist.
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

## Session Reset

After task 2:

1. Keep the repo state produced by the run you are evaluating.
2. End the agent session or restart the tool so session 2 starts with no chat memory.
3. Start the follow-up implementation prompt in a fresh session.

This is the point of the exercise: disciplined prompting should leave behind better reusable context for the next session to exploit.

## Task 3: Follow-Up Implementation

### Careless prompt

```text
Please add market_value_usd, unrealized_gain_usd, and concentration_bucket to the portfolio reporting outputs and make sure everything still works.
```

### Disciplined prompt

```text
Context:
This repo is a dbt + DuckDB sandbox. A previous session should already have created AGENTS.md and captured repo/lineage notes.

Scope:
- AGENTS.md
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
- Treat this as a new session: use the saved artifacts instead of relying on earlier chat memory.
- Reuse the existing AGENTS.md and lineage notes instead of rediscovering the repo from scratch.
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
