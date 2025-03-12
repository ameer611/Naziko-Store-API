from app.models import ShipmentType
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def create_shipment_type_on_db(db: AsyncSession, shipment):
    existing_shipment = await db.execute(select(ShipmentType).filter(ShipmentType.title == shipment.title))
    existing_shipment = existing_shipment.scalars().first()
    if existing_shipment:
        return None
    shipment_db = ShipmentType(**shipment.dict())
    db.add(shipment_db)
    await db.commit()
    await db.refresh(shipment_db)
    return shipment_db

async def get_shipments_from_db(db: AsyncSession):
    result = await db.execute(select(ShipmentType))
    return result.scalars().all()

async def get_shipment_by_id(db: AsyncSession, shipment_id: int):
    result = await db.execute(select(ShipmentType).filter(ShipmentType.id == shipment_id))
    shipment_db = result.scalars().first()
    if not shipment_db:
        return None
    return shipment_db

async def update_shipment_on_db(db: AsyncSession, shipment_db, shipment):
    updated_shipment = shipment.dict(exclude_unset=True)

    # Retrieve the existing shipment
    existing_shipment = await db.execute(select(ShipmentType).filter(ShipmentType.id == shipment_db.id))
    existing_shipment = existing_shipment.scalars().first()

    if not existing_shipment:
        return None  # Or raise an exception

    # Apply the updates manually
    for key, value in updated_shipment.items():
        setattr(existing_shipment, key, value)

    await db.commit()
    await db.refresh(existing_shipment)
    return existing_shipment