import math
from datetime import datetime
from unittest.mock import patch

from app.core.config import setting
from app.core.exceptions import AuthError
from app.core.security import decode_jwt
from app.entities.user import User
from app.schema.auth_schema import SignUpSchema, SignInSchema
from tests.factories.user_factory import UserEntityFactory

PASSWORD = "S0meR4ndOmP!asworD987234"


def test_auth_service_sign_up_user_called_correct_method_and_return_user_entity(container):
    with patch('app.repository.user_repository.UserRepository.create') as mock_create:
        mock_create.return_value = UserEntityFactory()

        auth_service_instance = container.auth_service()

        user_entity = UserEntityFactory(password=PASSWORD)

        user_schema = SignUpSchema(email=user_entity.email, password=user_entity.password)
        user = auth_service_instance.sign_up(user_schema)

        mock_create.assert_called_once()

        assert type(user) == User


def test_auth_service_sign_in_read_user_from_repository_and_validate_user_and_return_access_token(container):
    auth_service_instance = container.auth_service()
    user_entity = UserEntityFactory(password=PASSWORD)
    with patch('app.repository.user_repository.UserRepository.read_by_options') as mock_read_by_options:
        mock_read_by_options.return_value = {
            "founds": [user_entity],
            'search_options': {'page': 1, 'page_size': 20, 'ordering': '-id', 'total_count': 0},
        }

        user_schema = SignInSchema(email=user_entity.email, password=PASSWORD)
        sign_in_result = auth_service_instance.sign_in(user_schema)

        assert 'access_token' in sign_in_result
        assert 'expiration' in sign_in_result
        assert 'user_info' in sign_in_result

        assert sign_in_result['user_info']['email'] == user_entity.email

        user_from_token = decode_jwt(sign_in_result['access_token'])
        assert user_from_token['id'] == sign_in_result['user_info']['id']
        assert user_from_token['email'] == sign_in_result['user_info']['email']

        expiration_time = datetime.utcfromtimestamp(user_from_token['exp'])
        now = datetime.utcnow()

        total_diff_minutes = (expiration_time - now).total_seconds() / 60

        margin_of_error_minutes = 1

        assert math.isclose(total_diff_minutes, setting.ACCESS_TOKEN_EXPIRE_MINUTES,
                            abs_tol=margin_of_error_minutes), f"Expiration difference is outside the acceptable range: {total_diff_minutes} vs {setting.ACCESS_TOKEN_EXPIRE_MINUTES}"


def test_auth_service_sign_in_raise_exception_when_password_is_incorrect(container):
    auth_service_instance = container.auth_service()
    user_entity = UserEntityFactory(password=PASSWORD)
    with patch('app.repository.user_repository.UserRepository.read_by_options') as mock_read_by_options:
        mock_read_by_options.return_value = {
            "founds": [user_entity],
            'search_options': {'page': 1, 'page_size': 20, 'ordering': '-id', 'total_count': 1},
        }

        user_schema = SignInSchema(email=user_entity.email, password="somewrongpass")
        try:
            auth_service_instance.sign_in(user_schema)
        except AuthError as e:
            assert e.detail == "Incorrect email or password"


def test_auth_service_sign_in_raise_exception_when_email_is_not_found(container):
    auth_service_instance = container.auth_service()
    with patch('app.repository.user_repository.UserRepository.read_by_options') as mock_read_by_options:
        mock_read_by_options.return_value = {
            "founds": [],
            'search_options': {'page': 1, 'page_size': 20, 'ordering': '-id', 'total_count': 0},
        }

        user_schema = SignInSchema(email="somerandemail@gmail.com", password=PASSWORD)
        try:
            auth_service_instance.sign_in(user_schema)
        except AuthError as e:
            assert e.detail == "Incorrect email or password"
