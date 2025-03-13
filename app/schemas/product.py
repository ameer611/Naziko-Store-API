from typing import Optional, List, Dict, Any

from pydantic import BaseModel, ConfigDict


# ====================
# Database Product Base Schema
# ====================
class DatabaseProductBase(BaseModel):
    title: str
    price: float
    product_link: str
    image_link: str


# ====================
# Database Product Create Schema
# ====================
class DatabaseProductCreate(DatabaseProductBase):
    pass


# ====================
# Database Product Update Schema
# ====================
class DatabaseProductUpdate(DatabaseProductBase):
    pass


# ====================
# Database Product Response Schema
# ====================
class DatabaseProductResponse(DatabaseProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductLink(BaseModel):
    product_link: str


# ====================
# Online Product Base Schema
# ====================
class OnlineProductBase(BaseModel):
    title: str
    price: float
    product_link: str
    images_links: Optional[List[str]] = []
    weight: Optional[float] = None
    description: Optional[dict] = None
    variants: Dict[str, Any] | None = None


# ====================
# Online Product Response Schema
# ====================
class OnlineProductResponse(OnlineProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
