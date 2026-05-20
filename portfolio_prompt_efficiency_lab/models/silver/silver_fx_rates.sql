select
    cast(rate_date as date) as rate_date,
    upper(trim(source_currency)) as source_currency,
    upper(trim(target_currency)) as target_currency,
    cast(rate_to_usd as double) as rate_to_usd,
    cast(rate_date as varchar) || '|' || upper(trim(source_currency)) || '|' || upper(trim(target_currency)) as fx_rate_key
from {{ ref('raw_fx_rates') }}
