from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.authentication import get_user_by_phone
from app.crud.order import create_order_on_db, get_orders_from_db, get_order_by_id, delete_order_from_db, \
    create_order_item_on_db
from app.crud.shipment import get_shipment_by_id
from app.db.base import get_db
from app.schemas.order import OrderResponse, OrderCreate, OrderItemCreate, OrderItemResponse

router = APIRouter()


@router.post("/create-order", response_model=OrderResponse, status_code=201)
async def create_order(order: OrderCreate, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_db = get_user_by_phone(db, user.get("phone_number"))
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    if not db:
        raise HTTPException(status_code=404, detail="Database connection error")

    shipment_db = get_shipment_by_id(db, order.shipment_id)
    if not shipment_db:
        raise HTTPException(status_code=404, detail="Shipment not found")

    order_db = create_order_on_db(db, order, user.get("user_id"))
    if not order_db:
        raise HTTPException(status_code=400, detail="Error creating order")

    return order_db


@router.get("/orders", response_model=list[OrderResponse], status_code=200)
async def get_orders(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=404, detail="Orders not found")

    user_db = get_user_by_phone(db, user.get("phone_number"))
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    orders = get_orders_from_db(db, user.get("user_id"))
    if not orders:
        return []

    return orders


@router.delete("/delete-order/{order_id}", status_code=204)
async def delete_order(order_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=404, detail="Order not found")

    user_db = get_user_by_phone(db, user.get("phone_number"))
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    order = get_order_by_id(db, user.get("user_id"), order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    message = delete_order_from_db(db, order_id)
    if not message:
        raise HTTPException(status_code=400, detail="Error deleting order")


@router.get("/get-order/{order_id}", response_model=Union[OrderResponse, dict], status_code=200)
async def get_order(order_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=404, detail="Order not found")

    user_db = get_user_by_phone(db, user.get("phone_number"))
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    order = get_order_by_id(db, user.get("user_id"), order_id)
    if not order:
        return {"message": "Order not found"}

    return order


@router.post("/create-order-item", response_model=OrderItemResponse, status_code=201)
async def create_order_item(order_item: OrderItemCreate,
                            user: dict = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=404, detail="Order not found")

    user_db = get_user_by_phone(db, user.get("phone_number"))
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    order_db = get_order_by_id(db, user.get("user_id"), order_item.order_id)
    if not order_db:
        raise HTTPException(status_code=404, detail="Order not found")

    order_item_db = create_order_item_on_db(db, order_item)
    if not order_item_db:
        raise HTTPException(status_code=400, detail="Error creating order item")

    return order_item_db
