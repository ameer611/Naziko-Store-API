from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Float, Enum, JSON
from sqlalchemy.orm import relationship

from app.common.enums import OrderStatus
from app.db.base import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    shipment_id = Column(Integer, ForeignKey('shipment_types.id'), nullable=True)
    total_paid = Column(Float, default=0.0, nullable=False)

    # Relationships
    shipment = relationship('ShipmentType', lazy="joined")
    order_items = relationship('OrderItem', cascade='all, delete', lazy="joined")

    @property
    def total_price(self):
        return round(sum(item.price * item.quantity for item in self.order_items), 2)

    @property
    def total_weight(self):
        return round(sum(item.weight * item.quantity for item in self.order_items), 3)




class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete="CASCADE"), nullable=False)
    product_link = Column(String, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    price = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    variant = Column(JSON, nullable=True)


    # Relationship
    order = relationship('Order', back_populates='order_items')
