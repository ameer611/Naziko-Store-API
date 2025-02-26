from sqlalchemy import Column, Integer, String, Float

from app.db.base import Base


class ShipmentType(Base):
    __tablename__ = 'shipment_types'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), unique=True)
    description = Column(String(255))
    cost_per_kg = Column(Float)