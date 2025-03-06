from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.authentication import get_user_by_phone
from app.crud.percentage import create_percentage_on_db, get_percentages_from_db, update_percentage_on_db
from app.db.base import get_db
from app.schemas.transaction import PercentageCreate, PercentageResponse, PercentageUpdate

router = APIRouter()


@router.post("/create-percentage", response_model=PercentageResponse, status_code=201)
async def create_percentage(percentage: PercentageCreate,
                            current_user=Depends(get_current_user),
                            db: Session = Depends(get_db)):
    """Create a new percentage"""
    user_db = get_user_by_phone(db, current_user.get("phone_number"))
    if not user_db:
        raise HTTPException(status_code=401, detail="You need to be logged in to perform this action.")

    if not user_db.is_superuser:
        raise HTTPException(status_code=400, detail="You are not authorized to perform this action.")

    percentage = create_percentage_on_db(db, percentage)
    if not percentage:
        raise HTTPException(status_code=400, detail="Failed to create a new percentage.")
    return percentage


@router.get("/get-percentages", response_model=list[PercentageResponse], status_code=200)
async def get_percentages(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all percentages"""
    if not current_user:
        raise HTTPException(status_code=401, detail="You need to be logged in to perform this action.")
    if not current_user["is_superuser"]:
        raise HTTPException(status_code=400, detail="You are not authorized to perform this action.")

    percentages = get_percentages_from_db(db)

    # Ensure all descriptions are strings
    return [
        PercentageResponse(
            id=p.id,
            percentage=p.percentage,
            description=p.description,
            created_at=p.created_at
        )
        for p in percentages
    ]


@router.patch("/update-percentage", response_model=dict, status_code=200)
async def update_percentage(percentage_id: int, percentage: PercentageUpdate, current_user=Depends(get_current_user),
                            db: Session = Depends(get_db)):
    """Update a percentage"""
    if not current_user:
        raise HTTPException(status_code=401, detail="You need to be logged in to perform this action.")
    if not current_user["is_superuser"]:
        raise HTTPException(status_code=400, detail="You are not authorized to perform this action.")

    message = update_percentage_on_db(percentage_id, db, percentage)
    if not message:
        raise HTTPException(status_code=400, detail="Failed to update the percentage.")
    return message
