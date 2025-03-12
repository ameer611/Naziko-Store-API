from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.percentage import get_percentage
from app.db.base import get_db
from app.schemas.transaction import PercentageResponse

router = APIRouter()

@router.get("/", response_model=PercentageResponse, status_code=200)
async def get_last_percentage(db: AsyncSession = Depends(get_db)):
    percentage_db = await get_percentage(db)
    if not percentage_db:
        raise HTTPException(status_code=404, detail="Percentage not found")
    return percentage_db