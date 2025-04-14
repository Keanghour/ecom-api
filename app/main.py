from fastapi import FastAPI
from app.db.database import engine, Base
from app.api import user, product
from app.core.logging import LoggingMiddleware
import app.models  

# Initialize FastAPI app
app = FastAPI(title="E-Commerce API")
app.add_middleware(LoggingMiddleware)

# Create database tables on startup
Base.metadata.create_all(bind=engine)

# Include API routers separately
app.include_router(user.router)
app.include_router(product.router)
