from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.authentication import get_user_by_phone
from app.crud.cart import create_cart_on_db, create_cart_item_on_db, get_cart_by_id, \
    get_cart_item_by_id, get_carts_by_user_id
from app.db.base import get_db
from app.schemas.cart import CartResponse, CartItemCreate, CartItemResponse, CartItemUpdate

router = APIRouter()


@router.post("/create-cart", response_model=CartResponse, status_code=201)
async def create_cart(user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection error")

    user_db = get_user_by_phone(db, user.get('phone_number'))
    if not user_db:
        raise HTTPException(status_code=401, detail="You need to be logged in to perform this action.")

    cart_db = create_cart_on_db(db, user_db)
    return cart_db


@router.get("/get-carts", response_model=list[CartResponse], status_code=200)
async def get_cart(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection error")

    user_db = get_user_by_phone(db, user.get('phone_number'))
    if not user_db:
        raise HTTPException(status_code=401, detail="You need to be logged in to perform this action.")

    cart = get_carts_by_user_id(db, user.get('user_id'))
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.post("/create-cart-item", response_model=CartItemResponse, status_code=201)
async def create_cart_item(cart_item: CartItemCreate,
                           user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection error")

    user_db = get_user_by_phone(db, user.get('phone_number'))
    if not user_db:
        raise HTTPException(status_code=401, detail="You need to be logged in to perform this action.")

    cart_db = get_cart_by_id(db, cart_item.cart_id, user.get('user_id'))
    if not cart_db:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item = create_cart_item_on_db(db, cart_item, user.get("user_id"))
    if not cart_item:
        raise HTTPException(status_code=400, detail="Cart Item already exists")
    return cart_item


@router.patch("/update-cart-item", response_model=CartItemResponse, status_code=200)
async def update_cart_item(cart_item_id: int,
                           cart_item: CartItemUpdate,
                           user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection error")

    user_db = get_user_by_phone(db, user.get('phone_number'))
    if not user_db:
        raise HTTPException(status_code=401, detail="You need to be logged in to perform this action.")

    cart_item_db = get_cart_item_by_id(db, cart_item_id, user.get("user_id"))
    if not cart_item_db:
        raise HTTPException(status_code=404, detail="Cart Item not found")

    cart_item_db.quantity = cart_item.quantity
    db.commit()
    db.refresh(cart_item_db)
    return cart_item_db


@router.delete("/delete-cart-item", status_code=204)
async def delete_cart_item(cart_item_id: int,
                           user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    user_db = get_user_by_phone(db, user.get("phone_number"))
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found.")

    if not db:
        raise HTTPException(status_code=404, detail="Database not found.")

    cart_item_db = get_cart_item_by_id(db, cart_item_id, user_db.id)
    if not cart_item_db:
        raise HTTPException(status_code=404, detail="Cart item not found.")

    db.delete(cart_item_db)
    db.commit()







