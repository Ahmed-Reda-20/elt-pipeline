"""
FakeStore API Integration Testing Suite

This module validates API endpoints and data schemas before ETL pipeline development.
Ensures data contracts are met and establishes performance baselines for production monitoring.

Author: [Ahmed Reda]
Purpose: Pre-pipeline validation for Bronze layer data ingestion
"""

import requests
import time

# API Configuration
base_url = "https://fakestoreapi.com"

# Data Schema Definitions
# These schemas define the expected structure and data types for each API endpoint
# Used for data validation before pipeline development

product_schema = {
    "id": int,
    "title": str,
    "price": (int, float, str),
    "description": str,
    "category": str,
    "image": str,
    "rating": {
        "rate": (int, float),
        "count": int
    }
}

user_schema = {
    "id": int,
    "email": str,
    "username": str,
    "password": str,
    "phone": str,
    "__v": int,
    "name": {
        "firstname": str,
        "lastname": str
    },
    "address": {
        "city": str,
        "street": str,
        "number": int,
        "zipcode": str,
        "geolocation": {
            "lat": (str,float, int),
            "long": (str,float, int)
        }
    }
}

cart_schema = {
    "id": int,
    "userId": int,
    "date": str,
    "__v": int,
    "products": [
        {
            "productId": int,
            "quantity": int
        }
    ]
}

#recursive helper funciton
def validate_schema(data, schema):
    """
    Recursively validate data structure against expected schema structure

    Args:
        data (dict): The data object to validate
        schema (dict): The expected schema definition

    Raises:
        AssertionError: If data doesn't match expected schema

    """

    for key, expected_type in schema.items():
        # Check if required key exists
        assert key in data, f"Missing key: {key}"
        value = data[key]

        # Handle nested dictionary validation
        if isinstance(expected_type, dict):
            assert isinstance(value, dict), f"Key: '{key}' should be a dict"
            validate_schema(value, expected_type)
        #handle list validation while checking and validating for dictionaries and normal types (int,str,float,etc..) inside the list
        elif isinstance(expected_type, list):
            assert isinstance(value, list), f"Key: '{key}' should be a list"
            if expected_type:
                schema_blueprint = expected_type[0]
                for item in value:
                    if isinstance(schema_blueprint, dict):
                        assert isinstance(item, dict)
                        validate_schema(item, schema_blueprint)
                    else:
                        assert isinstance(item, schema_blueprint), f"Each item in '{key}' should be of type {schema_blueprint.__name__}"

        else:
            assert isinstance(value, expected_type), f"Key '{key}' should be of type {expected_type.__name__}, got {type(value).__name__}"


        
def test_product_api():
    """
    Test Products API endpoint for data structure and performance.
    
    Validates:
    - HTTP response status
    - Response format (list of objects)
    - Each product object schema
    - API response time performance
    
    Critical for pipeline reliability.
    """

    # Make API request and calculating response time
    start_time = time.time()
    response = requests.get(f"{base_url}/products")
    response_time = time.time() - start_time

    # Validate HTTP response
    assert response.status_code == 200, f"API returned {response.status_code}"
    # Parse and validate response structure
    data = response.json()
    assert isinstance(data, list), "Products should return a list"
    assert len(data) > 0, "Should have at least one product"

    # Validate each cart against expected schema
    for product in data:
        validate_schema(product, product_schema)

    # Log performance metrics for pipeline planning
    print(f"📊 Products API response time: {response_time:.3f}s ({len(data)} records)")

def test_user_api():
    """
    Test Users API endpoint for data structure and performance.
    
    Validates:
    - HTTP response status  
    - Response format (list of objects)
    - Each user object schema including nested address/name objects
    - API response time performance
    
    Critical for pipeline reliability.
    """

    # Make API request and calculating response time
    start_time = time.time()
    response = requests.get(f"{base_url}/users")
    response_time = time.time() - start_time

    # Validate HTTP response
    assert response.status_code == 200, f"API returned {response.status_code}"
    # Parse and validate response structure
    data = response.json()
    assert isinstance(data, list), "Users should return a list"
    assert len(data) > 0, "Should have at least one user"

    # Validate each cart against expected schema
    for user in data:
            validate_schema(user, user_schema)
    
    # Log performance metrics for pipeline planning
    print(f"📊 Users API response time: {response_time:.3f}s ({len(data)} records)")

def test_cart_api():
    """
    Test Carts API endpoint for data structure and performance.
    
    Validates:
    - HTTP response status
    - Response format (list of objects)  
    - Each cart object schema including nested products array
    - API response time performance
    
    Critical for pipeline reliability.
    """

    # Make API request and calculating response time
    start_time = time.time()
    response = requests.get(f"{base_url}/carts")
    response_time = time.time() - start_time

    # Validate HTTP response
    assert response.status_code == 200, f"API returned {response.status_code}"
    # Parse and validate response structure
    data = response.json()
    assert isinstance(data, list), "Carts should return a list"
    assert len(data) > 0, "Should have at least one cart"

    # Validate each cart against expected schema
    for cart in data:
            validate_schema(cart, cart_schema)

    # Log performance metrics for pipeline planning
    print(f"📊 Carts API response time: {response_time:.3f}s ({len(data)} records)")