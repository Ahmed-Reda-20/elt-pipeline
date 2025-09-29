SELECT
    user_id,
    first_name,
    last_name,
    email,
    username,
    phone,
    city,
    street,
    address_number,
    zipcode,
    latitude,
    longitude

     -- Metadata
    bronze_id,
    source_system,
    batch_id,
    ingestion_timestamp,
    transformation_timestamp,
    CURRENT_TIMESTAMP AS core_transformation_timestamp
FROM {{ ref('stg_users') }}
