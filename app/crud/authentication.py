from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.code_generator import generate_code
from app.models.user import User
from app.models.verification_code import VerificationCode
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password


async def create_user(db: AsyncSession, user_data: UserCreate):
    """
    Create a new user in the database
    """
    hashed_password = hash_password(user_data.password)
    db_user = User(
        fullname=user_data.fullname,
        phone_number=user_data.phone_number,
        password_hash=hashed_password,
        tg_id=user_data.tg_id
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_phone(db: AsyncSession, phone_number: str):
    """
    Get user by phone number
    """
    result = await db.execute(select(User).filter(User.phone_number == phone_number))
    return result.scalars().first()


async def get_user_tg_id(db: AsyncSession, tg_id: str):
    """
    Get user by telegram ID
    """
    if not tg_id:
        return None

    result = await db.execute(select(User).filter(User.tg_id == tg_id))
    return result.scalars().first()


async def get_verification_code(db: AsyncSession, user):
    """
    Get verification code for a user
    """
    result = await db.execute(select(VerificationCode).filter(VerificationCode.user_id == user.id))
    return result.scalars().first()


async def create_verification_code(db: AsyncSession, phone_number: str):
    """
    Create a verification code for a user
    """
    user = await get_user_by_phone(db, phone_number)
    if not user:
        return None

    # Delete any existing codes for this user
    while True:
        user_expired_codes = await get_verification_code(db, user)
        if not user_expired_codes:
            break
        await db.delete(user_expired_codes)
        await db.commit()

    # Create a new code and ensure it's an integer
    code = generate_code()

    db_code = VerificationCode(user_id=user.id, code=code)
    db.add(db_code)
    await db.commit()
    await db.refresh(db_code)
    return db_code


async def verify_sent_code(db: AsyncSession, user, code: int):
    """
    Verify a code sent to a user
    """
    db_code = await get_verification_code(db, user)
    if not db_code:
        raise HTTPException(status_code=404, detail="Code not found")

    if db_code.code != code:
        db_code.attempts += 1
        await db.commit()
        if db_code.attempts > 3:
            db.delete(db_code)
            await db.commit()
            raise HTTPException(status_code=400, detail="Too many attempts")
        raise HTTPException(status_code=400, detail="Invalid code")

    if db_code.expires_at < datetime.now():
        db.delete(db_code)
        await db.commit()
        raise HTTPException(status_code=400, detail="Code expired")

    db_code.is_used = True
    await db.commit()
    return {
        "status": "success",
        "message": "Code verified successfully",
        "code_id": db_code.id
    }


async def delete_verification_code(db: AsyncSession, code_id: int):
    """
    Delete a verification code
    """
    result = await db.execute(select(VerificationCode).filter(VerificationCode.id == code_id))
    db_code = result.scalars().first()

    if not db_code:
        raise HTTPException(status_code=404, detail="Code not found")

    db.delete(db_code)
    await db.commit()
    return {"status": "success", "message": "Code deleted successfully"}


async def change_password(db: AsyncSession, user, new_password: str):
    """
    Change a user's password
    """
    user.password_hash = hash_password(new_password)
    user.updated_at = datetime.now()
    await db.commit()
    await db.refresh(user)
    return {"status": "success", "message": "Password changed successfully"}


async def authenticate_user(username: str, password: str, db: AsyncSession):
    """
    Authenticate a user by phone number and password
    """
    user = await get_user_by_phone(db, username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user