select
    trim(bucket_name) as bucket_name,
    cast(min_share as double) as min_share,
    cast(max_share as double) as max_share,
    cast(display_order as integer) as display_order
from {{ ref('raw_concentration_thresholds') }}
