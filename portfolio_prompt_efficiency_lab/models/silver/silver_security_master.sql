select
    upper(trim(symbol)) as symbol,
    trim(security_name) as security_name,
    trim(asset_class) as asset_class,
    trim(sector) as sector,
    upper(trim(domicile_country)) as domicile_country,
    upper(trim(default_currency)) as default_currency
from {{ ref('raw_security_master') }}
