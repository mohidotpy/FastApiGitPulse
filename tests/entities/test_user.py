import pytest

from app.entities.exceptions import InvalidDataException
from app.entities.user import User


def test_create_user_entity_with_valid_data():
    user_email = "mohidotpy@gmail.com"
    user = User(email=user_email)
    assert user.email == user_email


def test_create_user_entity_with_invalid_email():
    with pytest.raises(InvalidDataException) as e:
        User(
            email="mohidotpy_gmail.com"
        )
    assert e.value.message == 'Invalid email address'

    with pytest.raises(InvalidDataException) as e:
        User(
            email="@.com"
        )
    assert e.value.message == 'Invalid email address'

    with pytest.raises(InvalidDataException) as e:
        User(
            email="@gmail.com"
        )
    assert e.value.message == 'Invalid email address'

    with pytest.raises(InvalidDataException) as e:
        User(
            email="mohidotpy@gmail."
        )
    assert e.value.message == 'Invalid email address'
