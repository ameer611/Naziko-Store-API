from sqlalchemy.orm import Session

from app.models import OnlineProduct
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


def get_product_from_db_if_exists(db: Session, product_link: str):
    """Get the product from the database if it exists."""
    online_product_db =  db.query(OnlineProduct).filter(OnlineProduct.product_link == product_link).first()
    if not online_product_db:
        return None
    return online_product_db

def update_product_add_variants_to_db_product(db: Session, variants: list, product_link: str):
    """Update the product on the database by adding variants."""
    db_product = get_product_from_db_if_exists(db, product_link)
    if not db_product:
        return None
    db_product.variants = variants
    db.commit()
    return db_product.variants

def save_product_on_db(db, product_details:dict, product_link:str):
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
    db.commit()
    return db_product



def get_products_from_db(db: Session):
    """Get the list of products from the database."""
    return db.query(DatabaseProduct).all()

