from app.crud.product import get_product_from_db_if_exists
from app.models import Cart, CartItem
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


async def create_cart_on_db(db: AsyncSession, user):
    cart = Cart(
        user_id=user.id,
    )
    db.add(cart)
    await db.commit()
    await db.refresh(cart)
    return cart

async def get_cart_by_id(db: AsyncSession, cart_id: int, user_id: int):
    result = await db.execute(select(Cart).options(selectinload(Cart.cart_items)).filter(Cart.id == cart_id, Cart.user_id == user_id))
    return result.scalars().first()


async def get_cart_by_user_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(Cart).options(selectinload(Cart.cart_items)).filter(Cart.user_id == user_id))
    return result.scalars().first()

async def get_carts_by_user_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(Cart).options(selectinload(Cart.cart_items)).filter(Cart.user_id == user_id).order_by(Cart.created_at.desc()))
    return result.scalars().all()


async def create_cart_item_on_db(db: AsyncSession, cart_item, user_id: int):
    cart = await get_cart_by_id(db, cart_item.cart_id, user_id)
    if not cart:
        return None

    product_db = await get_product_from_db_if_exists(db, cart_item.product_link)

    cart_item_db = CartItem(
        cart_id=cart.id,
        product_link=cart_item.product_link,
        price=getattr(product_db, "price", 0),
        weight=getattr(product_db, "weight", 0),
        quantity=cart_item.quantity,
        variant=cart_item.variant
    )
    db.add(cart_item_db)
    await db.commit()
    await db.refresh(cart_item_db)
    return cart_item_db

async def get_cart_item_by_id(db: AsyncSession, cart_item_id: int, user_id: int):
    result = await db.execute(select(CartItem).options(selectinload(CartItem.cart)).filter(CartItem.id == cart_item_id))
    cart_item = result.scalars().first()
    if not cart_item:
        return None
    if cart_item.cart.user_id != user_id:
        return None
    return cart_item