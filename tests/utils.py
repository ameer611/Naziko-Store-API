import pytest
from sqlalchemy import text

from app.core.security import hash_password
from app.models.user import User
from tests.db_test import TestingSessionLocal


@pytest.fixture
def test_user():
    user = User(
        phone_number="+998951234567",
        password_hash=hash_password("password"),
        fullname="John Doe",
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with TestingSessionLocal() as db:
        db.execute(text("DELETE FROM users;"))
        db.commit()

