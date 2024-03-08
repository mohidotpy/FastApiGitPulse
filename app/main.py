from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from app.api import api_routers
from app.core.config import setting
from app.core.container import Container
from app.entities.exceptions import InvalidDataException
from app.repository.cache_repository import RedisRepository
from app.repository.exceptions import ExternalAPIError
from app.util.class_object import singleton


@singleton
class AppCreator:
    def __init__(self):
        self.app = FastAPI(
            title=setting.PROJECT_NAME,
            openapi_url=f"{setting.API}/openapi.json",
            version="0.0.1",
        )

        # set db and container
        self.container = Container()
        self.db = self.container.db()
        self.redis_connection = self.container.redis_connection()
        # self.db.create_database()

        # set cors
        if setting.BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in setting.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        # set routes
        @self.app.get("/")
        def root():
            return "service is working"

        self.app.include_router(api_routers)

        self.setup_exception_handlers()

    def setup_exception_handlers(self):
        from app.core import exception_handlers

        self.app.add_exception_handler(RequestValidationError, exception_handlers.validation_exception_handler)
        self.app.add_exception_handler(InvalidDataException, exception_handlers.invalid_data_exception_handler)
        self.app.add_exception_handler(ExternalAPIError, exception_handlers.external_api_error_handler)


app_creator = AppCreator()
app = app_creator.app
db = app_creator.db
redis_connection = app_creator.redis_connection
# TODO is it ok or not
app.state.cache = RedisRepository(redis_connection=redis_connection)

container = app_creator.container