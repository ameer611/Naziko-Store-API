from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update

from app.core.security import verify_password, hash_password
from app.models import User


async def change_user_info_on_db(db: AsyncSession, user_id: int, changed_info):
    """Changes user info in the database."""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        return None
    update_data = changed_info.dict(exclude_unset=True)
    if not update_data:
        return {"message": "No changes provided."}
    await db.execute(update(User).where(User.id == user_id).values(**update_data))
    await db.commit()
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def change_user_password_on_db(db: AsyncSession, user_id: int, changed_info):
    """Changes user password in the database."""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        return None
    user.password_hash = hash_password(changed_info.new_password)
    await db.commit()
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def check_passwords(old_password: str, user_id: int, db: AsyncSession):
    """Check if the old password is correct."""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(old_password, user.password_hash):
        return False
    return True


async def change_phone_number_on_db(db: AsyncSession, user_id: int, phone_number: str):
    """Change phone number in the database."""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        return None
    user.phone_number = phone_number
    await db.commit()
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


########################################
# Admin functions
########################################
async def get_customers_from_db(db: AsyncSession):
    """Get all customers from the database."""
    result = await db.execute(select(User).filter(User.is_superuser == False))
    return result.scalars().all()


async def get_customer_by_id_from_db(db: AsyncSession, customer_id: int):
    """Get a customer by ID from the database."""
    result = await db.execute(select(User).filter(User.id == customer_id))
    return result.scalars().first()


async def change_customer_password_on_db(db: AsyncSession, customer, new_password: str):
    """Change customer password in the database."""
    customer.password_hash = hash_password(new_password)
    await db.commit()
    result = await db.execute(select(User).filter(User.id == customer.id))
    return result.scalars().first()


async def delete_customer_from_db(db: AsyncSession, customer):
    """Delete a customer from the database."""
    await db.delete(customer)
    await db.commit()
    return {"message": "Customer deleted successfully"}


async def get_user_by_id(db: AsyncSession, user_id: int):
    """Get a user by ID from the database."""
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()