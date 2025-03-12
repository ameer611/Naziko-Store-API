from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text

from app.models import OnlineProduct
from app.models.product import DatabaseProduct


async def refresh_products_on_db(db: AsyncSession, products: list):
    await db.execute(text("DELETE FROM products"))
    for product in products:
        await db.execute(
            text("INSERT INTO products (title, price, image_link, product_link) VALUES (:title, :price, :image_link, :product_link)"),
            {
                "title": product["title"],
                "price": product["price"],
                "image_link": product["image_link"],
                "product_link": product["product_link"],
            },
        )
    await db.commit()
    return {"message": "Products refreshed successfully."}


async def get_product_from_db_if_exists(db: AsyncSession, product_link: str):
    """Get the product from the database if it exists."""
    result = await db.execute(select(OnlineProduct).filter(OnlineProduct.product_link == product_link))
    return result.scalars().first()


async def update_product_add_variants_to_db_product(db: AsyncSession, variants: list, product_link: str):
    """Update the product on the database by adding variants."""
    db_product = await get_product_from_db_if_exists(db, product_link)
    if not db_product:
        return None
    db_product.variants = variants
    await db.commit()
    return db_product.variants


async def save_product_on_db(db: AsyncSession, product_details: dict, product_link: str):
    """Save the product details on the database."""
    db_product = OnlineProduct(
        title=product_details.get("title", ""),
        price=product_details.get("price", 0.0),
        product_link=product_link,
        images_links=product_details.get("images_links", []),
        weight=product_details.get("descriptions", {}).get("weight", 0.0),
        description=product_details.get("descriptions", {})
    )
    db.add(db_product)
    await db.commit()
    return db_product


async def get_products_from_db(db: AsyncSession):
    """Get the list of products from the database."""
    result = await db.execute(select(DatabaseProduct))
    return result.scalars().all()