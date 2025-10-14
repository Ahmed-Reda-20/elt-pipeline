CREATE SCHEMA IF NOT EXISTS bronze;

CREATE TABLE IF NOT EXISTS bronze.bronze_products (
    -- Store complete API response
    id SERIAL PRIMARY KEY,
    api_product_id INT,
    raw_json JSONB,   
    
    -- Data Governance & Lineage
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    source_system VARCHAR(50) DEFAULT 'fakestoreapi' NOT NULL,
    batch_id UUID,
    api_endpoint VARCHAR(100) NOT NULL,
    data_size_bytes INT NOT NULL,

    processing_status VARCHAR(20) DEFAULT 'pending',
    error_message TEXT,
    

    -- Data Quaility Constraints
    CONSTRAINT valid_batch_id CHECK (batch_id IS NOT NULL),
    CONSTRAINT valid_ingestion_time CHECK (ingestion_timestamp <= CURRENT_TIMESTAMP),
    CONSTRAINT valid_raw_json CHECK(raw_json IS NOT NULL),
    CONSTRAINT valid_api_product_id CHECK(api_product_id IS NOT NULL),
    CONSTRAINT positive_data_size CHECK (data_size_bytes > 0)



);

CREATE TABLE IF NOT EXISTS bronze.bronze_users (
    id SERIAL PRIMARY KEY,
    api_user_id INT,
    raw_json JSONB,   
    
    -- Data Governance & Lineage
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    source_system VARCHAR(50) DEFAULT 'fakestoreapi' NOT NULL,
    batch_id UUID,
    api_endpoint VARCHAR(100) NOT NULL,
    data_size_bytes INT NOT NULL,

    processing_status VARCHAR(20) DEFAULT 'pending',
    error_message TEXT,
    

    -- Data Quaility Constraints
    CONSTRAINT valid_batch_id CHECK (batch_id IS NOT NULL),
    CONSTRAINT valid_ingestion_time CHECK (ingestion_timestamp <= CURRENT_TIMESTAMP),
    CONSTRAINT valid_raw_json CHECK(raw_json IS NOT NULL),
    CONSTRAINT valid_api_user_id CHECK(api_user_id IS NOT NULL),
    CONSTRAINT positive_data_size CHECK (data_size_bytes > 0)
);

CREATE TABLE IF NOT EXISTS bronze.bronze_carts (
    id SERIAL PRIMARY KEY,
    api_cart_id INT,
    raw_json JSONB,   
    
    -- Data Governance & Lineage
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    source_system VARCHAR(50) DEFAULT 'fakestoreapi' NOT NULL,
    batch_id UUID,
    api_endpoint VARCHAR(100) NOT NULL,
    data_size_bytes INT NOT NULL,

    processing_status VARCHAR(20) DEFAULT 'pending',
    error_message TEXT,
    

    -- Data Quaility Constraints
    CONSTRAINT valid_batch_id CHECK (batch_id IS NOT NULL),
    CONSTRAINT valid_ingestion_time CHECK (ingestion_timestamp <= CURRENT_TIMESTAMP),
    CONSTRAINT valid_raw_json CHECK(raw_json IS NOT NULL),
    CONSTRAINT valid_api_cart_id CHECK(api_cart_id IS NOT NULL),
    CONSTRAINT positive_data_size CHECK (data_size_bytes > 0)
);

CREATE TABLE IF NOT EXISTS bronze.ingestion_log (
    id SERIAL PRIMARY KEY,
    batch_id UUID UNIQUE NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    source_system VARCHAR(50),
    api_endpoint VARCHAR(100),
    row_count INT,
    status VARCHAR(20) CHECK (status IN ('IN_PROGRESS', 'SUCCESS', 'FAILED')),
    error_message TEXT
);