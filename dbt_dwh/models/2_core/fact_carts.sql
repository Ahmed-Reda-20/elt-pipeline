SELECT
    cart_id,
    user_id,
    cart_date,
    version,

    -- Metadata
    bronze_id,
    source_system,
    batch_id,
    ingestion_timestamp,
    transformation_timestamp,
    CURRENT_TIMESTAMP AS core_transformation_timestamp
FROM {{ ref('stg_carts') }}
