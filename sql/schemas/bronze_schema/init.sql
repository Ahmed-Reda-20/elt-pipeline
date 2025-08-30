CREATE TABLE bronze_products (
    -- Store complete API response
    id SERIAL PRIMARY KEY,
    raw_json JSONB NOT NULL,   
    
    -- MetaData
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_system VARCHAR(50) DEFAULT 'fakestoreapi',
    batch_id UUID,
    api_endpoint VARCHAR(100)  
);

CREATE TABLE bronze_users (
    id SERIAL PRIMARY KEY,
    raw_json JSONB NOT NULL,
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_system VARCHAR(50) DEFAULT 'fakestoreapi',
    batch_id UUID,
    api_endpoint VARCHAR(100)
);

CREATE TABLE bronze_carts (
    id SERIAL PRIMARY KEY,
    raw_json JSONB NOT NULL,
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_system VARCHAR(50) DEFAULT 'fakestoreapi',
    batch_id UUID,
    api_endpoint VARCHAR(100)
);