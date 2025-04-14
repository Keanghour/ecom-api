# app/schemas/__init__.py

# Import all schema classes to ensure they are available for the app
from .user import (
    UserBase,
    UserCreate,
    UserCreateAdmin,
    UserUpdate,
    UserOut,
    UserAuth,
    ChangePasswordRequest,
    ResetPasswordRequest,
    UserRequest,
    UserResponse
)

from .product import (
    Seo,
    Attributes,
    Variant,
    Image,
    Review,
    Discount,
    Shipping,
    Seller,
    ProductBase,
    ProductCreate,
    ProductUpdate,
    ProductOut
)
