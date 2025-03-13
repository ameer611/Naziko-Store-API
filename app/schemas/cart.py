from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# ====================
# Cart Item Base Schema
# ====================
class CartItemBase(BaseModel):
    pass


# ====================
# Cart Item Create Schema
# ====================
class CartItemCreate(CartItemBase):
    product_link: str
    quantity: int = Field(..., gt=0)
    cart_id: int
    variant: Optional[dict] = None


# ====================
# Cart Item Update Schema
# ====================
class CartItemUpdate(BaseModel):
    quantity: Optional[int] = None


# ====================
# Cart Item Response Schema
# ====================
class CartItemResponse(CartItemBase):
    id: int
    product_link: str
    quantity: int
    price: float
    weight: float
    cart_id: int
    variant: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)


# ====================
# Cart Response Schema
# ====================
class CartResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    total_price: float
    total_weight: float
    cart_items: list[CartItemResponse]

    model_config = ConfigDict(from_attributes=True)