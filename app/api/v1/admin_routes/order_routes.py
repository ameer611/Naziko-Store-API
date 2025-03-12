from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import OrderStatus
from app.core.security import get_current_user
from app.crud.authentication import get_user_by_phone
from app.crud.order import get_order_by_id
from app.crud.user import get_user_by_id
from app.db.base import get_db
from app.service.telegram import send_message_to_customer

router = APIRouter()


@router.patch("/update-status", response_model=dict, status_code=200)
async def update_order_status(order_id: int,
                              status: OrderStatus,
                              user: dict = Depends(get_current_user),
                              db: AsyncSession = Depends(get_db)):
    user_db = await get_user_by_phone(db, user.get("phone_number"))
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found.")

    if not user_db.is_superuser:
        raise HTTPException(status_code=403, detail="You don't have enough permissions.")

    order = await get_order_by_id(db, user_db.id, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")

    order.status = status
    await db.commit()

    customer_db = await get_user_by_id(db, order.user_id)
    send_message_to_customer(customer_db.tg_id, f"Your order updated to {status.value.upper()}")

    return {"message": "Order status updated successfully."}