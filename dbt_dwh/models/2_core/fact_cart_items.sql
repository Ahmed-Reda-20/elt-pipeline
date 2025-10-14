-- models/2_core/fact_cart_items.sql
{{ config(materialized='table') }}

WITH exploded_carts AS (
    SELECT
        cart_id,
        user_id,
        cart_date,
        jsonb_array_elements(products_array) AS product_item,
        -- Metadata
        bronze_id,
        source_system,
        batch_id,
        ingestion_timestamp,
        transformation_timestamp
    FROM {{ ref('stg_carts') }}
),

cart_items_base AS (
    SELECT
        row_number() over() as cart_item_id,
        user_id,
        cart_id,
        (product_item->>'productId')::INT AS product_id,
        cart_date,
        (product_item->>'quantity')::INT AS quantity,
        -- Metadata
        bronze_id,
        source_system,
        batch_id,
        ingestion_timestamp,
        transformation_timestamp
    FROM exploded_carts
)

SELECT
    ci.cart_item_id,
    ci.user_id,
    ci.cart_id,
    ci.product_id,
    ci.cart_date,
    ci.quantity,
    
    -- PRODUCT DETAILS from stg_products
    p.product_price,
    p.product_rating,  
    p.product_rating_count,
    
    -- Metadata
    ci.bronze_id,
    ci.source_system,
    ci.batch_id,
    ci.ingestion_timestamp,
    ci.transformation_timestamp,
    CURRENT_TIMESTAMP AS core_transformation_timestamp

FROM cart_items_base ci
LEFT JOIN {{ ref('stg_products') }} p ON ci.product_id = p.product_id