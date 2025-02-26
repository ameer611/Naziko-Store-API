from sqlalchemy.orm import Session

from app.models.product import DatabaseProduct


async def refresh_products_on_db(db: Session, products: list):
    """Refresh the product list on the database."""
    db.query(DatabaseProduct).delete()
    for product in products:
        db_product = DatabaseProduct(
            title=product["title"],
            price=product["price"],
            product_link=product["product_link"],
            image_link=product["image_link"]
        )
        db.add(db_product)
    db.commit()
    return {"message": "Products list refreshed successfully."}


def get_products_from_db(db: Session):
    """Get the list of products from the database."""
    return db.query(DatabaseProduct).all()