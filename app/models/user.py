# app\models\user.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum  
from datetime import datetime
import pytz
from app.db.database import Base
from app.schemas.user import RoleEnum  

# Timezone configuration for Asia/Bangkok
tz = pytz.timezone('Asia/Bangkok')

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    firstName = Column(String, nullable=True)
    lastName = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)

    role = Column(SQLEnum(RoleEnum), default=RoleEnum.user)
    phone_number = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)  
    hashed_password = Column(String, nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(pytz.utc).astimezone(tz), onupdate=lambda: datetime.now(pytz.utc).astimezone(tz))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.utc).astimezone(tz))

    # Relationship (if needed)
    # orders = relationship("Order", back_populates="user")  # If you have an Order model
