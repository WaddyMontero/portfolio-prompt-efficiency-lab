-- Scratch query for ad hoc investigation.
-- This file is intentionally not part of the main reporting flow.

select *
from {{ ref('fct_portfolio_positions') }}
order by account_id, report_date, position_rank
