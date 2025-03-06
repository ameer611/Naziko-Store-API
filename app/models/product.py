from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.base import Base


class DatabaseProduct(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    product_link = Column(String)
    image_link = Column(String)


class OnlineProduct(Base):
    __tablename__ = 'online_products'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    product_link = Column(String, unique=True, index=True, nullable=False)
    images_links = Column(JSON, nullable=True)
    weight = Column(Float, nullable=True)
    description = Column(JSON, nullable=True)
    variants = Column(JSON, nullable=True)


