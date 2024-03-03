import json
from unittest.mock import patch

from app.core.container import Container
from app.repository.exceptions import ExternalAPIError
from tests.repositories.utils import generate_random_star_count_and_forks_count


def test_external_repo_information_store_successfully_in_cache(redis):
    redis_repository = Container.redis_repository(
        redis_connection=redis,
    )
    owner = "someone"
    repo = "somerepo"
    stargazers_count, forks_count = generate_random_star_count_and_forks_count()

    external_git_repository = Container.external_git_repo_repository(access_token="fake_access_token",
                                                                     cache_repo=redis_repository)

    with patch("app.repository.external_git_repo_repository.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "stargazers_count": stargazers_count,
            "forks_count": forks_count
        }

        repo_info = external_git_repository.get_cached_or_retrieve_external_repo_info(owner, repo)
        assert repo_info['stargazers_count'] == stargazers_count
        assert repo_info['forks_count'] == forks_count

        cache_data = external_git_repository.cache_repo.get("repo:someone:somerepo")
        assert cache_data

        json_data = json.loads(cache_data)
        assert json_data['stargazers_count'] == stargazers_count
        assert json_data['forks_count'] == forks_count


def test_external_repo_information_raise_exception_in_case_of_error(redis):
    redis_repository = Container.redis_repository(
        redis_connection=redis,
    )
    owner = "someone"
    repo = "somerepo"

    external_git_repository = Container.external_git_repo_repository(access_token="fake_access_token",
                                                                     cache_repo=redis_repository)

    with patch("app.repository.external_git_repo_repository.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 401
        try:
            external_git_repository.get_cached_or_retrieve_external_repo_info(owner, repo)
        except ExternalAPIError as e:
            assert e.message == "Failed to fetch repository information"
