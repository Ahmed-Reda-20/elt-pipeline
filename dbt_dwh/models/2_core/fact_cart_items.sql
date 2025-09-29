WITH exploded AS (
    SELECT
        cart_id,
        user_id,
        cart_date,
        jsonb_array_elements(products_array) AS product_item,  -- expand products list

        -- Metadata
        bronze_id,
        source_system,
        batch_id,
        ingestion_timestamp,
        transformation_timestamp
    FROM {{ ref('stg_carts') }}
)

SELECT
    cart_id,
    user_id,
    cart_date,
    (product_item->>'productId')::INT AS product_id,
    (product_item->>'quantity')::INT AS quantity,

    -- Metadata
    bronze_id,
    source_system,
    batch_id,
    ingestion_timestamp,
    transformation_timestamp,
    CURRENT_TIMESTAMP AS core_transformation_timestamp

FROM exploded