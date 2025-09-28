WITH source_data AS (
    SELECT 
        -- Extract cart attributes from JSON
        (raw_json->>'id')::INT as cart_id,
        (raw_json->>'userId')::INT as user_id,
        (raw_json->>'date')::TIMESTAMP as cart_date,
        raw_json->>'__v' as version,
        
        -- Extract products array
        raw_json->'products' as products_array,

        -- Metadata
        id as bronze_id,
        ingestion_timestamp,
        source_system,
        batch_id
        
    FROM {{ source('bronze', 'bronze_carts') }}
    WHERE processing_status = 'success'
)

SELECT 
    *, CURRENT_TIMESTAMP as transformation_timestamp
FROM source_data