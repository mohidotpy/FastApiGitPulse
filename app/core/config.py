import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

ENV: str = os.getenv("ENV", "prod")


class Configs(BaseSettings):
    API: str = "/api"
    API_V1_STR: str = "/api/v1"
    API_V2_STR: str = "/api/v2"
    PROJECT_NAME: str = "FastApiGitPulse"
    # TODO figure it out

    DB_ENGINE_MAPPER: dict = {
        "postgresql": "postgresql",
    }

    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ALEMBIC_INI_PATH: str = os.path.join(PROJECT_ROOT, 'alembic', 'alembic.ini')

    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 60 minutes * 24 hours * 30 days = 30 days

    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    DB: str = os.getenv("DB")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST", "db")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_ENGINE: str = DB_ENGINE_MAPPER.get(DB, "postgresql")

    DATABASE_URI_FORMAT: str = "{db_engine}://{user}:{password}@{host}:{port}/{database}"

    DATABASE_URI = "{db_engine}://{user}:{password}@{host}:{port}/{database}".format(
        db_engine=DB_ENGINE,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB,
    )

    PAGE = 1
    PAGE_SIZE = 20
    ORDERING = "-id"

    # Redis configurations
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = os.getenv("REDIS_PORT", 6379)
    REDIS_DB: int = os.getenv("REDIS_DB", 0)
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", None)  # Use None if no password is required

    CACHE_DATA_TIME_TO_LIVE = os.getenv("TTL", 3600)

    # Optional: Redis configuration for Celery
    CELERY_REDIS_DB: int = os.getenv("CELERY_REDIS_DB", 1)
    CELERY_BROKER_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{CELERY_REDIS_DB}"
    CELERY_RESULT_BACKEND: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{CELERY_REDIS_DB}"

    GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN", "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")

    class Config:
        case_sensitive = True


class TestConfigs(Configs):
    ENV: str = "test"
    REDIS_DB: int = 10
    CELERY_REDIS_DB: int = 11
    # TODO remove
    DB_HOST: str = "localhost"
    DB_PORT: str = "5433"
    DB: str = "FastApiGitPulseTest"
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_ENGINE_MAPPER: dict = {
        "postgresql": "postgresql",
    }
    DB_ENGINE: str = DB_ENGINE_MAPPER.get(DB, "postgresql")
    DATABASE_URI = "{db_engine}://{user}:{password}@{host}:{port}/{database}".format(
        db_engine=DB_ENGINE,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB,
    )


if ENV == "prod":
    setting = Configs()
elif ENV == "test":
    setting = TestConfigs()
