from sqlalchemy import Column, Integer, String, Float

from app.db.base import Base


class ShipmentType(Base):
    __tablename__ = 'shipment_types'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), unique=True)
    description = Column(String)
    days = Column(Integer, nullable=False)
    cost_per_kg = Column(Float, nullable=False)