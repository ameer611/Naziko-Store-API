from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.shipment import get_shipments_from_db, get_shipment_by_id
from app.db.base import get_db
from app.schemas.shipment import ShipmentTypeResponse

router = APIRouter()

@router.get("/shipments", response_model=list[ShipmentTypeResponse], status_code=200)
async def get_shipments(db: AsyncSession = Depends(get_db)):
    shipment_db = await get_shipments_from_db(db)
    if not shipment_db:
        return []
    return shipment_db

@router.get("/shipments/{shipment_id}", response_model=Union[ShipmentTypeResponse, dict], status_code=200)
async def get_shipment(shipment_id: int, db: AsyncSession = Depends(get_db)):
    shipment_db = await get_shipment_by_id(db, shipment_id)
    if not shipment_db:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment_db