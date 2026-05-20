select
    account_id,
    report_date,
    symbol,
    security_name,
    asset_class,
    market_value_local,
    position_weight,
    case
        when position_weight >= 0.30 then 'escalate_immediately'
        when position_weight >= 0.20 then 'review'
        else 'monitor'
    end as review_action
from {{ ref('fct_portfolio_positions') }}
where position_weight >= 0.20
