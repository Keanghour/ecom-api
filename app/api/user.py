# app/api/user.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.schemas.user import ChangePasswordRequest, ResetPasswordRequest, RoleEnum, UserCreate, UserCreateAdmin, UserRequest, UserResponse, UserUpdate, UserOut, UserAuth
from app.services.user_service import (
    change_user_password,
    create_user_admin,
    deactivate_user,
    get_all_users,
    reset_user_password,
    create_user,
    update_user,
    get_user_by_id,
    authenticate_user
)
from app.db.database import get_db
from app.core.security import create_access_token, get_current_user, hash_password, is_admin, verify_password
from app.models.user import User  
from datetime import datetime, timedelta 
import logging

# Setup logger
logger = logging.getLogger("uvicorn")

# Define router with a /api/user/ prefix
router = APIRouter(prefix="/api/user", tags=["users"])

# Register new user
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Registering user: {user_data.email}")
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        logger.warning(f"Email already registered: {user_data.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user_data)

@router.post("/register/admin", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_admin(user_data: UserCreateAdmin, db: Session = Depends(get_db)):
    # Check if the email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Convert role integer to string using the RoleEnum mapping
    role_string = RoleEnum.to_string(user_data.role)

    if not role_string:
        raise HTTPException(status_code=400, detail="Invalid role value")

    # Create the admin user with the role as a string
    user_data.role = role_string  # Store the full role string (e.g., "admin")
    return create_user_admin(db, user_data)

# Update user profile
@router.put("/{user_id}", response_model=UserOut)
def update_user_profile(
    user_id: int, 
    user_data: UserUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user")
    
    logger.info(f"Updating user profile: {user_id}")
    user = update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Get user profile
@router.get("/{user_id}", response_model=UserOut)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching user profile: {user_id}")
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/all/users", response_model=list[UserResponse])
def get_all_users_route(db: Session = Depends(get_db)):
    logger.info("Fetching all users")
    users = get_all_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

# User login
@router.post("/login")
def login(user_data: UserAuth, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Convert role to string
    role = user.role.value if user.role else None
    
    access_token = create_access_token(data={"id": user.id, "sub": user.email, "role": role}, expires_delta=timedelta(hours=24))
    
    return {
        "code": 200,
        "message": "Login successful",
        "data": {
            "user_id": user.id,
            "firstName": user.firstName, 
            "lastName": user.lastName,
            "email": user.email,
            "token": access_token,
            "role": role,  
            "is_verified": user.is_active,
            "profile_picture_url": "https://example.com/path/to/profile/pic.jpg", 
            "last_login": datetime.utcnow().isoformat() 
        }
    }

@router.put("/change/password", response_model=dict)
def change_password(
    data: ChangePasswordRequest,  # Request body for old and new passwords
    db: Session = Depends(get_db),  # Database session
    current_user: User = Depends(get_current_user),  # The user extracted from the JWT
):
    """
    Change the password for the currently logged-in user.
    """
    # Get the current user ID from the authenticated token
    user_id = current_user.id
    print(f"Current authenticated user ID: {user_id}")
    
    # Verify the old password by comparing it with the stored hashed password
    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password"
        )

    # Hash the new password and update it in the database
    current_user.hashed_password = hash_password(data.new_password)
    db.commit()  # Commit the change to the database
    db.refresh(current_user)  # Refresh the current_user to get the latest data

    return {"message": "Password changed successfully"}

# Reset password
@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    # Call the service to reset the password
    reset_result = reset_user_password(db, data)
    
    return {"message": "Password reset successfully. Please check your email for the new temporary password."}

@router.patch("/deactivate/{user_id}", response_model=dict)
def deactivate_user_route(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    is_admin: bool = Depends(is_admin)  # Ensure the user is an admin
):
    """API endpoint to deactivate a user."""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Deactivate the user
    user.is_active = False
    db.commit()  # Commit the change
    db.refresh(user)  # Refresh to get the latest state

    logger.info(f"User {user_id} deactivated by admin {current_user.id}")
    return {"message": f"User {user_id} has been deactivated"}

# # Not yet implement

# from google.auth.transport import requests
# from google.oauth2 import id_token
# from google.auth.exceptions import GoogleAuthError

# # Feature flag to enable/disable Google Authentication
# GOOGLE_AUTH_ENABLED = ("GOOGLE_AUTH_ENABLED", "False").lower() == "true"

# @router.post("/authenticate")
# def authenticate_user(request: UserRequest, db: Session):
#     """
#     Authenticate user with username and password or Google OAuth (if enabled)
#     """
#     # First check for Google authentication if it's enabled
#     if GOOGLE_AUTH_ENABLED:
#         raise HTTPException(status_code=501, detail="Google authentication is not yet implemented")

#     # Regular username/password authentication
#     user = db.query(User).filter(User.username == request.username).first()
#     if user and verify_password(request.password, user.hashed_password):
#         return {"message": f"User {user.username} authenticated successfully"}
    
#     raise HTTPException(status_code=401, detail="Invalid credentials")

# @router.post("/authenticate/google")
# def authenticate_user_with_google(request: GoogleTokenRequest, db: Session):
#     """
#     Placeholder for Google Authentication logic.
#     Respond with 'Not yet implemented' if Google authentication is not enabled.
#     """
#     if not GOOGLE_AUTH_ENABLED:
#         raise HTTPException(status_code=501, detail="Google authentication is not yet implemented")

#     # Google authentication logic will go here when ready.
#     # Placeholder for now.
#     return {"message": "Google authentication logic will be implemented soon!"}