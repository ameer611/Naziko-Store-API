from sqlalchemy.ext.asyncio import AsyncEngine
from app.db.base import engine  # Ensure you import the correct engine
from app.db.base import Base  # Import Base where all models inherit from

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# from app.db.base import Base, engine
#
#
# def init_db():
#     Base.metadata.create_all(bind=engine)