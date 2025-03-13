from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field, condecimal

from app.common.enums import OrderStatus
from app.schemas.shipment import ShipmentTypeResponse


# ====================
# Order Items Base Schema
# ====================
class OrderItemBase(BaseModel):
    pass


# ====================
# Order Items Create Schema
# ====================
class OrderItemCreate(OrderItemBase):
    order_id: int = Field(..., gt=0)
    product_link: str
    quantity: int = Field(..., gt=0)
    variant: Optional[dict] = None


# ====================
# Order Items Response Schema
# ====================
class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    product_link: str
    quantity: int
    price: float
    weight: float

    model_config = ConfigDict(from_attributes=True)


# ====================
# Order Base Schema
# ====================
class OrderBase(BaseModel):
    pass


# ====================
# Order Create Schema
# ====================
class OrderCreate(OrderBase):
    shipment_id: int


# ====================
# Order Update Schema
# ====================
class OrderUpdateUser(OrderBase):
    shipment_id: Optional[int] = None

class OrderUpdateAdmin(OrderBase):
    status: Optional[OrderStatus] = None
    shipment_id: Optional[int] = None


# ====================
# Order Response Schema
# ====================
class OrderResponse(OrderBase):
    id: int
    user_id: int
    status: OrderStatus
    created_at: datetime
    shipment_id: int
    total_paid: condecimal(max_digits=10, decimal_places=3)
    total_price: condecimal(max_digits=10, decimal_places=3)
    total_weight: condecimal(max_digits=10, decimal_places=3)

    order_items: List[OrderItemResponse] = []
    shipment: ShipmentTypeResponse

    model_config = ConfigDict(from_attributes=True)