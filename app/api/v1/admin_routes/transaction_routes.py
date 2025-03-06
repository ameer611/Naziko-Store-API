from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.admin_routes.order_routes import update_order_status
from app.core.security import get_current_user
from app.crud.authentication import get_user_by_phone
from app.crud.order import get_order_by_id
from app.crud.transaction import get_transactions_from_db_for_admin, update_transaction_to_valid
from app.db.base import get_db
from app.schemas.transaction import TransactionResponse
from app.service.telegram import send_message_to_customer

router = APIRouter()


@router.get("/all-transactions", response_model=List[TransactionResponse])
async def get_all_transaction_for_admin(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_db = get_user_by_phone(db, user.get("phone_number"))
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    if not user_db.is_superuser:
        raise HTTPException(status_code=403, detail="You don't have enough permissions")

    transactions = get_transactions_from_db_for_admin(db)
    if not transactions:
        return []

    return transactions


@router.patch("/verify-transaction/{transaction_id}", response_model=TransactionResponse)
async def verify_transaction_endpoint(transaction_id: int,
                                      transaction_amount: float,
                                      user: dict = Depends(get_current_user),
                                      db: Session = Depends(get_db)):
    user_db = get_user_by_phone(db, user.get("phone_number"))
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    if not user_db.is_superuser:
        raise HTTPException(status_code=403, detail="You don't have enough permissions")

    transaction = update_transaction_to_valid(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    order_db = get_order_by_id(db, transaction.user_id, transaction.order_id)
    if not order_db:
        raise HTTPException(status_code=404, detail="Order not found")
    order_db.total_paid += transaction_amount
    db.commit()

    if transaction.user and transaction.user.tg_id:
        send_message_to_customer(transaction.user.tg_id, "Your Transaction is Verified.")
    return transaction

