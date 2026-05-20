-- Another decoy file that looks useful but is unrelated to the main workshop tasks.

select
    account_id,
    report_date,
    count(*) as flagged_positions
from {{ ref('compliance_large_positions') }}
group by 1, 2
