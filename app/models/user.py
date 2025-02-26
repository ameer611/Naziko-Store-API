from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLAlchemyEnum, DateTime

from app.common.enums import Language
from app.db.base import Base


class User(Base):
    """
    User model representing application users with authentication and preference details.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(255), nullable=False)
    phone_number = Column(String(13), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    tg_id = Column(String(10), nullable=True, unique=True)
    is_admin = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    language_code = Column(SQLAlchemyEnum(Language), default=Language.uz, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
