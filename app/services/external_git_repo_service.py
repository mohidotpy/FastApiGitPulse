from app.schema.external_git_repo_schema import ExternalRepoPopularityResponseSchema


class ExternalGitRepoService:
    def __init__(self, external_git_repo_repository):
        self._repository = external_git_repo_repository

    def _calculate_score(self, owner: str, repo: str) -> int:
        repo_info = self._repository.get_cached_or_retrieve_external_repo_info(owner=owner, repo=repo)
        return repo_info['stargazers_count'] * 1 + repo_info['forks_count'] * 2

    @staticmethod
    def _is_external_repo_popular(score: int) -> bool:
        return score >= 500

    def fetch_external_repo_popularity_information(self,
                                                   owner: str, repo: str) -> ExternalRepoPopularityResponseSchema:
        score = self._calculate_score(owner=owner, repo=repo)
        is_external_repo_popular = self._is_external_repo_popular(score)

        return ExternalRepoPopularityResponseSchema(score=score, is_popular=is_external_repo_popular)
