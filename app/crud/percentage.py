from app.models.transaction import Percentage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def create_percentage_on_db(db: AsyncSession, percentage):
    """Create a new percentage on the database."""
    percentage = Percentage(**percentage.dict())
    db.add(percentage)
    await db.commit()
    await db.refresh(percentage)
    return percentage

async def get_percentages_from_db(db: AsyncSession):
    """Get all percentages from the database."""
    result = await db.execute(select(Percentage))
    percentages = result.scalars().all()
    for percentage in percentages:
        if percentage.description is None:
            percentage.description = "No description available"
        if percentage.percentage is None:
            percentage.percentage = 0.0
    return percentages

async def update_percentage_on_db(id: int, db: AsyncSession, percentage_update):
    """Update a percentage in the database, allowing updates to either field."""

    result = await db.execute(select(Percentage).filter(Percentage.id == id))
    percentage = result.scalars().first()
    if not percentage:
        return None  # Return None if no record is found

    update_data = percentage_update.dict(exclude_unset=True)  # Exclude fields that were not provided

    if not update_data:
        return {"message": "No changes provided."}  # Handle empty update requests

    for key, value in update_data.items():
        setattr(percentage, key, value)

    await db.commit()
    return {"message": "Percentage updated successfully."}

async def get_percentage(db: AsyncSession):
    """ Get the latest percentage """
    result = await db.execute(select(Percentage).order_by(Percentage.created_at.desc()).limit(1))
    return result.scalars().first()