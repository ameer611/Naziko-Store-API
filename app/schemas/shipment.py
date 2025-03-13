from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ShipmentTypeBase(BaseModel):
    pass

class ShipmentTypeCreate(ShipmentTypeBase):
    title: str = Field(..., max_length=200)
    description: str = Field(..., max_length=255)
    days: int = Field(..., gt=0)
    cost_per_kg: float = Field(..., gt=0)

class ShipmentTypeUpdate(ShipmentTypeBase):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=255)
    days: Optional[int] = Field(None, gt=0)
    cost_per_kg: Optional[float] = Field(None, gt=0)

class ShipmentTypeResponse(ShipmentTypeBase):
    id: int
    title: str
    description: str
    days: int
    cost_per_kg: float

    model_config = ConfigDict(
        from_attributes=True
    )