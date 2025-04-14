# app\services\user_service.py

import random   
import string
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.models.user import User
from app.schemas.user import *
from app.core.security import hash_password, verify_password
from datetime import datetime
import pytz
import logging

# Configure logging
logger = logging.getLogger("google_auth")

tz = pytz.timezone('Asia/Bangkok')

def get_all_users(db: Session):
    """Retrieve all users from the database."""
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user_data: UserCreate):
    hashed_pwd = hash_password(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        firstName=user_data.firstName,  
        lastName=user_data.lastName,
        phone_number=user_data.phone_number,
        hashed_password=hashed_pwd,
        created_at=datetime.now(pytz.utc).astimezone(tz)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_admin(db: Session, user_data: UserCreateAdmin):
    hashed_pwd = hash_password(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd,
        role=user_data.role,  # store the role as a string (admin, user, etc.)
        created_at=datetime.now(pytz.utc).astimezone(tz)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    if user_data.firstName:
        user.firstName = user_data.firstName
    if user_data.lastName:
        user.lastName = user_data.lastName    
    if user_data.phone_number:
        user.phone_number = user_data.phone_number
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username_or_email: str, password: str):
    user = db.query(User).filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()

    if user and verify_password(password, user.hashed_password):
        return user
    return None

def change_user_password(db: Session, user_id: str, old_password: str, new_password: str) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if user and verify_password(old_password, user.hashed_password):
        user.hashed_password = hash_password(new_password)
        db.commit()
        db.refresh(user)
        return True
    return False

def reset_user_password(db: Session, data: ResetPasswordRequest):
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Generate a temporary password
    temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    user.hashed_password = hash_password(temp_password)
    db.commit()

    # TODO: Implement an email service to send the temporary password
    print(f"Temporary password for {user.email}: {temp_password}")

    return {"message": "A temporary password has been sent to your email"}

def deactivate_user(db: Session, user_id: int):
    """Deactivates (soft deletes) a user by setting is_active to False."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    user.is_active = False  # Soft delete
    db.commit()
    db.refresh(user)
    return user


