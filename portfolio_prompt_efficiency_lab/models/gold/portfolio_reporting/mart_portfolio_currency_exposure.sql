select
    account_id || '|' || cast(report_date as varchar) || '|' || position_currency as account_currency_key,
    account_id,
    report_date,
    position_currency,
    count(*) as holding_count,
    round(sum(market_value_local), 2) as currency_market_value_local,
    round(sum(position_weight), 6) as currency_weight_share
from {{ ref('fct_portfolio_positions') }}
group by 1, 2, 3, 4
