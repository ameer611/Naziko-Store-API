from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user, hash_password
from app.crud.authentication import get_user_by_phone
from app.crud.user import (
    change_user_info_on_db, check_passwords, change_user_password_on_db, change_phone_number_on_db
)
from app.db.base import get_db
from app.models import User
from app.schemas.user import UserResponse, UserUpdate, UserPasswordUpdate, UserPhoneNumberUpdate

router = APIRouter()


@router.get("/", response_model=UserResponse, status_code=200)
async def get_profile(user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection error")
    user_db = await get_user_by_phone(db, user["phone_number"])
    if not user_db:
        return {"message": "You need to be logged in to perform this action."}
    return user_db


@router.patch("/change-info", response_model=UserResponse, status_code=200)
async def change_user_info(changed_info: UserUpdate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    changed_user = await change_user_info_on_db(db, int(user["user_id"]), changed_info)

    if not changed_user:
        return {"message": "User not found"}
    return changed_user


@router.patch("/change-password", response_model=UserResponse, status_code=200)
async def change_user_password(changed_info: UserPasswordUpdate, user=Depends(get_current_user),
                               db: AsyncSession = Depends(get_db)):
    if not await check_passwords(changed_info.old_password, int(user["user_id"]), db):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    changed_user = await change_user_password_on_db(db, int(user["user_id"]), changed_info)

    if not changed_user:
        return {"message": "User not found"}
    return changed_user


@router.patch("/change-phone", response_model=UserResponse, status_code=200)
async def change_user_phone(changed_info: UserPhoneNumberUpdate, user=Depends(get_current_user),
                            db: AsyncSession = Depends(get_db)):
    if not await check_passwords(changed_info.password, int(user["user_id"]), db):
        raise HTTPException(status_code=400, detail="Password is incorrect")
    changed_user = await change_phone_number_on_db(db, int(user["user_id"]), changed_info.new_phone_number)

    if not changed_user:
        return {"message": "User not found"}
    return changed_user


@router.post("/add-super-user", response_model=UserResponse, status_code=200)
async def add_super_admin(user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection error")

    # Ensure that only an authorized user (for example, an existing superuser) can create a new super admin
    if not user:
        raise HTTPException(status_code=403, detail="Not authorized to create a super admin")

    # Check if a user with the same email already exists
    result = await db.execute(select(User).filter(User.phone_number == user["phone_number"]))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Super admin already exists")

    # Create a new User instance for the super admin
    existing_user.is_superuser = True

    db.add(existing_user)
    await db.commit()
    await db.refresh(existing_user)

    return existing_user