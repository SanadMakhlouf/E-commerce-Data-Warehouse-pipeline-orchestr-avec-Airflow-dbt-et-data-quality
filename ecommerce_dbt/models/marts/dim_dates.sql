with distinct_dates as (
    select distinct
        cast(order_date as date) as order_date
    from {{ ref('stg_orders') }}
)

select
    row_number() over (order by order_date) as date_id,
    order_date,
    extract(year from order_date)::int as year,
    extract(month from order_date)::int as month,
    extract(day from order_date)::int as day,
    trim(to_char(order_date, 'Day')) as day_name
from distinct_dates
