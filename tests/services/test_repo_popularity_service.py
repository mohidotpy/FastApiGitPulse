from unittest.mock import patch

import pytest

from app.core.container import Container


@pytest.mark.parametrize("star_number, fork_number, expected_is_popular", [
    (500, 199, True),
    (0, 5, False),
])
def test_repo_popularity_service_work_correctly(star_number, fork_number, expected_is_popular):
    external_git_repo_address = "https://github.com/something/somerepo"
    external_git_service_instance = Container.external_git_service()

    with patch('app.repository.external_git_repo_repository.ExternalGitRepoRepository.get_external_repo_information',
               return_value=(star_number, fork_number)) as mock_get_info:

        external_repo_popularity_information = external_git_service_instance.fetch_external_repo_popularity_information(
            external_git_repo_address)

        assert external_repo_popularity_information.is_popular == expected_is_popular
