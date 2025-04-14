from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Product(Base):
    __tablename__ = "products"
    
    product_id = Column(String, primary_key=True, index=True)
    product_name = Column(String)
    description = Column(Text)
    category = Column(String)
    price = Column(Float)
    currency = Column(String)
    stock_quantity = Column(Integer)
    availability = Column(String)
    average_rating = Column(Float)
    total_reviews = Column(Integer)
    condition = Column(String)
    
    # Relationships
    seo = relationship("ProductSeo", back_populates="product", uselist=False, cascade="all, delete-orphan")
    seller = relationship("ProductSeller", back_populates="products")
    shipping = relationship("ProductShipping", back_populates="product", uselist=False, cascade="all, delete-orphan")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("ProductReview", back_populates="product", cascade="all, delete-orphan")
    discounts = relationship("ProductDiscount", back_populates="product", cascade="all, delete-orphan")
    tags = relationship("ProductTag", back_populates="product", cascade="all, delete-orphan")

class ProductSeo(Base):
    __tablename__ = "product_seos"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    meta_title = Column(String)
    meta_description = Column(String)
    keywords = Column(String)
    product_id = Column(String, ForeignKey('products.product_id'))
    
    product = relationship("Product", back_populates="seo")

class ProductSeller(Base):
    __tablename__ = "product_sellers"
    
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(String, unique=True)
    seller_name = Column(String)
    seller_rating = Column(Float)
    
    # Add the foreign key that links to the Product table
    product_id = Column(String, ForeignKey('products.product_id'))
    
    # Define the relationship with Product, specifying the foreign key
    products = relationship("Product", back_populates="seller")


# ProductShipping Model
class ProductShipping(Base):
    __tablename__ = "product_shippings"
    
    id = Column(Integer, primary_key=True, index=True)
    shipping_weight = Column(String)
    delivery_time = Column(String)
    shipping_methods = Column(String)
    free_shipping = Column(Boolean)
    
    product = relationship("Product", back_populates="shipping", uselist=False)

# ProductVariant Model
class ProductVariant(Base):
    __tablename__ = "product_variants"
    
    id = Column(Integer, primary_key=True, index=True)
    variant_id = Column(String)
    color = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer)
    sku = Column(String)
    product_id = Column(String, ForeignKey('products.product_id'))
    
    product = relationship("Product", back_populates="variants")

# ProductImage Model
class ProductImage(Base):
    __tablename__ = "product_images"
    
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    alt_text = Column(String)
    product_id = Column(String, ForeignKey('products.product_id'))
    
    product = relationship("Product", back_populates="images")

# ProductReview Model
class ProductReview(Base):
    __tablename__ = "product_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(String)
    rating = Column(Integer)
    review_text = Column(String)
    author = Column(String)
    date = Column(String)
    product_id = Column(String, ForeignKey('products.product_id'))
    
    product = relationship("Product", back_populates="reviews")

# ProductDiscount Model
class ProductDiscount(Base):
    __tablename__ = "product_discounts"
    
    id = Column(Integer, primary_key=True, index=True)
    discount_type = Column(String)
    value = Column(Float)
    start_date = Column(String)
    end_date = Column(String)
    product_id = Column(String, ForeignKey('products.product_id'))
    
    product = relationship("Product", back_populates="discounts")

# ProductTag Model
class ProductTag(Base):
    __tablename__ = "product_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String)
    product_id = Column(String, ForeignKey('products.product_id'))
    
    product = relationship("Product", back_populates="tags")
