SELECT
    "Order ID" AS order_id,
    "Date" AS order_date,
    "Status" AS status,
    "SKU" AS sku,
    "Category" AS category,
    "Style" AS style,
    "Size" AS size,
    "Qty" AS qty,
    "Amount" AS amount,
    "ship-city" AS ship_city,
    "ship-state" AS ship_state,
    "ship-country" AS ship_country
FROM {{ source('raw', 'raw_orders') }}
WHERE "Status" ILIKE '%Shipped%'
    AND "SKU" IS NOT NULL
    AND "Date" IS NOT NULL
    AND "Qty" IS NOT NULL
    AND "Amount" IS NOT NULL
    AND "Qty" > 0
    AND "Amount" > 0
    AND "ship-city" IS NOT NULL
    AND "ship-state" IS NOT NULL
    AND "ship-country" IS NOT NULL
