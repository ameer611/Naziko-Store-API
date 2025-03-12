from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.security import get_current_user
from app.crud.authentication import get_user_by_phone
from app.crud.cart import (
    create_cart_on_db, create_cart_item_on_db, get_cart_by_id,
    get_cart_item_by_id, get_carts_by_user_id
)
from app.db.base import get_db
from app.models import Cart  # Import the Cart model
from app.schemas.cart import CartResponse, CartItemCreate, CartItemResponse, CartItemUpdate

router = APIRouter()


@router.post("/create-cart", response_model=CartResponse, status_code=201)
async def create_cart(user: dict = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection error")

    user_db = await get_user_by_phone(db, user.get('phone_number'))
    if not user_db:
        raise HTTPException(status_code=401, detail="You need to be logged in to perform this action.")

    cart_db = await create_cart_on_db(db, user_db)

    # Explicitly load related cart_items
    cart_db = await db.execute(select(Cart).options(selectinload(Cart.cart_items)).filter(Cart.id == cart_db.id))
    cart_db = cart_db.scalars().first()

    cart_items = cart_db.cart_items
    total_price = sum(item.price * item.quantity for item in cart_items)
    total_weight = sum(item.weight * item.quantity for item in cart_items)
    return {
        "id": cart_db.id,
        "user_id": cart_db.user_id,
        "created_at": cart_db.created_at,
        "total_price": total_price,
        "total_weight": total_weight,
        "cart_items": cart_items
    }


@router.get("/get-carts", response_model=list[CartResponse], status_code=200)
async def get_cart(user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection error")

    user_db = await get_user_by_phone(db, user.get('phone_number'))
    if not user_db:
        raise HTTPException(status_code=401, detail="You need to be logged in to perform this action.")

    user_id = int(user.get('user_id'))
    carts = await get_carts_by_user_id(db, user_id)
    if not carts:
        raise HTTPException(status_code=404, detail="Cart not found")

    response = []
    for cart in carts:
        cart = await db.execute(select(Cart).options(selectinload(Cart.cart_items)).filter(Cart.id == cart.id))
        cart = cart.scalars().first()

        cart_items = cart.cart_items
        total_price = sum(item.price * item.quantity for item in cart_items)
        total_weight = sum(item.weight * item.quantity for item in cart_items)
        response.append({
            "id": cart.id,
            "user_id": cart.user_id,
            "created_at": cart.created_at,
            "total_price": total_price,
            "total_weight": total_weight,
            "cart_items": cart_items
        })

    return response


@router.post("/create-cart-item", response_model=CartItemResponse, status_code=201)
async def create_cart_item(cart_item: CartItemCreate,
                           user: dict = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection error")

    user_db = await get_user_by_phone(db, user.get('phone_number'))
    if not user_db:
        raise HTTPException(status_code=401, detail="You need to be logged in to perform this action.")

    cart_db = await get_cart_by_id(db, cart_item.cart_id, int(user.get('user_id')))
    if not cart_db:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item_db = await create_cart_item_on_db(db, cart_item, int(user.get("user_id")))
    if not cart_item_db:
        raise HTTPException(status_code=400, detail="Cart Item already exists")
    return cart_item_db


@router.patch("/update-cart-item", response_model=CartItemResponse, status_code=200)
async def update_cart_item(cart_item_id: int,
                           cart_item: CartItemUpdate,
                           user: dict = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection error")

    user_db = await get_user_by_phone(db, user.get('phone_number'))
    if not user_db:
        raise HTTPException(status_code=401, detail="You need to be logged in to perform this action.")

    cart_item_db = await get_cart_item_by_id(db, cart_item_id, int(user.get("user_id")))
    if not cart_item_db:
        raise HTTPException(status_code=404, detail="Cart Item not found")

    cart_item_db.quantity = cart_item.quantity
    await db.commit()
    await db.refresh(cart_item_db)
    return cart_item_db


@router.delete("/delete-cart-item", status_code=204)
async def delete_cart_item(cart_item_id: int,
                           user: dict = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    user_db = await get_user_by_phone(db, user.get("phone_number"))
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found.")

    if not db:
        raise HTTPException(status_code=404, detail="Database not found.")

    cart_item_db = await get_cart_item_by_id(db, cart_item_id, int(user_db.id))
    if not cart_item_db:
        raise HTTPException(status_code=404, detail="Cart item not found.")

    await db.delete(cart_item_db)
    await db.commit()