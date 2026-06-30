with distinct_locations as (
    select distinct
        ship_city,
        ship_state,
        ship_country
    from {{ ref('stg_orders') }}
)

select
    row_number() over (order by ship_city, ship_state, ship_country) as location_id,
    ship_city,
    ship_state,
    ship_country
from distinct_locations
