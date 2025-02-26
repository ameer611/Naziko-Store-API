from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.cart import create_cart_on_db, create_cart_item_on_db, get_cart_by_id, \
    get_cart_item_by_id, get_carts_by_user_id
from app.db.base import get_db
from app.schemas.cart import CartResponse, CartItemCreate, CartItemResponse

router = APIRouter()


@router.post("/create-cart", response_model=CartResponse, status_code=201)
async def create_cart(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection error")
    cart_db = create_cart_on_db(db, user)
    return cart_db


@router.get("/get-carts", response_model=list[CartResponse], status_code=200)
async def get_cart(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection error")
    cart = get_carts_by_user_id(db, user.get('user_id'))
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.post("/create-cart-item", response_model=CartItemResponse, status_code=201)
async def create_cart_item(cart_item: CartItemCreate, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection error")
    message = get_cart_by_id(db, cart_item.cart_id, user.get('user_id'))
    if not message:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_item = create_cart_item_on_db(db, cart_item, user.get("user_id"))
    if not cart_item:
        raise HTTPException(status_code=400, detail="Cart Item already exists")
    return cart_item


@router.get("/get-cart-item", response_model=CartItemResponse, status_code=200)
async def get_cart_item(cart_item_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection error")
    cart_item = get_cart_item_by_id(db, cart_item_id, user.get('user_id'))
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart Item not found")
    return cart_item


