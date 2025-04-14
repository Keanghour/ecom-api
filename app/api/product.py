# app\api\product.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.product_service import create_product, update_product, delete_product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, MessageResponse

router = APIRouter(prefix="/api/product", tags=["Product"])

# Product creation endpoint
@router.post("/add", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def add_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    try:
        product = create_product(db, product_data)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product creation failed"
            )
        return ProductResponse(
            message="Product added successfully",
            product_id=product.product_id,
            product_name=product.product_name
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Product update endpoint
@router.put("/update/{product_id}", response_model=MessageResponse)
def modify_product(product_id: str, product_data: ProductUpdate, db: Session = Depends(get_db)):
    # Update the product in the database
    product = update_product(db, product_id, product_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return MessageResponse(message="Product updated successfully", product_id=product.product_id)


# Product delete endpoint
@router.delete("/delete/{product_id}", response_model=MessageResponse)
def remove_product(product_id: str, db: Session = Depends(get_db)):
    # Delete the product from the database
    product = delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return MessageResponse(message="Product deleted successfully", product_id=product.product_id)
