import json
from contextlib import contextmanager
from unittest.mock import patch

import pytest
from pydantic import ValidationError
from starlette import status

from app.schema.external_git_repo_schema import GitHubCheckerSchema

from tests.factories.user_factory import UserFactory


@contextmanager
def mock_get_request_to_external_repo_api(mock_value, status: status):
    with patch("app.repository.external_git_repo_repository.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = status
        mock_response.json.return_value = mock_value
        try:
            yield mock_response
        finally:
            pass


def generate_auth_user(db):
    return UserFactory(logged_in=True, session=db)


def generate_header(access_token: str):
    return {
        "Authorization": f"Bearer {access_token}"
    }


@pytest.mark.parametrize("star_number, fork_number, expected_is_popular,owner,repo", [
    (500, 1000, True, "owner1", "repo1"),
    (0, 5, False, "owner2", "repo2"),
])
def test_repo_api_fetch_data_and_save_in_cache_correctly(star_number, fork_number, expected_is_popular, owner, repo,
                                                         client, db_session, redis,
                                                         container):
    redis_repository = container.redis_repository(
        redis_connection=redis,
    )
    cache_key = f"repo:{owner}:{repo}"

    auth_user = generate_auth_user(db_session)
    headers = generate_header(auth_user.access_token)
    mock_value = {
        "stargazers_count": star_number,
        "forks_count": fork_number
    }
    with mock_get_request_to_external_repo_api(mock_value=mock_value, status=status.HTTP_200_OK) as mock_get:
        response = client.get(f'/api/v1/repositories/popularity/github/{owner}/{repo}', headers=headers)
        json_response = response.json()
        try:
            user_data = GitHubCheckerSchema(**json_response)
        except ValidationError as e:
            assert False, f"Response validation error: {e}"

        assert response.status_code == status.HTTP_200_OK
        assert user_data.is_popular == expected_is_popular

        cache_data = redis_repository.get(cache_key)
        cache_data = json.loads(cache_data)

        assert cache_data['stargazers_count'] == star_number
        assert cache_data['forks_count'] == fork_number


@pytest.mark.parametrize("status_code, external_api_detail_error", [
    (status.HTTP_400_BAD_REQUEST, {"message": "Bad Request", "documentation_url": "https://docs.github.com"}),
    (status.HTTP_401_UNAUTHORIZED, {"message": "Bad Credentials", "documentation_url": "https://docs.github.com"}),
    (status.HTTP_404_NOT_FOUND, {"message": "Not Found", "documentation_url": "https://docs.github.com"})
])
def test_repo_api_raise_external_error_properly(client, db_session, redis, container,status_code,external_api_detail_error):
    redis_repository = container.redis_repository(
        redis_connection=redis,
    )
    owner = "someowner"
    repo = "somerepo"

    cache_key = f"repo:{owner}:{repo}"

    auth_user = generate_auth_user(db_session)
    headers = generate_header(auth_user.access_token)
    with mock_get_request_to_external_repo_api(mock_value=external_api_detail_error, status=status_code) as mock_get:
        res = client.get(f'/api/v1/repositories/popularity/github/{owner}/{repo}', headers=headers)
        res_body = res.json()

        assert res.status_code == status_code
        assert res_body['message'] == "Failed to fetch repository information"
        assert res_body['external_api_detail_error'] == external_api_detail_error

        cache_data = redis_repository.get(cache_key)

        assert not cache_data
