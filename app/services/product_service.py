# app\services\product_service.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app import models
from app.schemas.product import *
from app.models.product import Product, ProductSeo, ProductVariant, ProductImage, ProductReview, ProductTag, ProductDiscount, ProductShipping, ProductSeller


def create_product(db: Session, product_data):
    try:
        # Check if seller exists, if not create
        seller = db.query(ProductSeller).filter(
            ProductSeller.seller_id == product_data.seller.seller_id
        ).first()
        
        if not seller:
            seller = ProductSeller(
                seller_id=product_data.seller.seller_id,
                seller_name=product_data.seller.seller_name,
                seller_rating=product_data.seller.seller_rating
            )
            db.add(seller)
            db.flush()  # Flush to get the ID if needed

        # Create main product
        product = Product(
            product_id=product_data.product_id,
            product_name=product_data.product_name,
            description=product_data.description,
            category=product_data.category,
            price=product_data.price,
            currency=product_data.currency,
            stock_quantity=product_data.stock_quantity,
            availability=product_data.availability,
            average_rating=product_data.average_rating,
            total_reviews=product_data.total_reviews,
            condition=product_data.condition,
            seller=seller
        )

        # Create SEO
        if product_data.seo:
            product.seo = ProductSeo(
                meta_title=product_data.seo.meta_title,
                meta_description=product_data.seo.meta_description,
                keywords=",".join(product_data.seo.keywords) if product_data.seo.keywords else None
            )

        # Create Shipping
        if product_data.shipping:
            product.shipping = ProductShipping(
                shipping_weight=product_data.shipping.shipping_weight,
                delivery_time=product_data.shipping.delivery_time,
                shipping_methods=",".join(product_data.shipping.shipping_methods),
                free_shipping=product_data.shipping.free_shipping
            )

        # Add variants
        if product_data.variants:
            product.variants = [
                ProductVariant(
                    variant_id=v.variant_id,
                    color=v.color,
                    price=v.price,
                    stock_quantity=v.stock_quantity,
                    sku=v.sku
                ) for v in product_data.variants
            ]

        # Add other relationships similarly (images, reviews, discounts, tags)
        
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    except SQLAlchemyError as e:
        db.rollback()
        raise e


def update_product(db: Session, product_id: str, product_data: ProductUpdate):
    """Update an existing product."""
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        return None

    # Update the product details
    product.name = product_data.product_name
    product.description = product_data.description
    product.category = product_data.category
    product.price = product_data.price
    product.currency = product_data.currency
    product.stock_quantity = product_data.stock_quantity
    product.availability = product_data.availability

    # Update the ProductSeo
    if product_data.seo:
        product.seo.meta_title = product_data.seo.meta_title
        product.seo.meta_description = product_data.seo.meta_description
        product.seo.keywords = ",".join(product_data.seo.keywords)

    # Update Product variants (consider not deleting everything, just updating)
    for existing_variant, new_variant in zip(product.variants, product_data.variants):
        existing_variant.variant_id = new_variant.variant_id
        existing_variant.color = new_variant.color
        existing_variant.price = new_variant.price
        existing_variant.stock_quantity = new_variant.stock_quantity
        existing_variant.sku = new_variant.sku

    # Update Product Images
    for existing_image, new_image in zip(product.images, product_data.images):
        existing_image.image_url = new_image.image_url
        existing_image.alt_text = new_image.alt_text

    # Update Product Reviews
    for existing_review, new_review in zip(product.reviews, product_data.reviews):
        existing_review.review_id = new_review.review_id
        existing_review.rating = new_review.rating
        existing_review.review_text = new_review.review_text
        existing_review.author = new_review.author
        existing_review.date = new_review.date

    # Update Product Discounts
    for existing_discount, new_discount in zip(product.discounts, product_data.discounts):
        existing_discount.discount_type = new_discount.discount_type
        existing_discount.value = new_discount.value
        existing_discount.start_date = new_discount.start_date
        existing_discount.end_date = new_discount.end_date

    # Update shipping details
    if product_data.shipping:
        product.shipping.shipping_weight = product_data.shipping.shipping_weight
        product.shipping.delivery_time = product_data.shipping.delivery_time
        product.shipping.shipping_methods = ",".join(product_data.shipping.shipping_methods)
        product.shipping.free_shipping = product_data.shipping.free_shipping

    # Update seller
    if product_data.seller:
        product.seller.seller_id = product_data.seller.seller_id
        product.seller.seller_name = product_data.seller.seller_name
        product.seller.seller_rating = product_data.seller.seller_rating

    # Update tags
    product.tags = ",".join(product_data.tags)
    product.condition = product_data.condition
    product.average_rating = product_data.average_rating
    product.total_reviews = product_data.total_reviews

    # Commit the changes
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: str):
    """Delete a product."""
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        return None

    # Optionally delete related entities
    for review in product.reviews:
        db.delete(review)
    for image in product.images:
        db.delete(image)
    for variant in product.variants:
        db.delete(variant)
    if product.shipping:
        db.delete(product.shipping)
    
    db.delete(product)
    db.commit()
    return product
