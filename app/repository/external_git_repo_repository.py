import json

import requests

from abc import ABC, abstractmethod

from app.core.config import setting
from app.repository.cache_repository import CacheRepository
from app.repository.exceptions import ExternalAPIError


class ExternalGitRepoRepository(ABC):

    def __init__(self, access_token: str, cache_repo: CacheRepository):
        self.access_token = access_token
        self.cache_repo = cache_repo

    @abstractmethod
    def _get_external_repo_information(self, owner: str, repo_name: str):
        """
        Fetches repository information.

        :param owner: The username or organization name that owns the repository.
        :param repo_name: The name of the repository.
        :return: A dictionary containing repository information.
        """
        pass

    @abstractmethod
    def get_cached_or_retrieve_external_repo_info(self, owner: str, repo: str) -> dict:
        pass


class ExternalGitHubRepoRepository(ExternalGitRepoRepository):

    def __init__(self, access_token: str, cache_repo: CacheRepository):
        super(ExternalGitHubRepoRepository, self).__init__(access_token, cache_repo)
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.access_token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def _get_external_repo_information(self, owner: str, repo: str) -> dict:
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            data = response.json()

            return {
                "stargazers_count": data.get("stargazers_count", 0),
                "forks_count": data.get("forks_count", 0),
            }
        else:
            raise ExternalAPIError(response.status_code, message="Failed to fetch repository information",
                                   external_api_detail_error=response.json())

    def get_cached_or_retrieve_external_repo_info(self, owner: str, repo: str):
        cache_key = f"repo:{owner}:{repo}"

        if cache_data := self.cache_repo.get(cache_key):
            return json.loads(cache_data)

        external_repo_info = self._get_external_repo_information(owner, repo)
        self.cache_repo.set(cache_key, json.dumps(external_repo_info), ttl=setting.CACHE_DATA_TIME_TO_LIVE)
        return external_repo_info
