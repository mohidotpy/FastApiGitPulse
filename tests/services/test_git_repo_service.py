from unittest.mock import patch

import pytest


@pytest.mark.parametrize("star_number, fork_number, expected_is_popular", [
    (500, 800, True),
    (0, 5, False),
])
def test_repo_popularity_service_work_correctly(star_number, fork_number, expected_is_popular, container, redis):
    external_git_service_instance = container.external_git_service()
    owner = "someone"
    repo = "somerepo"
    with patch(
            'app.repository.external_git_repo_repository.ExternalGitHubRepoRepository._get_external_repo_information',
            return_value={"stargazers_count": star_number, "forks_count": fork_number}) as mock_get_info:
        external_repo_popularity_information = external_git_service_instance.fetch_external_repo_popularity_information(
            owner, repo)

        assert external_repo_popularity_information.is_popular == expected_is_popular
