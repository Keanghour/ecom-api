import pytest
from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI app
from app.schemas.product import ProductCreate, ProductUpdate
from datetime import datetime
import pytz

# Initialize test client
client = TestClient(app)

# Sample Product Data
sample_product_create = {
    "product_id": "p123",
    "product_name": "Wireless Headphones",
    "description": "Comfortable wireless headphones with noise cancellation.",
    "category": "Electronics",
    "price": 199.99,
    "currency": "USD",
    "stock_quantity": 100,
    "availability": "in_stock",
    "seo": {
        "meta_title": "Wireless Headphones - Buy Online",
        "meta_description": "Comfortable wireless headphones with noise cancellation.",
        "keywords": ["headphones", "wireless", "electronics"]
    },
    "attributes": {
        "color": "black",
        "weight": "250g",
        "dimensions": "20x15x10 cm",
        "battery_life": "20 hours",
        "bluetooth_version": "5.0",
        "material": "Plastic"
    },
    "variants": [
        {
            "variant_id": "v123",
            "color": "black",
            "price": 199.99,
            "stock_quantity": 50,
            "sku": "wh-bk-001"
        }
    ],
    "images": [
        {"image_url": "https://example.com/images/wh1.jpg", "alt_text": "Black Wireless Headphones"}
    ],
    "reviews": [
        {
            "review_id": "r123",
            "rating": 5,
            "review_text": "Excellent sound quality!",
            "author": "John Doe",
            "date": "2025-04-08T10:00:00Z"
        }
    ],
    "tags": ["headphones", "wireless", "electronics"],
    "discounts": [
        {
            "discount_type": "percentage",
            "value": 10,
            "start_date": "2025-04-01T00:00:00Z",
            "end_date": "2025-05-01T00:00:00Z"
        }
    ],
    "shipping": {
        "shipping_weight": "250g",
        "delivery_time": "3-5 days",
        "shipping_methods": ["Standard", "Express"],
        "free_shipping": False
    },
    "condition": "new",
    "seller": {
        "seller_id": "s123",
        "seller_name": "Best Electronics Store",
        "seller_rating": 4.8
    }
}

sample_product_update = {
    "product_name": "Updated Wireless Headphones",
    "description": "Updated version of the wireless headphones.",
    "category": "Electronics",
    "price": 179.99,
    "currency": "USD",
    "stock_quantity": 80,
    "availability": "in_stock",
    "seo": {
        "meta_title": "Updated Wireless Headphones",
        "meta_description": "The updated version of the wireless headphones.",
        "keywords": ["headphones", "wireless", "electronics"]
    },
    "attributes": {
        "color": "blue",
        "weight": "250g",
        "dimensions": "20x15x10 cm",
        "battery_life": "22 hours",
        "bluetooth_version": "5.0",
        "material": "Plastic"
    },
    "variants": [
        {
            "variant_id": "v124",
            "color": "blue",
            "price": 179.99,
            "stock_quantity": 80,
            "sku": "wh-bl-001"
        }
    ],
    "images": [
        {"image_url": "https://example.com/images/wh2.jpg", "alt_text": "Blue Wireless Headphones"}
    ],
    "reviews": [
        {
            "review_id": "r124",
            "rating": 4,
            "review_text": "Good sound quality.",
            "author": "Jane Doe",
            "date": "2025-04-09T10:00:00Z"
        }
    ],
    "tags": ["headphones", "wireless", "electronics"],
    "discounts": [
        {
            "discount_type": "percentage",
            "value": 15,
            "start_date": "2025-04-01T00:00:00Z",
            "end_date": "2025-05-01T00:00:00Z"
        }
    ],
    "shipping": {
        "shipping_weight": "250g",
        "delivery_time": "3-5 days",
        "shipping_methods": ["Standard", "Express"],
        "free_shipping": False
    },
    "condition": "new",
    "seller": {
        "seller_id": "s124",
        "seller_name": "Best Electronics Store",
        "seller_rating": 4.9
    }
}

# Test Product Creation
def test_add_product():
    response = client.post("/api/product/add", json=sample_product_create)
    assert response.status_code == 200
    assert response.json() == {"message": "Product added successfully", "product_id": "p123"}

# Test Product Update
def test_update_product():
    # First, create a product
    response = client.post("/api/product/add", json=sample_product_create)
    product_id = response.json()["product_id"]

    # Update the product
    response = client.put(f"/api/product/update/{product_id}", json=sample_product_update)
    assert response.status_code == 200
    assert response.json() == {"message": "Product updated successfully"}

# Test Product Deletion
def test_delete_product():
    # First, create a product
    response = client.post("/api/product/add", json=sample_product_create)
    product_id = response.json()["product_id"]

    # Delete the product
    response = client.delete(f"/api/product/delete/{product_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Product deleted successfully"}

