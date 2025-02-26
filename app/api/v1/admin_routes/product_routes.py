from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.alibaba_scraper.products_scraper import get_products_list
from app.core.security import get_current_user
from app.crud.product import refresh_products_on_db
from app.db.base import get_db

router = APIRouter()

@router.get("/refresh-products", response_model=dict)
async def refresh_products(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Refresh the product list"""
    if not current_user:
        raise HTTPException(status_code=401, detail="You need to be logged in to perform this action.")
    if not current_user["is_superuser"]:
        raise HTTPException(status_code=400, detail="You are not authorized to perform this action.")
    products = get_products_list(page_down_number=25)
    message = await refresh_products_on_db(db, products)
    return message



