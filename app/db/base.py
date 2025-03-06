from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from dotenv import load_dotenv
import os

from sqlalchemy.orm import DeclarativeBase

load_dotenv()

# Ensure the DATABASE_URL uses the async driver (e.g., 'postgresql+asyncpg://')
engine = create_async_engine(os.getenv("DATABASE_URL"), echo=True)

# Async Session Factory
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base class for models
class Base(AsyncAttrs, DeclarativeBase):
    pass

# Dependency for FastAPI
async def get_db():
    async with SessionLocal() as db:
        yield db


# from dotenv import load_dotenv
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os
# import app.models
#
# load_dotenv()
#
# DATABASE_URL = os.getenv("DATABASE_URL")
#
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()
#
# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
