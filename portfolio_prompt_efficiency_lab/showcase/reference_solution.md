# Reference Solution Boundary

This file is for rehearsal and facilitation, not for the live agent prompt.

## Expected scope for task 3

A good implementation should usually stay inside:

- `models/gold/portfolio_reporting/fct_portfolio_positions.sql`
- `models/gold/portfolio_reporting/mart_portfolio_account_summary.sql`
- `models/gold/portfolio_reporting/mart_portfolio_currency_exposure.sql`
- `models/gold/portfolio_reporting/_portfolio_reporting.yml`

It may also inspect:

- `models/gold/portfolio_reporting/portfolio_positions_base.sql`
- `models/silver/silver_concentration_thresholds.sql`

## Expected logic

- `market_value_usd = market_value_local * fx_rate_to_usd`
- `unrealized_gain_usd = unrealized_gain_local * fx_rate_to_usd`
- `concentration_bucket` should map from `position_weight` using the threshold table
- downstream summaries should keep existing local-currency metrics and add USD-aware rollups where needed

## Expected validation

- `uv run dbt build`
- `uv run dbt test`

## Anti-patterns to call out

- touching compliance models without a clear reason
- redesigning the silver layer when the existing FX field already supports the task
- skipping validation after editing
