from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from app.core.container import Container
from app.core.dependencies import authentication
from app.schema.external_git_repo_schema import GitHubCheckerSchema

from app.services.external_git_repo_service import ExternalGitRepoService

repo_router = APIRouter(prefix="/repositories", dependencies=[Depends(authentication)])


@repo_router.get("/popularity/github/{owner}/{repo}", response_model=GitHubCheckerSchema)
@inject
async def return_popularity_of_github_repository(request: Request, owner: str, repo: str,
                                                 service: ExternalGitRepoService = Depends(
                                                     Provide[Container.external_git_service])):
    return service.fetch_external_repo_popularity_information(owner=owner, repo=repo)
