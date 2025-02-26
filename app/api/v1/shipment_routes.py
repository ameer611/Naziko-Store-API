from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.shipment import get_shipments_from_db, get_shipment_by_id
from app.db.base import get_db
from app.schemas.shipment import ShipmentTypeResponse

router = APIRouter()

@router.get("/shipments", response_model=list[ShipmentTypeResponse], status_code=200)
async def get_shipments(db: Session = Depends(get_db)):
    shipment_db = get_shipments_from_db(db)
    if not shipment_db:
        return []
    return shipment_db

@router.get("/shipments/{shipment_id}", response_model=Union[ShipmentTypeResponse, dict], status_code=200)
async def get_shipment(shipment_id: int, db: Session = Depends(get_db)):
    shipment_db = get_shipment_by_id(db, shipment_id)
    if not shipment_db:
        return {"message":"Shipment not found"}
    return shipment_db