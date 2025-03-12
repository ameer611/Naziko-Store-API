from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.alibaba_scraper.products_scraper import get_products_list
from app.core.security import get_current_user
from app.crud.authentication import get_user_by_phone
from app.crud.product import refresh_products_on_db
from app.db.base import get_db

router = APIRouter()

@router.get("/refresh-products", response_model=dict)
async def refresh_products(current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Refresh the product list"""
    if not current_user:
        raise HTTPException(status_code=401, detail="You need to be logged in to perform this action.")

    user_db = await get_user_by_phone(db, current_user.get("phone_number"))
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found.")

    if not user_db.is_superuser:
        raise HTTPException(status_code=400, detail="You are not authorized to perform this action.")

    products = get_products_list(page_down_number=25)
    message = await refresh_products_on_db(db, products)
    return message