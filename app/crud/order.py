from app.crud.product import get_product_from_db_if_exists
from app.models import Order, OrderItem


def create_order_on_db(db, order, user_id):
    order_db = Order(**order.dict(), user_id=user_id)
    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db

def get_orders_from_db(db, user_id):
    if not user_id:
        return None
    orders = db.query(Order).filter(Order.user_id==user_id).order_by(Order.created_at.desc()).all()
    if not orders:
        return None
    return orders

def get_order_by_id(db, user_id, order_id):
    if not user_id:
        return None
    order = db.query(Order).filter(Order.user_id==user_id, Order.id==order_id).first()
    if not order:
        return None
    return order

def delete_order_from_db(db, order_id):
    order = db.query(Order).filter(Order.id==order_id).first()
    if not order:
        return None
    db.delete(order)
    db.commit()
    return "Order deleted"

def create_order_item_on_db(db, order_item):
    product = get_product_from_db_if_exists(db, order_item.product_link)
    if not product:
        return None
    order_item_db = OrderItem(**order_item.dict(), price=getattr(product, "price", 0), weight=getattr(product, "weight", 0))
    db.add(order_item_db)
    db.commit()
    db.refresh(order_item_db)
    return order_item_db