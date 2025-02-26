from app.models import Cart, CartItem


def create_cart_on_db(db, user):
    cart = Cart(
        user_id=user.get('user_id')
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
    return db.query(Cart).filter(Cart.user_id == user_id).all()


def create_cart_item_on_db(db, cart_item, user_id):
    cart = get_cart_by_user_id(db, user_id)
    if not cart:
        return None
    cart_item_db = CartItem(
        cart_id=cart.id,
        product_link=cart_item.product_link,
        price=cart_item.price,
        weight=cart_item.weight,
        quantity=cart_item.quantity
    )
    db.add(cart_item_db)
    db.commit()
    db.refresh(cart_item_db)
    return cart_item_db

def get_cart_item_by_id(db, cart_item_id, user_id):
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item:
        return None
    if get_cart_by_id(db, cart_item.cart_id, user_id):
        return cart_item
    return None








