from datetime import datetime

from sqlalchemy import Column, Float, DateTime, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    description = Column(String(255))
    date = Column(DateTime)
    order_id = Column(Integer, ForeignKey('orders.id'))
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    is_approved = Column(Boolean, default=False)

    order = relationship('Order', backref='transactions')

class Percentage(Base):
    __tablename__ = 'percentages'

    id = Column(Integer, primary_key=True)
    percentage = Column(Float)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

