from app.models import Transaction
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

async def create_transaction_on_db(db: AsyncSession, user_id, transaction):
    transaction_db = Transaction(
        user_id=user_id,
        amount=transaction.get("amount"),
        description=transaction.get("description"),
        date=transaction.get("date").replace(tzinfo=None),  # Ensure datetime is timezone-naive
        order_id=transaction.get("order_id"),
        image_url=transaction.get("image_url")
    )
    db.add(transaction_db)
    await db.commit()
    await db.refresh(transaction_db)
    return transaction_db

async def get_transactions_from_db(db: AsyncSession, user_id):
    if not user_id:
        return None
    result = await db.execute(
        select(Transaction)
        .options(joinedload(Transaction.user), joinedload(Transaction.order))
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.date.desc())
    )
    transactions = result.unique().scalars().all()
    if not transactions:
        return None
    return transactions

###########################################
# Admin CRUD Operations
###########################################
async def get_transactions_from_db_for_admin(db: AsyncSession):
    result = await db.execute(
        select(Transaction)
        .options(joinedload(Transaction.user), joinedload(Transaction.order))
        .order_by(Transaction.created_at.desc())
    )
    transactions = result.unique().scalars().all()
    if not transactions:
        return None
    return transactions

async def get_transaction_by_id(db: AsyncSession, transaction_id):
    result = await db.execute(
        select(Transaction)
        .options(joinedload(Transaction.user), joinedload(Transaction.order))
        .filter(Transaction.id == transaction_id)
    )
    transaction = result.scalars().first()
    if not transaction:
        return None
    return transaction

async def update_transaction_to_valid(db: AsyncSession, transaction_id):
    transaction = await get_transaction_by_id(db, transaction_id)
    if not transaction:
        return None
    transaction.is_approved = True
    await db.commit()
    return transaction