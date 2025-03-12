from app.crud.product import get_product_from_db_if_exists
from app.models import Order, OrderItem
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


async def create_order_on_db(db: AsyncSession, order, user_id: int):
    order_db = Order(**order.dict(), user_id=user_id)
    db.add(order_db)
    await db.commit()
    await db.refresh(order_db)
    return order_db

async def get_orders_from_db(db: AsyncSession, user_id: int):
    result = await db.execute(select(Order).options(selectinload(Order.order_items)).filter(Order.user_id == user_id).order_by(Order.created_at.desc()))
    return result.scalars().all()

async def get_order_by_id(db: AsyncSession, user_id: int, order_id: int):
    result = await db.execute(select(Order).options(selectinload(Order.order_items)).filter(Order.user_id == user_id, Order.id == order_id))
    return result.scalars().first()

async def delete_order_from_db(db: AsyncSession, order_id: int):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    order = result.scalars().first()
    if not order:
        return None
    await db.delete(order)
    await db.commit()
    return "Order deleted"

async def create_order_item_on_db(db: AsyncSession, order_item):
    product = await get_product_from_db_if_exists(db, order_item.product_link)
    if not product:
        return None
    order_item_db = OrderItem(**order_item.dict(), price=getattr(product, "price", 0), weight=getattr(product, "weight", 0))
    db.add(order_item_db)
    await db.commit()
    await db.refresh(order_item_db)
    return order_item_db