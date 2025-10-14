WITH source_data AS (
    SELECT 
        
        
        -- Extract user attributes from JSON
        (raw_json->>'id')::INT as user_id,
        raw_json->>'email' as email,
        raw_json->>'username' as username,
        raw_json->>'password' as password_hash,
        raw_json->>'phone' as phone,
        raw_json->>'__v' as version,
        raw_json->'name'->>'firstname' as first_name,
        raw_json->'name'->>'lastname' as last_name,
        raw_json->'address'->>'city' as city,
        raw_json->'address'->>'street' as street,
        (raw_json->'address'->>'number')::INT as address_number,
        raw_json->'address'->>'zipcode' as zipcode,
        (raw_json->'address'->'geolocation'->>'lat')::DECIMAL(9,6) as latitude,
        (raw_json->'address'->'geolocation'->>'long')::DECIMAL(9,6) as longitude,
        
        --metadata
        id as bronze_id,
        source_system,
        batch_id,
        ingestion_timestamp

    FROM {{ source('bronze', 'bronze_users') }}
    WHERE processing_status = 'success'
)

SELECT 
    *, CURRENT_TIMESTAMP as transformation_timestamp
FROM source_data