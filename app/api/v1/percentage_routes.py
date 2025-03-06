from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.percentage import get_percentage
from app.db.base import get_db
from app.schemas.transaction import PercentageResponse

router = APIRouter()

@router.get("/", response_model=PercentageResponse, status_code=200)
async def get_last_percentage(db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection error")

    percentage_db = get_percentage(db)
    if not percentage_db:
        raise HTTPException(status_code=404, detail="Percentage not found")
    return percentage_db