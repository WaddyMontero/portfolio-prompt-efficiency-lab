{% test portfolio_weights_sum_to_one(model, group_by_columns, weight_column, tolerance=0.00001) %}

with grouped as (
    select
        {% for column in group_by_columns -%}
        {{ column }}{% if not loop.last %}, {% endif %}
        {%- endfor %},
        sum({{ weight_column }}) as total_weight
    from {{ model }}
    group by
        {% for column in group_by_columns -%}
        {{ loop.index }}{% if not loop.last %}, {% endif %}
        {%- endfor %}
)

select *
from grouped
where abs(total_weight - 1.0) > {{ tolerance }}

{% endtest %}
