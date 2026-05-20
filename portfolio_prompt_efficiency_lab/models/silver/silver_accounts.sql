select
    upper(trim(account_id)) as account_id,
    trim(client_name) as client_name,
    lower(trim(risk_profile)) as risk_profile,
    upper(trim(base_currency)) as base_currency,
    upper(trim(advisor_region)) as advisor_region
from {{ ref('raw_accounts') }}
