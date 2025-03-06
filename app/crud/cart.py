from app.crud.product import get_product_from_db_if_exists
from app.models import Cart, CartItem


def create_cart_on_db(db, user):
    cart = Cart(
        user_id=user.id,
    )
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart

def get_cart_by_id(db, cart_id, user_id):
    return db.query(Cart).filter(Cart.id == cart_id, Cart.user_id == user_id).first()


def get_cart_by_user_id(db, user_id):
    return db.query(Cart).filter(Cart.user_id == user_id).first()

def get_carts_by_user_id(db, user_id):
    return db.query(Cart).filter(Cart.user_id == user_id).order_by(Cart.created_at.desc()).all()


def create_cart_item_on_db(db, cart_item, user_id):
    cart = get_cart_by_id(db, cart_item.cart_id, user_id)
    if not cart:
        return None

    product_db = get_product_from_db_if_exists(db, cart_item.product_link)

    cart_item_db = CartItem(
        cart_id=cart.id,
        product_link=cart_item.product_link,
        price=getattr(product_db, "price", 0),
        weight=getattr(product_db, "weight", 0),
        quantity=cart_item.quantity,
        variant=cart_item.variant
    )
    db.add(cart_item_db)
    db.commit()
    db.refresh(cart_item_db)
    return cart_item_db

def get_cart_item_by_id(db, cart_item_id, user_id):
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item:
        return None
    checking_cart_item_belong_the_user = get_cart_by_id(db, cart_item.cart_id, user_id)
    if not checking_cart_item_belong_the_user:
        return None
    return cart_item








