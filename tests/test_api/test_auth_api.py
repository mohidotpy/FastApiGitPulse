import math
from datetime import datetime

from app.core.config import setting
from app.entities.constants import INVALID_EMAIL_EXCEPTION_MESSAGE, INVALID_LOGIN_DATA_EXCEPTION_MESSAGE

from starlette import status

from app.schema.user_schema import FindUserSchema
from tests.factories.user_factory import UserFactory


def test_register_user_api_with_correct_data(client, db_session, container):
    data = {"email": "mohidotpy@gmail.com", "password": "123456789"}
    res = client.post('/api/v1/auth/sign-up', json=data)

    assert res.status_code == status.HTTP_200_OK
    find_query = FindUserSchema()

    user_service = container.user_service()
    users = user_service.get_list(find_query)
    assert users['search_options']['total_count'] == 1
    assert users['founds'][0].email == data['email']


def test_register_user_api_with_bad_email_address(client, db_session, container):
    data = {"email": "mohidotpy@gmail", "password": "123456789"}
    res = client.post('/api/v1/auth/sign-up', json=data)
    res_body = res.json()
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res_body['message'] == INVALID_EMAIL_EXCEPTION_MESSAGE


def test_login_user_api_with_correct_data(client, db_session, container):
    email = "mohi@gmail.com"
    password = "123456789"

    UserFactory(email=email, password=password, session=db_session)
    data = {"email": email, "password": password}

    res = client.post('/api/v1/auth/sign-in', json=data)
    res_body = res.json()
    expiration_date = datetime.strptime(res_body['expiration'], "%Y-%m-%dT%H:%M:%S")
    now = datetime.utcnow()

    total_diff_minutes = (expiration_date - now).total_seconds() / 60

    margin_of_error_minutes = 1

    assert res.status_code == status.HTTP_200_OK
    assert math.isclose(total_diff_minutes, setting.ACCESS_TOKEN_EXPIRE_MINUTES,
                        abs_tol=margin_of_error_minutes), f"Expiration difference is outside the acceptable range: {total_diff_minutes} vs {setting.ACCESS_TOKEN_EXPIRE_MINUTES}"


def test_login_user_api_with_incorrect_data(client, db_session, container):
    email = "mohi@gmail.com"
    password = "123456789"

    UserFactory._meta.sqlalchemy_session = db_session

    UserFactory(email=email, password=password)
    data = {"email": email, "password": "12345"}

    res = client.post('/api/v1/auth/sign-in', json=data)
    res_body = res.json()

    assert res.status_code == status.HTTP_403_FORBIDDEN
    assert res_body['detail'] == INVALID_LOGIN_DATA_EXCEPTION_MESSAGE
