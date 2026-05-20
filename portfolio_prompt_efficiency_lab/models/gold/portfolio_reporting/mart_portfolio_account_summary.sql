select
    account_id || '|' || cast(report_date as varchar) as account_report_key,
    account_id,
    client_name,
    risk_profile,
    advisor_region,
    report_date,
    count(*) as holding_count,
    round(sum(market_value_local), 2) as total_market_value_local,
    sum(case when is_cross_currency_position then 1 else 0 end) as cross_currency_holding_count,
    round(max(position_weight), 6) as largest_position_weight,
    max(case when position_rank = 1 then symbol end) as largest_holding_symbol
from {{ ref('fct_portfolio_positions') }}
group by 1, 2, 3, 4, 5, 6
