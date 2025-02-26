from tests.db_test import client
from tests.utils import test_user


def test_register(test_user):
    response = client.post("/v1/auth/register",
                           json={"phone_number": test_user.phone_number,
                                 "password": test_user.phone_number,
                                 "fullname": test_user.fullname})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "phone_number": "+998951234567",
        "fullname": "John Doe",
        "tg_id": None,
        "is_admin": False,
        "is_superuser": False,
        "is_active": True,
        "language_code": "uz",
        "created_at": response.json()["created_at"],
        "updated_at": response.json()["updated_at"]
    }
