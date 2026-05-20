select
    position_key,
    account_id,
    client_name,
    risk_profile,
    advisor_region,
    report_date,
    symbol,
    security_name,
    asset_class,
    sector,
    domicile_country,
    quantity,
    position_currency,
    account_base_currency,
    cost_basis_local,
    market_value_local,
    unrealized_gain_local,
    fx_rate_to_usd,
    round(position_weight, 6) as position_weight,
    row_number() over (
        partition by account_id, report_date
        order by market_value_local desc, symbol
    ) as position_rank,
    position_currency <> account_base_currency as is_cross_currency_position
from {{ ref('portfolio_positions_base') }}
