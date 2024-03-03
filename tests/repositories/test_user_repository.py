from app.core.exceptions import DuplicatedError
from tests.factories.user_factory import UserFactory, UserEntityFactory

EMAIL = "mohi@gmail.com"
PASSWORD = "123456789"


def test_user_repo_can_read_user_information_from_db_successfully(db_session, container):
    user = UserFactory(session=db_session)

    user_repo = container.user_repository()
    user_from_db = user_repo.read_by_id(user.id)

    assert user.id == user_from_db.id
    assert user.email == user_from_db.email


def test_user_repo_can_store_user_information_into_db_successfully(db_session, container):
    user_entity = UserEntityFactory(email=EMAIL)

    user_repo = container.user_repository()
    user_from_db = user_repo.create(user_entity)

    assert user_from_db.email == EMAIL


def test_user_repo_raise_exception_with_repetitive_email_address(client, db_session, container):
    email = "mohi@gmail.com"

    user_entity = UserEntityFactory(email=email)
    UserFactory(email=email, session=db_session)

    user_repo = container.user_repository()
    try:
        user_repo.create(user_entity)
    except DuplicatedError as e:
        assert "duplicate key value violates unique constraint" in e.detail


def test_user_repo_can_update_user_information_in_db_successfully(client, db_session, container):
    email = "mohi@gmail.com"
    password = "123456789"

    email_for_update = "mohi2@gmial.com"

    user = UserFactory(email=email, password=password, session=db_session)
    user_repo = container.user_repository()

    user_from_db = user_repo.read_by_id(user.id)
    assert user_from_db.email == user.email

    user_repo.update_attr(user.id, "email", email_for_update)

    user_from_db = user_repo.read_by_id(user.id)
    assert user_from_db.email == email_for_update
