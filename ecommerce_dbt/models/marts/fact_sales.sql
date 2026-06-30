select
    s.order_id,
    p.product_id,
    l.location_id,
    d.date_id,
    s.qty,
    s.amount,
    s.status
from {{ ref('stg_orders') }} as s
left join {{ ref('dim_products') }} as p
    on s.sku = p.sku
left join {{ ref('dim_locations') }} as l
    on s.ship_city = l.ship_city
    and s.ship_state = l.ship_state
    and s.ship_country = l.ship_country
left join {{ ref('dim_dates') }} as d
    on cast(s.order_date as date) = d.order_date
