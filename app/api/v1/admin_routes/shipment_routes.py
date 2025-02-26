from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.shipment import create_shipment_type_on_db, get_shipment_by_id, update_shipment_on_db
from app.db.base import get_db
from app.schemas.shipment import ShipmentTypeCreate, ShipmentTypeResponse, ShipmentTypeUpdate

router = APIRouter()

@router.post("/create-shipment", response_model=ShipmentTypeResponse, status_code=201)
async def create_shipment(shipment: ShipmentTypeCreate, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.get("is_superuser"):
        raise HTTPException(status_code=403, detail="You are not allowed to create shipment types")
    shipment_db = create_shipment_type_on_db(db, shipment)
    if not shipment_db:
        raise HTTPException(status_code=400, detail="Error creating shipment type")
    return shipment_db

@router.patch("/update-shipment/{shipment_id}", response_model=ShipmentTypeResponse, status_code=200)
async def update_shipment(shipment_id: int, shipment: ShipmentTypeUpdate, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.get("is_superuser"):
        raise HTTPException(status_code=403, detail="You are not allowed to update shipment types")
    shipment_db = get_shipment_by_id(db, shipment_id)
    if not shipment_db:
        raise HTTPException(status_code=404, detail="Shipment not found")
    changed_shipment = update_shipment_on_db(db, shipment_db, shipment)
    if not changed_shipment:
        raise HTTPException(status_code=400, detail="Error updating shipment type")
    return shipment_db