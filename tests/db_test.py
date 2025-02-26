from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.core.security import get_current_user
from app.db.base import Base, get_db
from app.main import main_app

FAKE_DATABASE_URL = 'sqlite:///fake.db'

engine = create_engine(
    FAKE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    # Poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"sub": "1", "fullname": "Ameer", "is_admin": False, "is_superuser": False}

main_app.dependency_overrides[get_db] = override_get_db
main_app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(main_app)
