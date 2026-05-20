with joined as (
    select
        h.position_key,
        h.account_id,
        a.client_name,
        a.risk_profile,
        a.base_currency as account_base_currency,
        a.advisor_region,
        h.report_date,
        h.symbol,
        s.security_name,
        s.asset_class,
        s.sector,
        s.domicile_country,
        h.quantity,
        h.currency as position_currency,
        h.cost_basis_local,
        h.market_value_local,
        h.market_value_local - h.cost_basis_local as unrealized_gain_local,
        fx.rate_to_usd as fx_rate_to_usd
    from {{ ref('silver_holdings') }} as h
    inner join {{ ref('silver_accounts') }} as a
        on h.account_id = a.account_id
    inner join {{ ref('silver_security_master') }} as s
        on h.symbol = s.symbol
    left join {{ ref('silver_fx_rates') }} as fx
        on h.report_date = fx.rate_date
       and h.currency = fx.source_currency
       and fx.target_currency = 'USD'
)

select
    *,
    market_value_local / nullif(sum(market_value_local) over (partition by account_id, report_date), 0) as position_weight
from joined
