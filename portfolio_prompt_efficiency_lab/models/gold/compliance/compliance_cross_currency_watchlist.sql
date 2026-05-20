select
    account_id,
    report_date,
    symbol,
    position_currency,
    account_base_currency,
    market_value_local,
    position_weight
from {{ ref('fct_portfolio_positions') }}
where is_cross_currency_position
  and position_weight >= 0.12
order by account_id, report_date, position_weight desc
