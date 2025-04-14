from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import pytz

# Define the timezone (Bangkok)
tz = pytz.timezone('Asia/Bangkok')

# Define SEO Model
class Seo(BaseModel):
    meta_title: str
    meta_description: str
    keywords: List[str]

# Define Attributes Model
class Attributes(BaseModel):
    color: str
    weight: Optional[str] = None
    dimensions: Optional[str] = None
    battery_life: Optional[str] = None
    bluetooth_version: Optional[str] = None
    material: Optional[str] = None

# Define Variant Model
class Variant(BaseModel):
    variant_id: str
    color: str
    price: float
    stock_quantity: int
    sku: str

# Define Image Model
class Image(BaseModel):
    image_url: str
    alt_text: str

# Define Review Model
class Review(BaseModel):
    review_id: str
    rating: int
    review_text: Optional[str] = None
    author: Optional[str] = None
    date: datetime = Field(default_factory=lambda: datetime.now(tz))  # Timezone-aware default

# Define Discount Model
class Discount(BaseModel):
    discount_type: str  # "percentage" or "fixed_amount"
    value: float
    start_date: datetime  # Changed to datetime
    end_date: datetime    # Changed to datetime

# Define Shipping Model
class Shipping(BaseModel):
    shipping_weight: Optional[str] = None
    delivery_time: Optional[str] = None
    shipping_methods: List[str]
    free_shipping: bool

# Define Seller Model
class Seller(BaseModel):
    seller_id: str
    seller_name: str
    seller_rating: Optional[float] = None

# Base Product Model with common fields
class ProductBase(BaseModel):
    product_id: str
    product_name: str
    description: str
    category: str
    price: float
    currency: str
    stock_quantity: int
    availability: str
    seo: Seo
    attributes: Attributes
    variants: Optional[List[Variant]] = Field(default_factory=list)
    images: Optional[List[Image]] = Field(default_factory=list)
    reviews: Optional[List[Review]] = Field(default_factory=list)
    average_rating: float
    total_reviews: int
    tags: Optional[List[str]] = Field(default_factory=list)
    discounts: Optional[List[Discount]] = Field(default_factory=list)
    shipping: Shipping
    condition: str
    seller: Seller

# Response Models
class ProductResponse(BaseModel):
    message: str
    product_id: str

class MessageResponse(BaseModel):
    message: str
    product_id: Optional[str] = None

# Create Product Model (inherits from ProductBase)
class ProductCreate(ProductBase):
    pass  # Inherits everything from ProductBase, no changes needed

# Update Product Model (inherits from ProductBase)
class ProductUpdate(ProductBase):
    pass  # Inherits everything from ProductBase, no changes needed

# Output Model for Product (including ORM and timestamps)
class ProductOut(ProductBase):
    id: int
    created_at: datetime  # Changed to datetime for better handling

    class Config:
        orm_mode = True

    def format_created_at(self):
        return self.created_at.astimezone(tz).isoformat()  # Ensure proper timezone formatting

