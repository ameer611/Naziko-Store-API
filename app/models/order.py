from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime, Float
from sqlalchemy.orm import relationship

from app.db.base import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_paid = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    shipment_id = Column(Integer, ForeignKey('shipment_types.id'), nullable=False)

    # Relationships
    shipment = relationship('ShipmentType',lazy="joined")
    order_items = relationship('OrderItem',cascade='all, delete', lazy="joined")



class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete="CASCADE"), nullable=False)
    product_link = Column(String, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    price = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)

    # Relationship
    order = relationship('Order', back_populates='order_items')
