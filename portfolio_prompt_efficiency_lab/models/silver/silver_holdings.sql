select
    upper(trim(account_id)) as account_id,
    upper(trim(symbol)) as symbol,
    cast(report_date as date) as report_date,
    cast(quantity as integer) as quantity,
    cast(cost_basis_local as double) as cost_basis_local,
    cast(market_value_local as double) as market_value_local,
    upper(trim(currency)) as currency,
    upper(trim(account_id)) || '|' || cast(report_date as varchar) || '|' || upper(trim(symbol)) as position_key
from {{ ref('raw_holdings') }}
