from unittest.mock import patch

from tests.factories.user_factory import UserEntityFactory

PASSWORD = "S0meR4ndOmP!asworD987234"


def test_user_service_get_by_id(container):
    user_service_instance = container.user_service()
    user_entity = UserEntityFactory(password=PASSWORD)
    with patch('app.repository.user_repository.UserRepository.read_by_id') as mock_read_by_id:
        mock_read_by_id.return_value = user_entity
        user = user_service_instance.get_by_id(id=user_entity.id)

        assert user.email == user_entity.email
        assert user.id == user_entity.id
        assert user.password == user_entity.password
        assert not user.password == PASSWORD


def test_user_service_get_list(container):
    user_service_instance = container.user_service()
    user_entity = UserEntityFactory(password=PASSWORD)
    with patch('app.repository.user_repository.UserRepository.read_by_options') as mock_read_by_options:
        mock_read_by_options.return_value = {
            "founds": [user_entity],
            'search_options': {'page': 1, 'page_size': 20, 'ordering': '-id', 'total_count': 1},
        }

        user = user_service_instance.get_list({"id": user_entity.id})
        user = user['founds'][0]

        assert user.email == user_entity.email
        assert user.id == user_entity.id
        assert user.password == user_entity.password
        assert not user.password == PASSWORD


def test_user_service_patch(container):
    user_service_instance = container.user_service()
    user_entity = UserEntityFactory(password=PASSWORD)
    with patch('app.repository.user_repository.UserRepository.read_by_options') as mock_read_by_options:
        mock_read_by_options.return_value = {
            "founds": [user_entity],
            'search_options': {'page': 1, 'page_size': 20, 'ordering': '-id', 'total_count': 1},
        }

        user = user_service_instance.get_list({"id": user_entity.id})
        user = user['founds'][0]

        assert user.email == user_entity.email
        assert user.id == user_entity.id
        assert user.password == user_entity.password
        assert not user.password == PASSWORD


def test_user_service_add(container):
    user_service_instance = container.user_service()
    user_entity = UserEntityFactory(password=PASSWORD)
    with patch('app.repository.user_repository.UserRepository.create') as mock_read_by_options:
        mock_read_by_options.return_value = user_entity

        user = user_service_instance.add(user_entity)

        assert user.email == user_entity.email
        assert user.id == user_entity.id
        assert user.password == user_entity.password
        assert not user.password == PASSWORD
