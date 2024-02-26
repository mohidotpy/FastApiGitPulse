from pydantic import ValidationError
from starlette import status

from tests.conftest import db, client

from app.schema.user_schema import CurrentUserSchema
from tests.factories.user_factory import UserFactory


def test_get_current_authenticated_user(client, db):
    email = "mohi@gmail.com"
    password = "123456789"

    UserFactory._meta.sqlalchemy_session = db

    user = UserFactory(email=email, password=password, logged_in=True)
    headers = {
        "Authorization": f"Bearer {user.access_token}"
    }
    res = client.get('/api/v1/users/me', headers=headers)
    res_body = res.json()

    try:
        user_data = CurrentUserSchema(**res_body)
    except ValidationError as e:
        assert False, f"Response validation error: {e}"

    assert res.status_code == status.HTTP_200_OK
    assert user_data.email == user.email
    assert user_data.id == user.id
