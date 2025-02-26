from sqlalchemy import Column, Integer, String, Float

from app.db.base import Base


class DatabaseProduct(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    product_link = Column(String)
    image_link = Column(String)