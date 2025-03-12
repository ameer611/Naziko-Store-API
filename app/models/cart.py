from datetime import datetime

from sqlalchemy import Float, Integer, Column, ForeignKey, String, DateTime, JSON
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.db.base import Base


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    cart_items = relationship('CartItem', backref='cart', cascade='all, delete')

    @hybrid_property
    def total_price(self):
        return round(sum(item.price * item.quantity for item in self.cart_items), 3)

    @hybrid_property
    def total_weight(self):
        return round(sum(item.weight * item.quantity for item in self.cart_items), 0)


class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.id'))
    product_link = Column(String)
    quantity = Column(Integer, default=1)
    price = Column(Float)
    weight = Column(Float)
    variant = Column(JSON, nullable=True)