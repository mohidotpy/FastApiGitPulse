from dependency_injector.wiring import inject
from fastapi import Depends, Request
from fastapi.routing import APIRouter

from app.core.dependencies import authentication
from app.schema.user_schema import CurrentUserSchema

user_router = APIRouter(prefix='/users', tags=['users'], dependencies=[Depends(authentication)])


@user_router.get("/me", response_model=CurrentUserSchema)
@inject
async def get_me(request: Request):
    return CurrentUserSchema.from_orm(request.state.user)
