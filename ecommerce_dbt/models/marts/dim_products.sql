with distinct_products as (
    select distinct
        sku,
        category,
        style,
        size
    from {{ ref('stg_orders') }}
)

select
    row_number() over (order by sku) as product_id,
    sku,
    category,
    style,
    size
from distinct_products
