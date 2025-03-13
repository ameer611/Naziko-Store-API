from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.order import OrderResponse
from app.schemas.user import UserResponse


# ====================
# Transaction Base Schema (Common Fields)
# ====================
class TransactionBase(BaseModel):
    amount: float
    description: Optional[str] = None
    date: datetime


# ====================
# Transaction Create Schema
# ====================
class TransactionCreate(TransactionBase):
    order_id: int


# ====================
# Transaction User Update Schema (Optional Fields)
# ====================
class TransactionUserUpdate(BaseModel):
    description: Optional[str] = None
    date: Optional[datetime] = None


# ====================
# Transaction Admin Update Schema (Optional Fields)
# ====================
class TransactionAdminUpdate(BaseModel):
    amount: Optional[float] = None
    is_approved: Optional[bool] = None


# ====================
# Transaction Response Schema
# ====================
class TransactionResponse(TransactionBase):
    id: int
    order_id: int
    image_url: str
    created_at: datetime
    is_approved: bool
    order: OrderResponse
    user: UserResponse

    model_config = ConfigDict(from_attributes=True)


# ====================
# Percentage Base Schema (Common Fields)
# ====================
class PercentageBase(BaseModel):
    percentage: float
    description: str


# ====================
# Percentage Create Schema
# ====================
class PercentageCreate(PercentageBase):
    """Schema for creating a new percentage record."""
    pass


# ====================
# Percentage Update Schema
# ====================
class PercentageUpdate(BaseModel):
    """Schema for updating percentage records (partial update)."""
    percentage: Optional[float] = None
    description: Optional[str] = None


# ====================
# Percentage Response Schema
# ====================
class PercentageResponse(PercentageBase):
    """Schema for returning percentage data."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)