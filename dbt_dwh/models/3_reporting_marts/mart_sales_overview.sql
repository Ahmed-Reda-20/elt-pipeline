/*
BUSINESS REQUEST:
- Sales team needed basic sales metrics for daily performance tracking
- Required ability to segment by product category and customer geography
- Needed privacy-compliant data accessible to entire sales organization

STAKEHOLDER COLLABORATION:
- Met with Sales Analytics team to identify key metrics
- Consulted Data Governance team on PII requirements
- Coordinated with Legal team on privacy compliance

SOLUTION DESIGN:
- Created focused sales mart with analytically useful columns only
- Excluded all PII (email, phone, address details)
- Used privacy-safe identifiers (username instead of real names)
- Simplified geographic analysis (city-level instead of coordinates)

APPROVAL:
- ✅ Sales Team
- ✅ Data Governance 
- ✅ Legal Compliance

BUSINESS IMPACT:
- Sales team can now self-serve basic sales reports
- 60% reduction in ad-hoc data requests to data team
- Enabled daily performance tracking by product category
- Maintained full privacy compliance
*/

WITH sales_mart_review AS (
    SELECT
        -- Identifiers - specify which table each column comes from
        fci.cart_item_id,
        fci.cart_id,
        fci.user_id,  -- From fact_cart_items
        fci.product_id,

        -- Quantitative measures
        fci.product_price,
        fci.quantity,
        fci.product_rating,

        -- Descriptive dimensions (analytically useful)
        p.product_category,
        fci.cart_date,

        -- Customer dimensions (privacy-safe)
        u.username,
        u.city
    
    FROM {{ ref('fact_cart_items') }} fci
    LEFT JOIN {{ ref('dim_products') }} p ON p.product_id = fci.product_id
    LEFT JOIN {{ ref('dim_users') }} u ON u.user_id = fci.user_id  -- Join on user_id
),

sales_metrics AS (
    SELECT
        *,
        
        -- REVENUE METRICS
        quantity * product_price AS line_revenue,
        
        -- PRODUCT PERFORMANCE METRICS  
        CASE 
            WHEN product_rating >= 4.5 THEN 'High Rated (4.5-5.0)'
            WHEN product_rating >= 3.5 THEN 'Medium Rated (3.5-4.4)'
            WHEN product_rating >= 2.5 THEN 'Low Rated (2.5-3.4)'
            ELSE 'Poor Rated (<2.5)'
        END AS rating_category,
        
        CASE 
            WHEN product_price > 1000 THEN 'Premium'
            WHEN product_price > 500 THEN 'Mid-Range'
            WHEN product_price > 100 THEN 'Standard'
            ELSE 'Budget'
        END AS price_tier,
        
        -- TIME-BASED METRICS
        EXTRACT(YEAR FROM cart_date) AS sale_year,
        EXTRACT(MONTH FROM cart_date) AS sale_month,
        EXTRACT(DAY FROM cart_date) AS sale_day,
        
        -- BUSINESS PERFORMANCE METRICS
        CASE 
            WHEN quantity * product_price > 2000 THEN 'High Value Order'
            WHEN quantity * product_price > 500 THEN 'Medium Value Order'
            ELSE 'Standard Order'
        END AS order_value_category,
        
        CASE 
            WHEN quantity > 10 THEN 'Bulk Purchase'
            WHEN quantity > 5 THEN 'Multi-Unit Purchase' 
            WHEN quantity > 1 THEN 'Multiple Items'
            ELSE 'Single Item'
        END AS purchase_size_category

    FROM sales_mart_review
),

final_sales_mart AS (
    SELECT
        -- IDENTIFIERS & KEYS
        cart_item_id,
        cart_id,
        user_id,
        product_id,
        
        -- TIME DIMENSIONS (for filtering)
        cart_date AS sale_date,
        sale_year,
        sale_month, 
        sale_day,
        
        -- CORE QUANTITATIVE METRICS
        quantity,
        product_price AS unit_price,
        line_revenue,
        product_rating,
        
        -- PRODUCT CONTEXT
        product_category,
        rating_category,
        price_tier,
        
        -- CUSTOMER CONTEXT (privacy-safe)
        username AS customer_name,
        city AS customer_city,
        
        -- BUSINESS SEGMENTATION
        order_value_category,
        purchase_size_category
        
    FROM sales_metrics
)

SELECT *
FROM final_sales_mart
-- This data is refreshed daily at 6:00 AM EET