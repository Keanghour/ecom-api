# app/core/security.py

from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Dict
from fastapi import HTTPException, logger, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.core.config import settings
import logging

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="passlib")


# Password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

# JWT Token creation
def create_access_token(data: Dict, expires_delta: timedelta = timedelta(minutes=60)) -> str:
    """Create and return a JWT token with the provided data and expiration time."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# OAuth2 Password Bearer for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the token and verify expiration
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_exp": True})
        
        user_id = payload.get("id")
        sub = payload.get("sub")  # Typically the email or username
        role = payload.get("role")
        
        if user_id is None or sub is None or role is None:
            raise credentials_exception  # Missing essential claims
        
    except JWTError as e:
        logger.error(f"JWT decoding error: {e}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Error during token validation: {e}")
        raise credentials_exception

    # Fetch user from the database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


def is_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough permissions"
        )



