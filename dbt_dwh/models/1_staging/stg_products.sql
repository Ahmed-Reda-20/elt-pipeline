with source_data as (
    SELECT
        -- extract product data from JSON responses
        (raw_json->>'id')::INT as product_id,
        raw_json->>'title' as product_title,
        (raw_json->>'price')::DECIMAL(10,2) AS product_price,
        raw_json->>'description' as product_description,
        raw_json->>'category' as product_category,
        raw_json->>'image' as product_image,
        (raw_json->'rating'->>'rate')::DECIMAL(3,2) as product_rating,
        (raw_json->'rating'->>'count')::INT as product_rating_count,

        --metadata
        id as bronze_id,
        source_system,
        batch_id,
        ingestion_timestamp

    FROM {{ source('bronze','bronze_products') }}
    WHERE processing_status = 'success'
)
SELECT *, CURRENT_TIMESTAMP as transformation_timestamp
FROM source_data