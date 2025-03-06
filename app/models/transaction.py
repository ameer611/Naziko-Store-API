from datetime import datetime

from sqlalchemy import Column, Float, DateTime, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float)
    description = Column(String(255), nullable=True)
    date = Column(DateTime)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    is_approved = Column(Boolean, default=False)

    order = relationship('Order', backref='transactions')
    user = relationship('User', backref='transactions')

class Percentage(Base):
    __tablename__ = 'percentages'

    id = Column(Integer, primary_key=True)
    percentage = Column(Float)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

