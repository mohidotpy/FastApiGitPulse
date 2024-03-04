import pytest
import sqlalchemy_utils
from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command

from app.core.config import setting

from fastapi.testclient import TestClient

from app.core.container import Container
from app.core.database import Database
from app.main import app
from sqlalchemy_utils import drop_database


@pytest.fixture
def db_session():
    if sqlalchemy_utils.database_exists(setting.DATABASE_URI):
        drop_database(setting.DATABASE_URI)

    sqlalchemy_utils.create_database(setting.DATABASE_URI)

    engine = create_engine(setting.DATABASE_URI)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    alembic_cfg = Config(setting.ALEMBIC_INI_PATH)
    command.upgrade(alembic_cfg, "head")

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        drop_database(setting.DATABASE_URI)


@pytest.fixture
def container():
    return Container()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[Database.session] = override_get_db
    return TestClient(app)


@pytest.fixture
def redis():
    redis_connection = Redis(
        host=setting.REDIS_HOST,
        port=setting.REDIS_PORT,
        db=setting.REDIS_DB,
        password=setting.REDIS_PASSWORD
    )
    redis_connection.flushdb()
    try:
        yield redis_connection
    finally:
        redis_connection.flushdb()
