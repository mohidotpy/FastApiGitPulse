from dependency_injector import containers, providers
from redis import Redis

from app.core.config import setting
from app.core.database import Database
from app.repository.cache_repository import RedisRepository
from app.repository.external_git_repo_repository import ExternalGitHubRepoRepository
from app.repository.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.external_git_repo_service import ExternalGitRepoService
from app.services.user_service import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.auth",
            "app.api.v1.git_info",
            "app.core.dependencies",
        ]
    )
    redis_connection = providers.Singleton(
        Redis,
        host=setting.REDIS_HOST,
        port=setting.REDIS_PORT,
        db=setting.REDIS_DB,
        password=setting.REDIS_PASSWORD,
    )
    db = providers.Singleton(Database, db_url=setting.DATABASE_URI)
    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)
    redis_repository = providers.Factory(
        RedisRepository,
        redis_connection=redis_connection,
    )
    external_git_repo_repository = providers.Factory(ExternalGitHubRepoRepository, access_token=setting.GITHUB_ACCESS_TOKEN,
                                                cache_repo=redis_repository)

    auth_service = providers.Factory(AuthService, user_repository=user_repository)
    user_service = providers.Factory(UserService, user_repository=user_repository)
    external_git_service = providers.Factory(ExternalGitRepoService,
                                             external_git_repo_repository=external_git_repo_repository)
