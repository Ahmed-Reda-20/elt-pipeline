SELECT
    product_id,
    product_title,
    product_category,
    product_description,
    product_price,
    product_image,
    product_rating,
    product_rating_count,

    -- Metadata
    bronze_id,
    source_system,
    batch_id,
    ingestion_timestamp,
    transformation_timestamp,
    CURRENT_TIMESTAMP AS core_transformation_timestampp
FROM {{ ref('stg_products') }}
