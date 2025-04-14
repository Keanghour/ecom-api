# app/models/__init__.py

# Import all models to ensure they are registered with SQLAlchemy
from .user import User
from .product import (
    Product,
    ProductVariant,
    ProductImage,
    ProductReview,
    ProductTag,
    ProductDiscount,
    ProductShipping,
    ProductSeller
)
