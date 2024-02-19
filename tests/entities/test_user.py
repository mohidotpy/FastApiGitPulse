from app.entities.user import User


def test_create_user_entity_with_valid_data():
    user_email = "mohidotpy@gmail.com"
    user = User(email=user_email)
    assert user.email == user_email