import json
from unittest.mock import patch

import pytest
from pydantic import ValidationError
from starlette import status

from app.schema.external_git_repo_schema import GitHubCheckerSchema

from tests.conftest import db, client, redis, container

from tests.factories.user_factory import UserFactory


@pytest.mark.parametrize("star_number, fork_number, expected_is_popular,owner,repo", [
    (500, 1000, True, "owner1", "repo1"),
    (0, 5, False, "owner2", "repo2"),
])
def test_repo_api_fetch_data_and_save_in_cache_correctly(star_number, fork_number, expected_is_popular, owner, repo,
                                                         client, db, redis,
                                                         container):
    redis_repository = container.redis_repository(
        redis_connection=redis,
    )
    cache_key = f"repo:{owner}:{repo}"

    UserFactory._meta.sqlalchemy_session = db

    user = UserFactory(logged_in=True)
    headers = {
        "Authorization": f"Bearer {user.access_token}"
    }
    with patch("app.repository.external_git_repo_repository.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = status.HTTP_200_OK
        mock_response.json.return_value = {
            "stargazers_count": star_number,
            "forks_count": fork_number
        }

        res = client.get(f'/api/v1/repositories/popularity/github/{owner}/{repo}', headers=headers)
        res_body = res.json()

        try:
            user_data = GitHubCheckerSchema(**res_body)
        except ValidationError as e:
            assert False, f"Response validation error: {e}"

        assert res.status_code == status.HTTP_200_OK
        assert user_data.is_popular == expected_is_popular

        cache_data = redis_repository.get(cache_key)
        cache_data = json.loads(cache_data)

        assert cache_data['stargazers_count'] == star_number
        assert cache_data['forks_count'] == fork_number


def test_repo_api_through_external_error_porperly(client, db, redis, container):
    redis_repository = container.redis_repository(
        redis_connection=redis,
    )
    owner = "someowner"
    repo = "somerepo"

    mock_value = {
            "message": "Not Found",
            "documentation_url": "https://docs.github.com/rest/repos/repos#get-a-repository"
        }

    cache_key = f"repo:{owner}:{repo}"

    UserFactory._meta.sqlalchemy_session = db

    user = UserFactory(logged_in=True)
    headers = {
        "Authorization": f"Bearer {user.access_token}"
    }
    with patch("app.repository.external_git_repo_repository.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = status.HTTP_404_NOT_FOUND
        mock_response.json.return_value = mock_value

        res = client.get(f'/api/v1/repositories/popularity/github/{owner}/{repo}', headers=headers)
        res_body = res.json()

        assert res.status_code == status.HTTP_404_NOT_FOUND
        assert res_body['message'] == "Failed to fetch repository information"
        assert res_body['external_api_detail_error'] == mock_value

        cache_data = redis_repository.get(cache_key)

        assert not cache_data

