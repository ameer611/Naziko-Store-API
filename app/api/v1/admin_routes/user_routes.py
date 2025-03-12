from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.crud.authentication import get_user_by_phone
from app.crud.user import get_customers_from_db, get_customer_by_id_from_db, change_customer_password_on_db, \
    delete_customer_from_db
from app.db.base import get_db
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/customers", response_model=list[UserResponse], status_code=200)
async def get_customers(user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_db = await get_user_by_phone(db, user.get("phone_number"))
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    if not user_db.is_superuser:
        raise HTTPException(status_code=403, detail="Forbidden")

    customers = await get_customers_from_db(db)
    return customers


@router.get("/customers/{customer_id}", response_model=UserResponse, status_code=200)
async def get_customer_by_id(customer_id: int, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not user["is_superuser"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    customer = await get_customer_by_id_from_db(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.patch("/change-customer-password/{customer_id}", response_model=dict, status_code=200)
async def change_customer_password(customer_id: int, new_password: SecretStr, user: dict = Depends(get_current_user),
                                   db: AsyncSession = Depends(get_db)):
    if not user["is_superuser"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    customer = await get_customer_by_id_from_db(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    changed_customer = await change_customer_password_on_db(db, customer, new_password.get_secret_value())
    if not changed_customer:
        raise HTTPException(status_code=400, detail="Error changing customer password")
    return {"message": "Password changed successfully"}


@router.delete("/delete-customer/{customer_id}", response_model=dict, status_code=200)
async def delete_customer_by_id(customer_id: int, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not user["is_superuser"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    customer = await get_customer_by_id_from_db(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    message = await delete_customer_from_db(db, customer)
    return message