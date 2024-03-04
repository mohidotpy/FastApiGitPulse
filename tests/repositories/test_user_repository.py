import random

from app.core.exceptions import DuplicatedError
from app.schema.user_schema import FindUserSchema, UpsertUserSchema
from tests.factories.user_factory import UserFactory, UserEntityFactory

EMAIL = "mohi@gmail.com"
PASSWORD = "123456789"
PAGE_SIZE = 20


def generate_bunch_of_user(user_number: int, db_session):
    user_list = []
    for i in range(user_number):
        user_list.append(UserFactory(session=db_session))

    return user_list


def test_user_repo_can_read_user_information_from_db_successfully(db_session, container):
    user = UserFactory(session=db_session)

    user_repo = container.user_repository()
    user_from_db = user_repo.read_by_id(user.id)

    assert user.id == user_from_db.id
    assert user.email == user_from_db.email


def test_user_repo_can_get_list_of_user_from_db_successfully(db_session, container):
    user_list = []
    random_number_of_users = random.randint(0, 30)
    for i in range(random_number_of_users):
        user_list.append(UserFactory(session=db_session))

    user_repo = container.user_repository()
    user_list_info_from_db = user_repo.read_by_options(schema=FindUserSchema())
    user_list_from_db = user_list_info_from_db['founds']

    assert len(user_list_from_db) == min(user_list_info_from_db['search_options']['total_count'], PAGE_SIZE)
    assert len(user_list) == user_list_info_from_db['search_options']['total_count']

    random_index = random.randint(0, random_number_of_users)

    random_user_from_db = user_repo.read_by_options(schema=FindUserSchema(email=user_list[random_index].email))
    assert random_user_from_db['founds'][0].email == user_list[random_index].email


def test_user_repo_can_store_user_information_into_db_successfully(db_session, container):
    user_entity = UserEntityFactory(email=EMAIL)

    user_repo = container.user_repository()
    user_from_db = user_repo.create(user_entity)

    assert user_from_db.email == EMAIL


def test_user_repo_raise_exception_with_repetitive_email_address(db_session, container):
    email = "mohi@gmail.com"

    user_entity = UserEntityFactory(email=email)
    UserFactory(email=email, session=db_session)

    user_repo = container.user_repository()
    try:
        user_repo.create(user_entity)
    except DuplicatedError as e:
        assert "duplicate key value violates unique constraint" in e.detail


def test_user_repo_can_update_user_in_db(db_session, container):
    email = "mohi@gmail.com"
    password = "123456789"

    user = UserFactory(email=email, password=password, session=db_session)
    user_repo = container.user_repository()

    user_from_db = user_repo.read_by_id(user.id)
    assert user_from_db.email == user.email

    new_user_entity = UserEntityFactory()
    updated_info = UpsertUserSchema(email=new_user_entity.email, user_token=new_user_entity.user_token)

    user_repo.update(id=user.id, schema=updated_info)

    user_from_db = user_repo.read_by_id(user.id)
    assert user_from_db.email == new_user_entity.email
    assert user_from_db.user_token == new_user_entity.user_token


def test_user_repo_can_update_user_attr_in_db(client, db_session, container):
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


def test_user_repo_can_remove_user_in_db(client, db_session, container):
    users_number = 5
    user_repo = container.user_repository()

    user_list = generate_bunch_of_user(users_number, db_session)

    user_to_remove = user_list[random.randint(0, users_number)]

    user_repo.delete_by_id(user_to_remove.id)

    assert not user_repo.read_by_id(user_to_remove.id)

    user_list = user_repo.read_by_options(FindUserSchema())['founds']
    assert len(user_list) == users_number - 1
